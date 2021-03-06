# -*- coding: utf-8 -*-
#  Copyleft  2021 Mattijs Snepvangers.
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
from os import path
import abc
from io import TextIOBase

global config_file_type
global config_file_name
global config_path
global DEFAULT_SECTION


class ConfigurationSelector:
    """Is used to choose a particular Configuration Variant"""

    EXTENSIONS = {
        "ini": ("cfg", "ini", "conf", "cnf"),
        "json": ("json", "jsn"),
        "toml": ("toml", "tml"),
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


def _load_defaults():
    """loads common configuration defaults"""
    global DEFAULT_SECTION

    DEFAULT_SECTION = "general"


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
        self._parse_env()
        self._filetype: str = ""

        # parse file
        filename = self._filename
        filetype = self._filetype
        module_name = "Ini"

        # parse arguments
        parser = argparse.ArgumentParser(description="Configure AMM Core")
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

    def _open_file(self, file_path: str, encoding="utf-8"):
        """Opens file in read/write mode and hands back the file object.

        file_path: str
        encoding: str
        """
        self.file_object = io.
        (file_path, mode="+", encoding=encoding)
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
            self._config.set(section=section, key=key, value=value)
        else:
            self._config.set(key=key, value=value)

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

    def save(self):
        """
        placeholder for save function in subclasses
        """
        pass
