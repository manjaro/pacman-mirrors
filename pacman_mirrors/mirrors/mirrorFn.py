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

from pacman_mirrors.constants import txt
from pacman_mirrors.config import configuration as conf
from pacman_mirrors.functions import validFn
from pacman_mirrors.functions import httpFn
from pacman_mirrors.functions import jsonFn
from pacman_mirrors.functions import util


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


def filter_user_branch(mirror_pool, config):
    """
    Filter mirrorlist on users branch and branch sync state
    """
    for idx, branch in enumerate(conf.BRANCHES):
        if config["x32"]:
            config_branch = config["branch"][4:]
        else:
            config_branch = config["branch"]
        if branch == config_branch:
            filtered = []
            for mirror in mirror_pool:
                try:
                    if mirror["branches"][idx] == 1:
                        filtered.append(mirror)
                except IndexError:
                    pass
            if len(filtered) > 0:
                return filtered
    return mirror_pool


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


def translate_interactive_to_pool(interactive_pool, mirror_pool, config):
    """
    Translate mirror pool for interactive display
    :param interactive_pool:
    :param mirror_pool:
    :param config:
    :return:
    """
    custom_pool = []
    mirror_list = []
    for custom in interactive_pool:
        """
        url without protocol
        """
        try:

            custom_url = util.strip_protocol(custom["url"])
            """
            locate mirror in the full mirror pool
            """
            for mirror in mirror_pool:
                try:
                    _ = mirror_pool[0]
                    mirror_url = util.strip_protocol(mirror["url"])
                    if custom_url == mirror_url:
                        custom_pool.append({
                            "country": mirror["country"],
                            "protocols": mirror["protocols"],
                            "url": mirror["url"]
                        })
                        try:
                            """
                            Try to replace protocols with user selection
                            """
                            _ = config["protocols"][0]
                            mirror["protocols"] = config["protocols"]
                        except IndexError:
                            pass
                        mirror_list.append(mirror)
                except (KeyError, IndexError):
                    print("{} {}\n"
                          "\tIn (mirrorFn.translate_interactive_to_pool -> inner Loop)".format(txt.WRN_CLR,
                                                                                               txt.HOUSTON))
                    break
        except KeyError:
            print("{} {}\n"
                  "\tIn (mirrorFn.translate_interactive_to_pool -> outer Loop)".format(txt.WRN_CLR,
                                                                                       txt.HOUSTON))
            break
    return custom_pool, mirror_list


def translate_pool_to_interactive(mirror_pool):
    """
    Translate mirror pool for interactive display
    :param mirror_pool:
    :return: list of dictionaries
            {
                "country": "country_name",
                "resp_time": "m.sss",
                "last_sync": "HH:MM",
                "url": "http://server/repo/"
            }
    """
    interactive_list = []
    for mirror in mirror_pool:
        try:
            _ = mirror_pool[0]
            # create an entry for all protocols related to a mirror
            for protocol in mirror["protocols"]:
                interactive_list.append({
                    "country": mirror["country"],
                    "resp_time": mirror["resp_time"],
                    "last_sync": "{}h {}m".format(mirror["last_sync"][:2].replace(":", ""),
                                                  mirror["last_sync"][2:].replace(":", "")),
                    "url": "{}{}".format(protocol[1], util.strip_protocol(mirror["url"]))
                })
        except (KeyError, IndexError):
            print("{} {}\n"
                  "\tIn (mirrorFn.translate_pool_to_interactive)".format(txt.WRN_CLR, txt.HOUSTON))
            break
    return interactive_list


