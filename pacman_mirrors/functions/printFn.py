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

"""Pacman-Mirrors Print Functions"""

from pacman_mirrors.constants import colors as color


def debug_msg(where, what, value):
    """Helper for printing debug messages"""
    print("{} {} >>>> '{} = {}'".format(color.DBG_CLR, where, what, value))


def blue_msg(message):
    """Helper for printing blue messages"""
    print("{}{}{}".format(color.BLUE, message, color.ENDCOLOR))


def green_msg(message):
    """Helper for printing green messages"""
    print("{}{}{}".format(color.GREEN, message, color.ENDCOLOR))


def red_msg(message):
    """Helper for printing yellow messages"""
    print("{}{}{}".format(color.RED, message, color.ENDCOLOR))


def yellow_msg(message):
    """Helper for printing yellow messages"""
    print("{}{}{}".format(color.YELLOW, message, color.ENDCOLOR))


