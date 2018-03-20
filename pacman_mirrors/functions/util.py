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


import platform
import shutil

from pacman_mirrors.api import apifn
from pacman_mirrors.constants import colors as color, txt


def i686_check(self, write=False):
    if platform.machine() == "i686":
        self.config["x32"] = True
        if "x32" not in self.config["branch"]:
            self.config["branch"] = "x32-{}".format(self.config["branch"])
            if write:
                apifn.write_config_branch(self.config["branch"], self.config["config_file"], quiet=True)


def strip_protocol(url):
    """
    Splits an url
    :param url:
    :returns url string without protocol
    """
    colon = url.find(":")
    if colon:
        return url[colon:]
    return url


def debug(where, what, value):
    """Helper for printing debug messages"""
    print("{} {} >>>> '{} = {}'".format(color.DBG_CLR, where, what, value))


def blue(message):
    """Helper for printing blue messages"""
    print("{}{}{}".format(color.BLUE, message, color.ENDCOLOR))


def green(message):
    """Helper for printing green messages"""
    print("{}{}{}".format(color.GREEN, message, color.ENDCOLOR))


def red(message):
    """Helper for printing yellow messages"""
    print("{}{}{}".format(color.RED, message, color.ENDCOLOR))


def yellow(message):
    """Helper for printing yellow messages"""
    print("{}{}{}".format(color.YELLOW, message, color.ENDCOLOR))


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
