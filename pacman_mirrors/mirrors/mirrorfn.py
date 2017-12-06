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

from pacman_mirrors.functions import validFn
from pacman_mirrors.functions import httpFn
from pacman_mirrors.functions import jsonFn


def build_country_list(country_selection, country_pool, geoip=False):
    """
    Do a check on the users country selection
    :param country_selection:
    :param country_pool:
    :param geoip:
    :return: list of valid countries
    :rtype: list
    """
    # This works so please don't touch
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


def filter_mirror_country(mirror_pool, country_pool):
    """
    Return new mirror pool with selected countries
    :param mirror_pool:
    :param country_pool:
    :rtype: list
    """
    result = []
    for mirror in mirror_pool:
        if mirror["country"] in country_pool:
            result.append(mirror)
    return result


def filter_mirror_protocols(mirror_pool, protocols=None):
    """
    Return a new mirrorlist with protocols
    :type mirror_pool: list
    :type protocols: list
    :rtype: list
    """
    result = []
    if not protocols:
        return mirror_pool
    for mirror in mirror_pool:
        accepted = []
        for idx, protocol in enumerate(protocols):
            if protocol in mirror["protocols"]:
                accepted.append(protocol)
        if accepted:
            mirror["protocols"] = accepted
            result.append(mirror)
    return result


def set_custom_mirror_status(config, custom_pool):
    """
    Apply the current mirror status to the custom mirror file
    :param config: config dictionary
    :param custom_pool: the custom mirror pool
    :return: custom mirror pool with status applied
    """
    status_list = tuple(jsonFn.read_json_file(config["status_file"], dictionary=False))
    custom_list = tuple(custom_pool)
    try:
        _ = status_list[0]
        for custom in custom_list:
            for status in status_list:
                if custom["url"] in status["url"]:
                    custom["last_sync"] = status["last_sync"]
                    custom["branches"] = status["branches"]
        return list(custom_list)
    except (IndexError, KeyError):
        return custom_pool
