"""
This module implements OpenSubtitles interface.
"""

import binascii
import datetime
import gzip
import http.client
import json
import os
import struct
import xml
import xmlrpc.client
from typing import List

from opensubtitles_downloader import error_handler
from opensubtitles_downloader.constants import OPENSUBTITLES_URL, VERBOSE_OPTION, USER_CONFIG_FILE
from opensubtitles_downloader.logger import logger
from opensubtitles_downloader.util import get_title


def hash_file(name: str) -> str:
    """
    Copied from
    https://trac.opensubtitles.org/projects%3Cscript%20type=/opensubtitles/wiki/HashSourceCodes
    """
    with open(name, "rb") as f:
        longlongformat = '<q'  # little-endian long long
        bytesize = struct.calcsize(longlongformat)

        filesize = os.path.getsize(name)
        filehash = filesize

        if filesize < 65536 * 2:
            return "SizeError"

        for _ in range(65536 // bytesize):
            buffer = f.read(bytesize)
            (l_value, ) = struct.unpack(longlongformat, buffer)
            filehash += l_value
            filehash = filehash & 0xFFFFFFFFFFFFFFFF  # to remain as 64bit number

        f.seek(max(0, filesize-65536), 0)
        for _ in range(65536 // bytesize):
            buffer = f.read(bytesize)
            (l_value, ) = struct.unpack(longlongformat, buffer)
            filehash += l_value
            filehash = filehash & 0xFFFFFFFFFFFFFFFF

        return "%016x" % filehash

    return None


def query_struct(filename: str, sublanguageid: str) -> list:
    """ Return a OpenSubtitles API compatible object for search queries. """

    info = {
        'sublanguageid': sublanguageid,
        'moviehash': hash_file(filename),
        'moviebytesize': os.path.getsize(filename),
        'imdbid': '',
        'query': '',
        'season': '',
        'episode': '',
        'tag': ''
    }
    return [info]  # for OpenSubtitle API support


def decode(content: str) -> str:
    """ Try to decode 'content' with various codec. """
    try:
        data = content.decode('utf-8')
    except UnicodeDecodeError:
        try:
            data = content.decode('latin-1')
        except UnicodeDecodeError:
            data = content.decode('ascii')
    return data


class Singleton(object):
    __instance = None

    def __new__(cls):
        if Singleton.__instance is None:
            Singleton.__instance = object.__new__(cls)
        return Singleton.__instance


class OpenSubtitle(Singleton):

    def __init__(self):
        """
        Inizialize a client for xml-rpc connection with OpenSubtitle.org
        """
        self.__token: str = None
        self.__languages: List[str] = None
        try:
            self.__proxy: 'ServerProxy' = xmlrpc.client.ServerProxy(OPENSUBTITLES_URL)
        except (xmlrpc.client.Fault, xmlrpc.client.ProtocolError) as err:
            error_handler.handle(err)

    def login(self,
              username: str = "",
              password: str = "",
              languages: List[str] = ["all"],
              useragent: str = "OSTestUserAgentTemp") -> None:
        """ Token is a unique identifier given by OpenSubtitle. """
        if self.__token:  # login already done
            return True

        try:
            login = self.__proxy.LogIn(username, password, languages[0], useragent)
            if not login:
                raise OpenSubtitleError("login problem...")
        except (xmlrpc.client.Fault,
                xmlrpc.client.ProtocolError,
                OpenSubtitleError) as err:
            self.__token = None
            error_handler.handle(err)
        else:
            self.__token = login['token']
        self.__languages = languages

    def logout(self, token: str = "") -> None:
        """ Opensubtitles logout """
        token = token if token else self.__token
        try:
            self.__proxy.LogOut(token)
        except (xmlrpc.client.Fault, xmlrpc.client.ProtocolError,
                TypeError) as err:
            error_handler.handle(err)

    def keep_alive(self, token: str = "") -> None:
        """ Should be called every 15 minutes to keep session alive. """
        token = token if token else self.__token
        try:
            self.__proxy.NoOperation(token, 'allow_none')
        except (xmlrpc.client.Fault, xmlrpc.client.ProtocolError) as err:
            error_handler.handle(err)

    def get_token(self) -> str:
        return self.__token

    def _search_subtitle(self, sublanguage: str = 'all', filenames: list = None) -> list:
        try:
            results = [self.__proxy.SearchSubtitles(self.__token, query_struct(f, sublanguage)) for f in filenames]
        except (xmlrpc.client.Fault, xmlrpc.client.ProtocolError,
                http.client.ResponseNotReady, OverflowError, TypeError) as err:
            if VERBOSE_OPTION:
                error_handler.handle(err)
            return None
        else:
            result = results[0] if any(results) else None

            if not result:
                return None

            elif (result['status'] == '503 Service Unavailable'
                  or result['status'] == '414 Unknown User Agent'
                  or result['status'] == '415 Disabled user agent'):
                logger.info(result['status'])
                return None

            ## This fix was necessary because we can't always trust hash to catch the correct subtitle, we need to look
            ## at the title of the subtitle to match the video title if we want to be sure.
            _, filename = os.path.split(filenames[0])  # we never search for more than 1 file per time
            title = get_title(filename)
            return [data for data in result['data'] if get_title(data['SubFileName']) == title]
            # return list(filter(lambda data: guessit(data['SubFileName'])['title'] == guessit(filename)['title'], result['data']))

    def _download_subtitles(self, filenames: list = None) -> (list, None):
        """
        More compatible with OpenSubtitles API.
        Return a list of dictionary:
        each 'data' in dictionary has to decode from base64 and gunzip to be
        readable.
        """
        result = None
        language = None
        for _language in self.__languages:
            result = self._search_subtitle(_language, filenames)
            if result:
                language = _language
                break

        # If no subtitle was found, try with english one
        if not result:
            language = 'eng'
            result = self._search_subtitle(language, filenames)
            if not result:
                return None, None  # neither english subtitle was found

        subtitle_id = result[0]['IDSubtitleFile']
        token = self.__token

        try:
            subtitle = self.__proxy.DownloadSubtitles(token, [subtitle_id])
        except (xmlrpc.client.Fault, xmlrpc.client.ProtocolError) as err:
            if VERBOSE_OPTION:
                error_handler.handle(err)
        else:
            if subtitle['status'] == '407 Download limit reached' and VERBOSE_OPTION:
                logger.warning(subtitle['status'], ': retry later.')
                return None, None

            return subtitle['data'], language

        return None, None

    def download_subtitle(self, filename: str = "") -> (str, str):
        """ Not compatible with OpenSubtitles API. """

        result, language = self._download_subtitles([filename])
        if not result:
            return None, None

        subtitle = result[0]['data']
        content = gzip.decompress(binascii.a2b_base64(subtitle))
        return decode(content), language


class OpenSubtitleError(Exception):
    def __init__(self, message):
        self.message = "[*] Opensubtitle " + message


def web_service_login(language: str = None) -> 'OpenSubtitle':
    """
    Login to OpenSubtitles using credentials in default configuration file
    location:
        {SubtitleDownloader_script}/opensubtitles_config.json
    """
    config_file = USER_CONFIG_FILE

    # Get OpenSubtitle user account info from config.json file.
    if not os.path.exists(config_file) or not os.path.isfile(config_file):
        logger.error("file '{}' couldn't be found.".format(config_file))
        return None

    with open(config_file, 'r') as config:
        try:
            decoder = json.JSONDecoder()

            userconfig = decoder.decode(config.read())

            username = userconfig['username']
            password = userconfig['password']
            languages = userconfig['languages']
            useragent = userconfig['useragent']

            # OpenSubtitle login
            opensubtitle = OpenSubtitle()
            opensubtitle.login(username, password, languages if not language else [language], useragent)

        except (json.decoder.JSONDecodeError,
                OpenSubtitleError,
                xml.parsers.expat.ExpatError) as err:
            error_handler.handle(err)
        else:
            return opensubtitle

    return None


def keep_alive_signal(opensubtitle: 'OpenSubtitle', start: datetime) -> None:
    """ Send keep-alive signal every 15 minutes (14 to be sure)  """
    delta = datetime.timedelta(minutes=14)
    if datetime.datetime.now() >= start + delta:
        opensubtitle.keep_alive()
