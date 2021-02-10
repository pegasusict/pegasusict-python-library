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


def load(variant: str, group: str, args: list = ()) -> object:
    """

    :param variant:
    :param group:
    :param args:
    :return:
    """
    group = group.capitalize()
    variant = variant.capitalize()

    if group == "General" or group == "":
        if variant == "Version":
            import Version as Class

    elif group == "Configuration":
        if variant == "Ini":
            from Configuration import ConfigurationIni as Class
        elif variant == "Toml":
            from Configuration import ConfigurationToml as Class
        else:
            from Configuration import ConfigurationIni as Class
    if args.__sizeof__() > 0:
        return Class(args[:])
    else:
        return Class
