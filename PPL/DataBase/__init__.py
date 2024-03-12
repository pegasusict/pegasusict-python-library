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

# DB Type
global database_type
# encoding
global database_encoding
# DB URI([user:pass@]URL[:port], socket, file)
global database_uri


class DataBaseInterface(metaclass=abc.ABCMeta):
    """
    Interface Metaclass for DataBase classes
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
                hasattr(subclass, "insert")
                and callable(subclass.insert_value)
                and hasattr(subclass, "set_value")
                and callable(subclass.set_value)
                and hasattr(subclass, "search")
                and callable(subclass.search)
                and hasattr(subclass, "update")
                and callable(subclass.update)
                and hasattr(subclass, "delete")
                and callable(subclass.delete)
        )


class DataBaseSuper:
    """DataBaseSuper base class"""

    def query(self, query: str):
        """placeholder for child classes"""
        pass

    def insert(self, insert, into: str = ''):
        return self.query(self, "INSERT " + insert + " INTO " + into)

    def update(self, update, into: str = '', where: str = '', comp=None, val=None, val2=None):
        if comp in {'=', 'EQ', '>', 'GT', '<', 'LT', '>=', 'GTE', '<=', 'LTE', '<>', 'NE', 'BETWEEN', 'LIKE', 'IN'}:
            if val2 is not None:
                val += ' and ' + val2
            return self.query(self, "UPDATE " + update + " INTO " + into + " WHERE " + where + ' ' + comp + ' ' + val)
        return self.query(self, "UPDATE " + update + " INTO " + into + " WHERE " + where)

