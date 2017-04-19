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

"""Pacman-Mirrors JSON Functions"""

import collections
import json


def json_dump_file(data, filename):
    with open(filename, "w") as outfile:
        json.dump(data, outfile)


def read_json_file(filename, dictionary=True):
    """Read json data from file"""
    result = list()
    try:
        if dictionary:
            with open(filename, "rb") as infile:
                result = json.loads(
                    infile.read().decode("utf8"),
                    object_pairs_hook=collections.OrderedDict)
        else:
            with open(filename, "r") as infile:
                result = json.load(infile)
    except OSError:
        pass
    return result


def write_json_file(data, filename, dictionary=False):
    """Writes data to file as json
    :param data
    :param filename:
    :param dictionary:
    """
    try:
        if dictionary:
            with open(filename, "wb") as outfile:
                json.dump(data, outfile)
        else:
            with open(filename, "w") as outfile:
                json.dump(data, outfile, sort_keys=True, indent=4)
        return True
    except OSError:
        return False
