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
import fcntl
import termios
import struct
import shutil

from . import txt


def debug(where, what, value):
    """Helper for printing debug messages"""
    print("{} In function {} -> '{} = {}'".format(txt.DBG_CLR,
                                                  where,
                                                  what,
                                                  value))


def internet_message():
    """Message when internet connection is down"""
    print(".: {} {}".format(txt.WRN_CLR, txt.INTERNET_DOWN))
    print(".: {} {}".format(txt.INF_CLR, txt.INTERNET_REQUIRED))
    print(".: {} {}".format(txt.INF_CLR, txt.MIRROR_RANKING_NA))
    print(".: {} {}".format(txt.INF_CLR, txt.INTERNET_ALTERNATIVE))


def terminal_size_ll():
    # http://www.w3resource.com/python-exercises/python-basic-exercise-56.php

    th, tw, hp, wp = struct.unpack('HHHH',
                                   fcntl.ioctl(0, termios.TIOCGWINSZ,
                                               struct.pack('HHHH', 0, 0, 0, 0)))
    return tw, th


def terminal_size():
    """get terminal size"""
    c = shutil.get_terminal_size().columns
    r = shutil.get_terminal_size().rows
    result = (c, r)
    return result
