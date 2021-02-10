#  Copyleft  2021 Mattijs Snepvangers.
#  This file is part of Audiophiles' Music Manager, hereafter named AMM.
#
#  AMM is free software: you can redistribute it and/or modify  it under the terms of the
#   GNU General Public License as published by  the Free Software Foundation, either version 3
#   of the License or any later version.
#
#  AMM is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
#   without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#   PURPOSE.  See the GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#   along with AMM.  If not, see <https://www.gnu.org/licenses/>.
from configparser import ConfigParser


class Configuration:
    """Ini file based configuration module
    :arg: filename
    """

    _config = list()

    def __init__(self, filename: str):
        _parser = ConfigParser()
        self._config = _parser.read(filename)

    def set(self, **kwargs):
        """Sets config value to [section]key

        :param kwargs:
        :return:
        """
        section = None
        value = str(kwargs.get("value"))
        key = str(kwargs.get("key"))
        if "section" in kwargs:
            section = str(kwargs.get("section")) or None
        if section is not None:
            self._config[section][key] = value
        else:
            self._config[key] = value

    def get(self, **kwargs):
        """Get config value from [section]key

        :param kwargs:
        :return:
        """
        section = None
        value = str(kwargs.get("value"))
        key = str(kwargs.get("key"))
        if "section" in kwargs:
            section = str(kwargs.get("section")) or None

        if section is not None:
            return self._config[section][key] or False
        else:
            return self._config[key] or False

    def save(self):
        pass
