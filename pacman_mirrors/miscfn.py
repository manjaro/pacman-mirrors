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
# Authors: Frede Hundewadt <frede@hundewadt.dk>

"""Pacman-Mirrors Niscellaneous Functions"""

from . import txt


def debug(where, what, value):
    """Helper for printing debug messages"""
    print("{} In function {} -> '{} = {}'".format(txt.DBG_CLR, where, what, value))


def internet_connection_message(required=False):
    """Message when internet connection is down"""
    print(".: {} {}".format(txt.INF_CLR, txt.INTERNET_DOWN))
    if required:
        print(".: {} {}".format(txt.INF_CLR, txt.INTERNET_REQUIRED))
    else:
        print(".: {} {}".format(txt.INF_CLR, txt.MIRROR_RANKING_NA))
