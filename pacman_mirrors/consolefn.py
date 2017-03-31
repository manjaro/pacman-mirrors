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

"""Pacman-Mirrors Console Functions"""

import json


def list_to_tuple(list_data, named_tuple):
    """
    Comvert list to a list with named tuples
    :param list_data: the list to convert
    :param named_tuple: tuple list item converts to
    :return data: list of named tuples
    """
    tdata = json.dumps(list_data)
    data = json.loads(tdata, object_hook=lambda x: named_tuple(**x))
    return data


def rows_from_tuple(servers, joiner=" | "):
    """
    Generates equal formatted lines
    :param servers: named tuples
    :param joiner: string used to join tuple items
    :return lines: list of nicely formatted lines
    """
    rows = []
    if servers:
        # calculate max col width
        col_width = [max(len(text) for text in col) for col in zip(*servers)]

        # generate lines
        for line in servers:
            rows.append(joiner.join("{:{}}".format(text, col_width[i])
                                    for i, text in enumerate(line)))
    return rows
