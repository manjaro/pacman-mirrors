#!/usr/bin/env python3
"""Pacman-Mirrors Validation Module"""

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
                print(".:> {}: {} '{} {}'\n".format(
                    txt.WARN, txt.INF_CUSTOM_MIRROR_FILE, CUSTOM_FILE, txt.INF_DOES_NOT_EXIST))
                return False
        return True

    @staticmethod
    def is_geoip_valid(country_list):
        """Check if geoip is possible
        :param country_list:
        :return: country name if found
        """
        geoip_country = HttpFn.get_geoip_country()
        if geoip_country and geoip_country in country_list:
            return [geoip_country]
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
        for country in selection:
            if country not in countrylist:
                print(".:>{}: {}{}: '{}: {}'.\n\n{}".format(txt.INFO, txt.INF_OPTION, txt.OPT_COUNTRY,
                                                            txt.INF_UNKNOWN_COUNTRY, country,
                                                            txt.INF_USING_ALL_SERVERS))
                return False
        return True

