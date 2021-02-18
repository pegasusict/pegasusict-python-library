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

# import PPL.Configuration as Module
from PPL.Configuration import ConfigurationSuper
import json


class ConfigurationJson(ConfigurationSuper):
    """JSON based Configuration"""

    def __init__(self, filename: str):
        super().__init__()
        _json = json.load(super()._open_file(filename).read())
        _sections = _json.sections()
        _sections.append("general")

    def load(self):
        """Save modified configuration data to file."""
        pass

    def save(self):
        """Save modified configuration data to file."""
        pass
