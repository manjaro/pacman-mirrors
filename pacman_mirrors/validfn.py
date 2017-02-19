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
    def is_custom_config_valid():
        """Check validity of custom selection
        :return: True or False
        :rtype: bool
        """
        if not os.path.isfile(CUSTOM_FILE):
            print(".: {} {} {} {}\n".format(txt.WRN_CLR,
                                            txt.INF_CUSTOM_MIRROR_FILE,
                                            CUSTOM_FILE,
                                            txt.INF_DOES_NOT_EXIST))
            return False  # filecheck failed
        return True  # valid

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
    def is_selection_valid(selection, countrylist):
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
                print(".: {} {}{}: '{}: {}'.\n\n".format(txt.WRN_CLR,
                                                         txt.INF_OPTION,
                                                         txt.OPT_COUNTRY,
                                                         txt.INF_UNKNOWN_COUNTRY,
                                                         country))
                exit(1)  # exit gracefully if validation fail
        return True

    @staticmethod
    def get_valid_country_list(only_country, countrylist, geoip):
        """Do a check on the users country selection
        :return: countrylist and custom flag
        :rtype: tuple
        """
        validlist = []
        custom = False
        if only_country:
            if ["Custom"] == only_country:
                if ValidFn.is_custom_config_valid():
                    custom = True

            elif ["all"] == only_country:
                validlist = countrylist  # reset to default
            else:
                if ValidFn.is_selection_valid(only_country, countrylist):
                    validlist = only_country

        if not custom:
            if geoip:
                country = ValidFn.is_geoip_valid(countrylist)
                if country:  # valid geoip
                    validlist = [country]
                else:  # validation fail
                    validlist = countrylist
            else:
                validlist = countrylist

        result = (validlist, custom)
        return result
