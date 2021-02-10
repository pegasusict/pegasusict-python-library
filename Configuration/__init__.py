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
from dotenv import load_dotenv
import confuse
import argparse
import PPL


class Configuration:
    _extensions = {
        'ini': ('cfg', 'ini', 'conf', 'cnf'),
        'json': ('json', 'jsn'),
        'toml': ('toml', 'tml'),
        'yaml': ('yaml', 'yml')
    }
    _config = None
    _file_config = None
    _env = None
    _args = None
    _basedir: str = None
    _filetype = 'ini'
    _filename = "config.ini"

    def __init__(self, **kwargs):
        """
        :arg filename: string
        :arg filetype: string
        :arg basedir: string"""
        self._basedir = path.abspath(path.dirname(__file__))
        if 'basedir' in kwargs:
            self._basedir = str(kwargs.get('basedir'))
        # parse environment
        self._parse_env()

        # parse file
        filename = self._filename
        filetype = self._filetype
        module_name = "Ini"
        if 'type' in kwargs and kwargs.get('type') in set(self._extensions.keys()):
            module_name = str(kwargs.get('type')).capitalize()
        if 'filename' in kwargs:
            filename = kwargs.get("filename")
        if self._check_file(filetype, filename):
            self._config = PPL.load(__name__, module_name)
        # parse arguments
        parser = argparse.ArgumentParser(description='Configure AMM Core')
        arg_group = parser.add_mutually_exclusive_group()
        arg_group.add_argument("-v", "--verbose", default=1, action="store_true", help="Increase feedback level.")
        arg_group.add_argument("-q", "--quiet", action="store_true", help="Mute feedback.")
        parser.parse_args()

    def set(self, **kwargs):
        """Sets config value to [section]key

        :param kwargs:
        :return:
        """
        if 'value' in kwargs:
            value = str(kwargs.get('value'))
        else:
            raise ValueError("Value is a mandatory argument")
        if 'key' in kwargs:
            key = str(kwargs.get('key'))
        else:
            raise ValueError("Key is a mandatory argument")
        if 'section' in kwargs:
            section = str(kwargs.get('section'))
            self._config.set(section=section, key=key, value=value)
        else:
            self._config.set(key=key, value=value)

    def get(self, **kwargs):
        """Get config value from [section]key

        :param kwargs:
        :return:
        """
        section = None
        if 'value' in kwargs:
            value = str(kwargs.get('value'))
        else:
            raise ValueError("Value is a mandatory argument")
        if 'key' in kwargs:
            key = str(kwargs.get('key'))
        else:
            raise ValueError("Key is a mandatory argument")
        if 'section' in kwargs:
            section = str(kwargs.get('section'))
            return self._config[section][key] or False
        else:
            return self._config[key] or False

    def save(self):
        pass

    def _parse_env(self):
        self._env = load_dotenv(path.join(self._basedir, '../.env'))

    def _parse_toml(self, filename: str):
        self._file_config = toml.load(filename)

    def _parse_yaml(self, filename: str):
        self._file_config = confuse.Configuration(globals()['AMM_APP_NAME'], self._filename)

    def _check_file(self, filetype: str, filename: str) -> bool:
        has_ext = False
        has_known_ext = False

        if "." in filename:
            if filename.split(".")[-1][1:] in self._extensions[filetype]:
                has_ext = True
                has_known_ext = True
            else:
                has_ext = True
                has_known_ext = False

        if not has_ext or not has_known_ext:
            if isinstance(self._extensions[filetype], tuple):
                filename += self._extensions[filetype][0]
            else:
                filename += self._extensions[filetype]

        if path.exists(filename):
            self._filename = filename
            return True
        return False
