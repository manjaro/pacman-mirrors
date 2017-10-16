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

"""Pacman-Mirrors Validation Functions"""

import os
import sys

from pacman_mirrors.config import configuration as conf
from pacman_mirrors.constants import txt


def custom_config_is_valid():
    """Check validity of custom selection
    :return: True or False
    :rtype: bool
    """
    valid = os.path.isfile(conf.CUSTOM_FILE)
    if not valid:
        # validation fail - inform user and exit
        print(".: {} {} {} {}".format(txt.ERR_CLR,
                                      txt.CUSTOM_MIRROR_FILE,
                                      conf.CUSTOM_FILE,
                                      txt.DOES_NOT_EXIST))
        print(".: {} {}: {}".format(txt.INF_CLR,
                                    txt.FALLING_BACK,
                                    txt.USING_ALL_MIRRORS))
    return valid


def country_list_is_valid(onlycountry, countrylist):
    """Check if the list of countries are valid.
    :param onlycountry: list of countries to check
    :param countrylist: list of available countries
    :return: True
    :rtype: bool
    """
    for country in onlycountry:
        if country not in countrylist:
            print(".: {} {}{}: {}: '{}'".format(txt.WRN_CLR,
                                                txt.OPTION,
                                                txt.OPT_COUNTRY,
                                                txt.UNKNOWN_COUNTRY,
                                                country))
            print(".: {} {}:".format(txt.INF_CLR,
                                     txt.AVAILABLE_COUNTRIES))
            print("{}".format(", ".join(countrylist)))
            sys.exit(1)  # exit gracefully
    return True
