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

"""Pacman-Mirror Mirror Functions"""

from . import httpfn
from . import validfn


def build_country_list(selectedcountries, countrylist, geoip=False):
    """Do a check on the users country selection
    :param selectedcountries:
    :param countrylist:
    :param geoip:
    :return: list of valid countries
    :rtype: list
    """
    result = []
    if selectedcountries:
        if selectedcountries == ["all"]:
            result = countrylist
        else:
            if validfn.country_list_is_valid(selectedcountries, countrylist):
                result = selectedcountries
    if not result:
        if geoip:
            country = get_geoip_country(countrylist)
            if country:  # valid geoip
                result = country
            else:
                result = countrylist
        else:
            result = countrylist
    return result


def get_geoip_country(countrylist):
    """Check if geoip is possible
    :param countrylist:
    :return: country name if found
    """
    g_country = httpfn.get_geoip_country()
    if validfn.country_is_in_countrylist(g_country, countrylist):
        return g_country
    else:
        return None


def filter_mirror_list(mirrorlist, countrylist):
    """Return new list with selection
    :param mirrorlist:
    :param countrylist:
    :rtype: list
    """

    result = []
    for mirror in mirrorlist:
        if mirror["country"] in countrylist:
            result.append(mirror)
    return result
