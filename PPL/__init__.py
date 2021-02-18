#  Copyleft (c) 2021 Mattijs Snepvangers.
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


class PPL(namedtuple("Library", "base_path config_dir config_file_type config_file_name")):
    """
    Pegasus-ICT Python Library
    """

    def __init__(self, **kwargs):
        _base_path = kwargs.get(key="base_path", default=os.path.dirname(os.path.abspath((inspect.stack()[0])[1])))
        self._base_path = _base_path if _base_path[-1] == "/" else _base_path + "/"

        config_path = kwargs.get(key="config_path", default="config/")
        self._config_path = config_path if config_path[0] == "/" else self.base_path + config_path

        self._config_file_name = kwargs.get(key="config_file_name", default="config")
        self._config_file_type = kwargs.get(key="config_file_type", default="ini")

        if self._config_file_type == "yaml":
            from Configuration import ConfigurationYaml as Class
        elif self._config_file_type == "toml":
            from Configuration import ConfigurationToml as Class
        elif self._config_file_type == "json":
            from Configuration import ConfigurationJson as Class
        else:
            from Configuration import ConfigurationIni as Class
