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
from urllib import parse as urlparse

import requests

from PPL import Configuration


def ar_message(**kwargs):
    url = "https://autoremotejoaomgcd.appspot.com/sendmessage"
    key = Configuration.get(section="tasker", key="ar_key")
    message = kwargs.get("message", "This is a test.")
    target = Configuration.get(section="tasker", key="ar_target")
    sender = kwargs.get("sender", "PPL")
    password = Configuration.get(section="tasker", key="ar_password")

    querystring = {
        "key": key,
        "message": urlparse.quote(sender.upper() + " " + message, safe=''),
        "target": target,
        "password": password
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
    }

    response = requests.get(url=url, headers=headers, params=querystring)

    print(response.json())


class TaskerAPI:
    pass
