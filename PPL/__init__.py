# -*- coding: utf-8 -*-
#  Copyleft  2021-2024 Mattijs Snepvangers.
#  This file is part of Pegasus-ICT Python Library, hereafter named PPL.
#
#  PPL is free software: you can redistribute it and/or modify  it under the terms of the
#   GNU General Public License as published by  the Free Software Foundation, either version 3
#   of the License or any later version.
#
#  PPL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
#   without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#   PURPOSE.  See the GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#   along with PPL.  If not, see <https://www.gnu.org/licenses/>.
"""
Pegasus-ICT Python Library
"""
import inspect
import os
from collections import namedtuple
import platformdirs
import sys

global USER_APP_DIR, SYS_APP_DIR, USER_CACHE_DIR, SYS_CACHE_DIR
global USER_CFG_DIR, SYS_CFG_DIR, USER_DATA_DIR, SYS_DATA_DIR
global USER_LOG_DIR, SYS_LOG_DIR, USER_STATE_DIR, SYS_TYPE
global USER_DOCUMENTS_DIR, USER_DOWNLOADS_DIR, USER_MUSIC_DIR, USER_PICTURES_DIR, USER_VIDEOS_DIR
global USER_DESKTOP_DIR, CONFIG


def set_app_defaults(appname: str, author: str = "Mattijs Snepvangers", version: str = '0.0.0', **kwargs):
    """
            :param appname:str          Application Name, defaults to 'UnknownApp'
            :param author:str           Application Author Name, defaults to 'Mattijs Snepvangers'
            :param version:str          Application Version, defaults to '0.0.0'
            :param opinion:bool         Whether to follow developers' opinion
            :param roaming:bool         Whether to use roaming data profiles on windows networked profiles
            :param multipath:bool       Whether to use roaming data profiles on windows networked profiles
            :param ensure_exists:bool   Makes sure directory exists, default: True
    """
    global USER_APP_DIR, SYS_APP_DIR, USER_CACHE_DIR, SYS_CACHE_DIR
    global USER_CFG_DIR, SYS_CFG_DIR, USER_DATA_DIR, SYS_DATA_DIR
    global USER_LOG_DIR, SYS_LOG_DIR, USER_STATE_DIR, SYS_TYPE
    global USER_DOCUMENTS_DIR, USER_DOWNLOADS_DIR, USER_MUSIC_DIR, USER_PICTURES_DIR, USER_VIDEOS_DIR
    global USER_DESKTOP_DIR

    # Check operating system in use
    if sys.platform == "win32":
        SYS_TYPE = "Windows"
    elif sys.platform == "darwin":
        SYS_TYPE = "MacOS"
    else:
        SYS_TYPE = "Unix"  # Linux, BSD etc
        # check whether we're dealing with android
        import os
        if os.getenv("ANDROID_DATA") == "/data" and os.getenv("ANDROID_ROOT") == "/system":
            if os.getenv("SHELL") or os.getenv("PREFIX"):
                SYS_TYPE = "Android"

    opinion: bool = kwargs.get("opinion", True)
    roaming: bool = kwargs.get("roaming", False)
    multipath: bool = kwargs.get("multipath", False)
    ensure_exists: bool = kwargs.get("ensure_exists", True)

    USER_APP_DIR = platformdirs.user_runtime_dir(appname=appname, appauthor=author, version=version, opinion=opinion,
                                                 ensure_exists=ensure_exists)
    SYS_APP_DIR = platformdirs.site_runtime_dir(appname=appname, appauthor=author, version=version, opinion=opinion,
                                                ensure_exists=ensure_exists)
    USER_CACHE_DIR = platformdirs.user_cache_dir(appname=appname, appauthor=author, version=version, opinion=opinion,
                                                 ensure_exists=ensure_exists)
    SYS_CACHE_DIR = platformdirs.site_cache_dir(appname=appname, appauthor=author, version=version, opinion=opinion,
                                                ensure_exists=ensure_exists)
    USER_CFG_DIR = platformdirs.user_config_dir(appname=appname, appauthor=author, version=version, roaming=roaming,
                                                ensure_exists=ensure_exists)
    SYS_CFG_DIR = platformdirs.site_config_dir(appname=appname, appauthor=author, version=version, multipath=multipath,
                                               ensure_exists=ensure_exists)
    USER_DATA_DIR = platformdirs.user_data_dir(appname=appname, appauthor=author, version=version, roaming=roaming,
                                               ensure_exists=ensure_exists)
    SYS_DATA_DIR = platformdirs.site_data_dir(appname=appname, appauthor=author, version=version, multipath=multipath,
                                              ensure_exists=ensure_exists)
    USER_LOG_DIR = platformdirs.user_log_dir(appname=appname, appauthor=author, version=version, opinion=opinion,
                                             ensure_exists=ensure_exists)
    SYS_LOG_DIR = SYS_TYPE == "Unix" and "/var/log/" or USER_LOG_DIR
    USER_STATE_DIR = platformdirs.user_state_dir(appname=appname, appauthor=author, version=version, roaming=roaming,
                                                 ensure_exists=ensure_exists)
    USER_DOCUMENTS_DIR = platformdirs.user_documents_dir()
    USER_DOWNLOADS_DIR = platformdirs.user_downloads_dir()
    USER_MUSIC_DIR = platformdirs.user_music_dir()
    USER_PICTURES_DIR = platformdirs.user_pictures_dir()
    USER_VIDEOS_DIR = platformdirs.user_videos_dir()
    USER_DESKTOP_DIR = platformdirs.user_desktop_dir()


class PPL(namedtuple("Library", "base_path config_dir config_file_type config_file_name")):
    """
        Pegasus-ICT Python Library
    """

    def __init__(self, **kwargs):
        """
        :param base_path:
        :param config_dir:
        :param config_file_type:
        :param config_file_name:

        PPL Initiator
        """
        _base_path = kwargs.get("base_path", os.path.dirname(os.path.abspath((inspect.stack()[0])[1])))
        self._base_path = _base_path if _base_path[-1] == "/" else _base_path + "/"

        global CONFIG
        config_path = kwargs.get("config_path", "config/")
        self._config_path = config_path if config_path[0] == "/" else self.base_path + config_path

        self._config_file_name = kwargs.get("config_file_name", "config")
        self._config_file_type = kwargs.get("config_file_type", "ini")

