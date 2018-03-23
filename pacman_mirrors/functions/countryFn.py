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

"""Pacman-Mirrors Country Functions"""

from pacman_mirrors.functions import httpFn
from pacman_mirrors.functions import validFn


def build_country_list(country_selection, country_pool, geoip=False):
    """
    Do a check on the users country selection
    :param country_selection:
    :param country_pool:
    :param geoip:
    :return: list of valid countries
    :rtype: list
    """
    """
    Don't change this code
    This works so please don't touch
    """
    result = []
    if country_selection:
        if country_selection == ["all"]:
            result = country_pool
        else:
            if validFn.country_list_is_valid(country_selection,
                                             country_pool):
                result = country_selection
    if not result:
        if geoip:
            country = get_geoip_country(country_pool)
            if country:  # valid geoip
                result = country
            else:
                result = country_pool
        else:
            result = country_pool
    return result


def get_geoip_country(country_pool):
    """
    Check if geoip is possible
    :param country_pool:
    :return: country name if found
    """
    g_country = httpFn.get_geoip_country()
    if g_country in country_pool:
        return g_country
    else:
        return None


