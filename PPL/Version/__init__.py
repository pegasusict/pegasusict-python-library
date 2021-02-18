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
"""Version related classes, Semantic Versioning compatible though somewhat stricter. v0.1.0-alpha+20210213"""
import re
from collections import namedtuple
from datetime import date


class VersionError(Exception):
    """Used to raise Errors form PPL's Version class"""

    pass


class Version(
    namedtuple("VersionBase", "major minor patch release revision build", defaults=(0, 0, 0, "final", 0, None))
):
    """Semantic Version compatible."""

    # noinspection PyMissingConstructor
    def __init__(self, major=0, minor=0, patch=0, release="final", revision=0, build=None):
        self._major = major or 0
        self._minor = minor or 0
        self._patch = patch or 0
        self._release = release or "final"
        self._revision = revision or 0
        self._build = build or None

    _version_re = re.compile(
        r"/(?P<major>0|[1-9]\d*)"
        r"\.(?P<minor>0|[1-9]\d*)"
        r"\.(?P<patch>0|[1-9]\d*)"
        r"(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
        r"(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?/gm"
    )
    _releases = {"dev": 0, "test": 1, "alpha": 2, "a": 2, "beta": 3, "b": 3, "rc": 4, "pre": 5, "final": 6}
    _build: str = ""

    def __new__(cls, major=0, minor=0, patch=0, release="final", revision=0, build=None):
        """

        :type major: int
        :type minor: int
        :type patch: int
        :type release: string
        :type revision: int
        :type build: string
        """
        if release not in cls.valid_releases():
            raise VersionError("Release should be either 'final', 'pre', 'rc', 'beta', 'alpha' or 'dev'")
        release = {"a": "alpha", "b": "beta"}.get(release, release)
        try:
            major = int(major)
            minor = int(minor)
            patch = int(patch)
            revision = int(revision)
        except (TypeError, ValueError):
            raise VersionError("major, minor, patch and revision must be integer values")
        # noinspection PyArgumentList
        return super(Version, cls).__new__(cls, major, minor, patch, release, revision, build)

    @classmethod
    def from_string(cls, version_str):
        """

        :param version_str:
        :return:
        """
        match = cls._version_re.search(version_str)
        if match:
            (major, minor, patch, release, revision) = match.groups()
            major = int(major)
            if minor is None:
                return Version(major)
            minor = int(minor)
            if patch is None:
                return Version(major, minor)
            patch = int(patch)
            if release is None:
                return Version(major, minor, patch)
            revision = int(revision)
            return Version(major, minor, patch, release, revision)
        raise VersionError("String '%s' does not match regex '%s'" % (version_str, cls._version_re.pattern))

    @classmethod
    def valid_releases(cls):
        """

        :return:
        """
        return set(cls._releases.keys())

    def to_string(self, short=False):
        """

        :param short:
        :return:
        """
        if short and self._release in ("alpha", "beta"):
            version = self._replace(release=self._release[0])
        else:
            version = self
        if short and version._release == "final":
            if version._patch == 0:
                version_str = "%d.%d" % version[:2]
            else:
                version_str = "%d.%d.%d" % version[:3]
        elif short and version._release in ("a", "b", "rc"):
            version_str = "%d.%d.%d-%s%d" % version
        elif version.get_build is not None:
            version_str = "%d.%d.%d-%s%d+%s" % version
        else:
            version_str = "%d.%d.%d-%s%d" % version
        return version_str

    @property
    def sort_key(self):
        """

        :return:
        """
        return self[:3] + (self._releases.get(self._release, 0), self._revision)

    def __str__(self):
        return self.to_string()

    def __lt__(self, other):
        if not isinstance(other, Version):
            other = Version()
        return self.sort_key < other.sort_key

    def __le__(self, other):
        if not isinstance(other, Version):
            other = Version()
        return self.sort_key <= other.sort_key

    def __gt__(self, other):
        if not isinstance(other, Version):
            other = Version()
        return self.sort_key > other.sort_key

    def __ge__(self, other):
        if not isinstance(other, Version):
            other = Version()
        return self.sort_key >= other.sort_key

    def __eq__(self, other):
        if not isinstance(other, Version):
            other = Version()
        return self.sort_key == other.sort_key

    def __ne__(self, other):
        if not isinstance(other, Version):
            other = Version()
        return self.sort_key != other.sort_key

    def __hash__(self):
        return super().__hash__()

    def set_build(self, year: int, month: int, day: int, iteration: int = None) -> object:
        """Sets build string

        :rtype: Version
        """
        _build = date(year, month, day).strftime("%Y%m%d")
        if iteration > 0:
            self._build = str(_build) + "." + str(iteration)
        else:
            self._build = str(_build)
        return self

    def get_build(self) -> str or None:
        """

        :return:
        """
        return self._build
