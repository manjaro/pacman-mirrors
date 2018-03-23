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

"""Pacman-Mirrors Utility Functions"""


import platform
import shutil

from pacman_mirrors.api import apifn
from pacman_mirrors.constants import txt


def extract_mirror_url(data):
    """Extract mirror url from data"""
    line = data.strip()
    if line.startswith("Server"):
        return line[9:].replace("$branch/$repo/$arch", "")


def get_country(data):
    """Extract mirror country from data"""
    line = data.strip()
    if line.startswith("[") and line.endswith("]"):
        return line[1:-1]
    elif line.startswith("## Country") or line.startswith("## Location"):
        return line[19:]


def get_protocol(data):
    """Extract protocol from url"""
    pos = data.find(":")
    return data[:pos]


def get_protocol_from_url(url):
    """
    Splits an url
    :param url:
    :returns protocol eg. http
    """
    colon = url.find(":")
    if colon:
        return url[:colon]
    return url


def get_server_location_from_url(url):
    """
    Splits an url
    :param url:
    :returns url string without protocol
    """
    colon = url.find(":")
    if colon:
        return url[colon:]
    return url


def i686_check(self, write=False):
    if platform.machine() == "i686":
        self.config["x32"] = True
        if "x32" not in self.config["branch"]:
            self.config["branch"] = "x32-{}".format(self.config["branch"])
            if write:
                apifn.write_config_branch(self.config["branch"], self.config["config_file"], quiet=True)


def internet_message():
    """Message when internet connection is down"""
    print(".: {} {}".format(txt.WRN_CLR, txt.INTERNET_DOWN))
    print(".: {} {}".format(txt.INF_CLR, txt.MIRROR_RANKING_NA))
    print(".: {} {}".format(txt.INF_CLR, txt.INTERNET_ALTERNATIVE))


def terminal_size():
    """get terminal size"""
    # http://www.programcreek.com/python/example/85471/shutil.get_terminal_size
    cols = shutil.get_terminal_size().columns
    lines = shutil.get_terminal_size().lines
    result = (cols, lines)
    return result
