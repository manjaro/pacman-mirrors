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
import shutil

from . import txt


def debug(where, what, value):
    """Helper for printing debug messages"""
    print("{} In function {} -> '{} = {}'".format(txt.DBG_CLR, where, what, value))


def blue(where, what, value):
    """Helper for printing blue messages"""
    print("{}In function{} >>{} \n\n{} = {}".format(txt.BS, where, txt.CE, what, value))


def green(where, what, value):
    """Helper for printing green messages"""
    print("{}In function {} >>{} \n\n{} = {}".format(txt.GS, where, txt.CE, what, value))


def red(where, what, value):
    """Helper for printing yellow messages"""
    print("{}In function {} >>{} \n\n{} = {}".format(txt.RS, where, txt.CE, what, value))


def yellow(where, what, value):
    """Helper for printing yellow messages"""
    print("{}In function {} >>{} \n\n{} = {}".format(txt.YS, where, txt.CE, what, value))


def internet_message():
    """Message when internet connection is down"""
    print(".: {} {}".format(txt.WRN_CLR, txt.INTERNET_DOWN))
    print(".: {} {}".format(txt.INF_CLR, txt.INTERNET_REQUIRED))
    print(".: {} {}".format(txt.INF_CLR, txt.MIRROR_RANKING_NA))
    print(".: {} {}".format(txt.INF_CLR, txt.INTERNET_ALTERNATIVE))


def terminal_size():
    """get terminal size"""
    # http://www.programcreek.com/python/example/85471/shutil.get_terminal_size
    cols = shutil.get_terminal_size().columns
    lines = shutil.get_terminal_size().lines
    result = (cols, lines)
    return result
