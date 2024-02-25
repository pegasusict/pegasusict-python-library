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

class PplException(BaseException):
    """Raised in case of error concerning PPL functionality

        Attributes:
            cls  -- Class in which the error occurred
            func -- Function in which the error occurred
            msg  -- Error message
        """

    def __init__(self, cls: str, func: str, msg: str = "Something did a booboo"):
        self.cls = cls
        self.func = func
        self.message = cls + "=>" + func + "(): " + msg
        super().__init__(self.message)


class CommunicationException(PplException):
    """Raised in case of error concerning communication functionality"""
    pass


class ConfigurationException(PplException):
    """Raised in case of error concerning Configuration functionality"""
    pass


class DataBaseException(PplException):
    """Raised in case of error concerning DataBase functionality"""
    pass
