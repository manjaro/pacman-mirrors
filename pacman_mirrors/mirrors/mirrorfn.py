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

"""Pacman-Mirror Mirror Functions"""

from pacman_mirrors.functions import validfn
from pacman_mirrors.functions import httpfn
from pacman_mirrors.functions import jsonfn


def build_country_list(selectedcountries, countrylist, geoip=False):
    """Do a check on the users country selection
    :param selectedcountries:
    :param countrylist:
    :param geoip:
    :return: list of valid countries
    :rtype: list
    """
    # This works so please don't touch
    result = []
    if selectedcountries:
        if selectedcountries == ["all"]:
            result = countrylist
        else:
            if validfn.country_list_is_valid(selectedcountries,
                                             countrylist):
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
    if g_country in countrylist:
        return g_country
    else:
        return None


def filter_mirror_country(mirrorlist, countrylist):
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


def filter_mirror_protocols(mirrorlist, protocols=None):
    """Return a new mirrorlist with protocols
    :type mirrorlist: list
    :type protocols: list
    :rtype: list
    """
    result = []
    if not protocols:
        return mirrorlist
    for mirror in mirrorlist:
        accepted = []
        for idx, protocol in enumerate(protocols):
            if protocol in mirror["protocols"]:
                accepted.append(protocol)
        if accepted:
            mirror["protocols"] = accepted
            result.append(mirror)
    return result


def get_custom_mirror_status(config, custom_mirrors):
    """
    Apply the current mirror status to the custom mirror file
    :param config:
    :param custom_mirrors:
    :return: custom mirrorfile with current status applied
    """
    status_list = tuple(jsonfn.read_json_file(config["status_file"], dictionary=False))
    custom_list = tuple(custom_mirrors)
    try:
        _ = status_list[0]
        for custom in custom_list:
            for status in status_list:
                if custom["url"] in status["url"]:
                    custom["last_sync"] = status["last_sync"]
                    custom["branches"] = status["branches"]
        return custom_list
    except (IndexError, KeyError):
        return custom_mirrors
