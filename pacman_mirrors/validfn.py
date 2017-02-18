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

"""Pacman-Mirrors Validation Functions"""

import os
from .configuration import CUSTOM_FILE
from .httpfn import HttpFn
from . import txt


class ValidFn:
    """Validation Functions"""

    @staticmethod
    def is_custom_conf_valid(only_country):
        """Check validity of custom selection
        :param only_country:
        :return: True or False
        :rtype: bool
        """
        if only_country == ["Custom"]:
            if not os.path.isfile(CUSTOM_FILE):
                print(".: {} {} {} {}\n".format(txt.WRN_CLR,
                                                txt.INF_CUSTOM_MIRROR_FILE,
                                                CUSTOM_FILE,
                                                txt.INF_DOES_NOT_EXIST))
                return False  # filecheck failed
            return True  # valid
        return False  # not valid

    @staticmethod
    def is_geoip_valid(country_list):
        """Check if geoip is possible
        :param country_list:
        :return: country name if found
        """
        geoip_country = HttpFn.get_geoip_country()
        if geoip_country and geoip_country in country_list:
            return geoip_country
        else:
            return None

    @staticmethod
    def is_list_valid(selection, countrylist):
        """Check if the list of countries are valid.
        :param selection: list of countries to check
        :param countrylist: list of available countries
        :return: True or False
        :rtype: bool
        """
        if selection == "all":
            return True
        for country in selection:
            if country not in countrylist:
                print(".: {} {}{}: '{}: {}'.\n\n{}".format(txt.WRN_CLR,
                                                           txt.INF_OPTION,
                                                           txt.OPT_COUNTRY,
                                                           txt.INF_UNKNOWN_COUNTRY,
                                                           country,
                                                           txt.INF_USING_ALL_SERVERS))
                return False
        return True

