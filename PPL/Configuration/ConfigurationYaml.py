#  Copyleft  2021-2024 Mattijs Snepvangers.
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
from PPL.Configuration import ConfigurationSuper
import yaml


class ConfigurationXml(ConfigurationSuper):
    """
    Yaml configuration
    """

    def __init__(self, filepath: str):
        super().__init__()
        file_contents = open(filepath)
        self._config = yaml.safe_load(file_contents)
