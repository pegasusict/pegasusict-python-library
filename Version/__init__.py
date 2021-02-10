# -*- coding: utf-8 -*-

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

import re
from collections import namedtuple
from datetime import date


class VersionError(Exception):
    pass


class Version(namedtuple("VersionBase", "major minor patch identifier revision build")):
    # {'major': 3, 'minor': 4, 'patch': 5, 'prerelease': 'pre.2', 'build': 'build.4'}
    _version_re = re.compile(
        r"/(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*["
        r"a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>["
        r"0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?/gm"
    )
    _identifiers = {
        "dev": 0,
        "alpha": 1,
        "a": 1,
        "beta": 2,
        "b": 2,
        "rc": 3,
        "pre": 4,
        "final": 5,
    }
    _build: str = ""

    def __new__(
        cls,
        major: int,
        minor: int = 0,
        patch: int = 0,
        rel: str = "final",
        rev: int = 0,
        build: str = None,
    ):
        """

        :type major: int
        :type minor: int
        :type patch: int
        :type rel: string
        :type rev: int
        :type build: string
        """
        if rel not in cls.valid_phases():
            raise VersionError(
                "Should be either 'final', 'pre', 'rc', 'beta', 'alpha' or 'dev'"
            )
        rel = {"a": "alpha", "b": "beta"}.get(rel, rel)
        try:
            major = int(major)
            minor = int(minor)
            patch = int(patch)
            rev = int(rev)
        except (TypeError, ValueError):
            raise VersionError(
                "major, minor, patch and revision must be integer values"
            )
        return super(Version, cls).__new__(cls, major, minor, patch, rel, rev, build)

    @classmethod
    def from_string(cls, version_str):
        match = cls._version_re.search(version_str)
        if match:
            (major, minor, patch, identifier, revision) = match.groups()
            major = int(major)
            if minor is None:
                return Version(major)
            minor = int(minor)
            if patch is None:
                return Version(major, minor)
            patch = int(patch)
            if identifier is None:
                return Version(major, minor, patch)
            revision = int(revision)
            return Version(major, minor, patch, identifier, revision)
        raise VersionError(
            "String '%s' does not match regex '%s'"
            % (version_str, cls._version_re.pattern)
        )

    @classmethod
    def valid_phases(cls):
        return set(cls._identifiers.keys())

    def to_string(self, short=False):
        if short and self.identifier in ("alpha", "beta"):
            version = self._replace(identifier=self.identifier[0])
        else:
            version = self
        if short and version.identifier == "final":
            if version.patch == 0:
                version_str = "%d.%d" % version[:2]
            else:
                version_str = "%d.%d.%d" % version[:3]
        elif short and version.identifier in ("a", "b", "rc"):
            version_str = "%d.%d.%d-%s%d" % version
        elif version.get_build is not None:
            version_str = "%d.%d.%d-%s%d+%s" % version
        else:
            version_str = "%d.%d.%d-%s%d" % version
        return version_str

    @property
    def sort_key(self):
        return self[:3] + (self._identifiers.get(self.identifier, 0), self.revision)

    def __str__(self):
        return self.to_string()

    def __lt__(self, other):
        if not isinstance(other, Version):
            other = Version(*other)
        return self.sort_key < other.sort_key

    def __le__(self, other):
        if not isinstance(other, Version):
            other = Version(*other)
        return self.sort_key <= other.sort_key

    def __gt__(self, other):
        if not isinstance(other, Version):
            other = Version(*other)
        return self.sort_key > other.sort_key

    def __ge__(self, other):
        if not isinstance(other, Version):
            other = Version(*other)
        return self.sort_key >= other.sort_key

    def __eq__(self, other):
        if not isinstance(other, Version):
            other = Version(*other)
        return self.sort_key == other.sort_key

    def __ne__(self, other):
        if not isinstance(other, Version):
            other = Version(*other)
        return self.sort_key != other.sort_key

    def __hash__(self):
        return super().__hash__()

    def set_build(
        self, year: int, month: int, day: int, iteration: int = None
    ) -> object:
        """Sets build string

        :rtype: Version
        """
        _build = date(year, month, day).strftime("%Y%m%d")
        if iteration > 0:
            self._build = str(_build) + "." + str(iteration)
        else:
            self._build = str(_build)
        return self

    def get_build(self):
        if self._build is not None:
            return str(self._build)
        else:
            return None
