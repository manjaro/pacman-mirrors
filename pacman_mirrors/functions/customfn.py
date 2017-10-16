#!/usr/bin/env python
#
# This file is part of pacman-mirrors.
#
# pacman-mirrors is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pacman-mirrors is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pacman-mirrors.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Frede Hundewadt <echo ZmhAbWFuamFyby5vcmcK | base64 -d>

"""Pacman-Mirrors Custom Functions"""

import os

from pacman_mirrors.config import configuration as conf
from pacman_mirrors.constants import txt
from pacman_mirrors.functions import jsonfn


def convert_to_json():
    """Convert custom mirror file to json"""
    print(".: {} {}".format(txt.INF_CLR, txt.CONVERT_CUSTOM_MIRROR_FILE))
    mirrors = []
    with open(conf.O_CUST_FILE, "r") as mirrorfile:
        mirror_country = None
        for line in mirrorfile:
            country = get_country(line)
            if country:
                mirror_country = country
                continue
            mirror_url = get_url(line)
            if not mirror_url:
                continue
            mirror_protocol = get_protocol(mirror_url)
            # add to mirrors
            mirrors.append({
                "country": mirror_country,
                "protocols": [mirror_protocol],
                "url": mirror_url
            })
        # write new file
        jsonfn.write_json_file(mirrors, conf.CUSTOM_FILE)
        os.remove(conf.O_CUST_FILE)


def get_protocol(data):
    """Extract protocol from url"""
    pos = data.find(":")
    return data[:pos]


def get_country(data):
    """Extract mirror country from data"""
    line = data.strip()
    if line.startswith("[") and line.endswith("]"):
        return line[1:-1]
    elif line.startswith("## Country") or line.startswith("## Location"):
        return line[19:]


def get_url(data):
    """Extract mirror url from data"""
    line = data.strip()
    if line.startswith("Server"):
        return line[9:].replace("$branch/$repo/$arch", "")
