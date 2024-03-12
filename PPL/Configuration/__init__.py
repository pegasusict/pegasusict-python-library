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

import abc
import envargparse
from os import path

global config_file_type, config_file_name, config_path, DEFAULT_SECTION


def _load_defaults():
    """
        loads common configuration defaults
    """
    global DEFAULT_SECTION
    DEFAULT_SECTION = "main"


def _parse_env(env_args: dict):
    """
    Parse Argument and ENV variables
    :param env_args: (arg(
    :return:
    """
    if len(env_args) == 0:
        return None
    parser = envargparse.EnvArgParser()
    for arg in env_args:
        parser.add_argument(
            # "-u", "--url", envvar='URL',
            # help="Specify the URL to process (can also be specified using URL environment variable)"
        )
    args = parser.parse_args()


class ConfigurationSelector:
    """Is used to choose/detect (a) Configuration Variation(s)"""

    EXTENSIONS = {
        "ini": ("cfg", "ini", "conf", "cnf"),
        "json": ("json", "jsn"),
        "toml": ("toml", "tml"),
        "xml": ("xml", "xlt"),
        "yaml": ("yaml", "yml"),
    }

    @classmethod
    def select(cls, **kwargs):
        """

        :param kwargs:
            base_path
        """
        global config_file_type
        global config_file_name
        global config_path
        for key in ("config_file_type", "config_file_name", "config_path"):
            if key in kwargs and kwargs.get(key) in set(cls.EXTENSIONS.keys()):
                globals()[key] = str(kwargs.get(key))

        config_file_type = config_file_type or list(cls.EXTENSIONS.keys())[0]
        config_file_name = config_file_name or "config"
        config_path = config_path or path.abspath(__file__)

        if cls._check_file():
            if config_file_type == "yaml":
                from ConfigurationYaml import Configuration
            elif config_file_type == "toml":
                from ConfigurationToml import Configuration
            elif config_file_type == "xml":
                from ConfigurationXml import Configuration
            elif config_file_type == "json":
                from ConfigurationJson import Configuration
            else:
                from ConfigurationIni import Configuration

            globals()["Config"] = Configuration(filename=config_path + config_file_name)

    @classmethod
    def _check_file(cls) -> bool:
        global config_file_type
        global config_file_name
        global config_path
        has_ext = False
        has_known_ext = False

        if "." in config_file_name:
            if config_file_name.split(".")[-1][1:] in cls.EXTENSIONS[config_file_type]:
                has_ext = True
                has_known_ext = True
            else:
                has_ext = True
                has_known_ext = False

        if not has_ext or not has_known_ext:
            config_file_name += cls.EXTENSIONS[config_file_type][0]

        if path.exists(config_path + config_file_name):
            return True
        return False


class ConfigurationInterface(metaclass=abc.ABCMeta):
    """
    Interface Metaclass for Configuration classes
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
                hasattr(subclass, "get_value")
                and callable(subclass.get_value)
                and hasattr(subclass, "set_value")
                and callable(subclass.set_value)
                and hasattr(subclass, "save")
                and callable(subclass.save)
                and hasattr(subclass, "load")
                and callable(subclass.load)
        )


class ConfigurationSuper:
    """ConfigurationSuper base class"""

    _config = dict()
    _args = dict()

    def __init__(self, **kwargs):
        """
        :arg filename: string
        :arg filetype: string
        :arg basedir: string
        """
        self._filename: str = ""
        _load_defaults()
        _parse_env(env_args=kwargs.get("env_args"))
        self._filetype: str = ""

        # parse file
        filename = self._filename
        filetype = self._filetype
        module_name = "Ini"

        # parse arguments
        parser = envargparse.EnvArgParser()
        arg_group = parser.add_mutually_exclusive_group()
        arg_group.add_argument(
            "-v",
            "--verbose",
            default=1,
            action="store_true",
            help="Increase feedback level.",
        )
        arg_group.add_argument("-q", "--quiet", action="store_true", help="Mute feedback.")
        parser.parse_args()

    def _read_file(self, file_path: str, encoding="utf-8", mode="r"):
        """Opens file in read/write mode and hands back the file object.

        file_path: str
        encoding: str
        """
        if mode == "w":
            mode = "w"
        else:
            mode = "r"
        self.file_object = open(file_path, mode)
        self.file_contents = self.file_object.read()

    def set(self, **kwargs):
        """Sets config value to [section]key

        :param kwargs:
        :return:
        """
        if "value" in kwargs:
            value = str(kwargs.get("value"))
        else:
            raise ValueError("Value is a mandatory argument")
        if "key" in kwargs:
            key = str(kwargs.get("key"))
        else:
            raise ValueError("Key is a mandatory argument")
        if "section" in kwargs:
            section = str(kwargs.get("section"))
            self._config[section][key] = value
        else:
            self._config[key] = value

    def get(self, **kwargs):
        """Get config value from [section]key

        :param kwargs:
        :return:
        """
        if "key" in kwargs:
            key = str(kwargs.get("key"))
        else:
            raise ValueError("Key is a mandatory argument")
        if "section" in kwargs:
            section = str(kwargs.get("section"))
            return self._config[section][key] or False
        else:
            return self._config[key] or False

    def save(self, file):
        """
        placeholder for save function in subclasses
        """
        self.file_object.write(file)
