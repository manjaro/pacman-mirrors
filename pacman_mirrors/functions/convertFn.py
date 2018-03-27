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

"""Pacman-Mirrors Converter Functions"""

from collections import OrderedDict

from pacman_mirrors.constants import txt
from pacman_mirrors.functions import util


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
    custom_urls = set()
    custom_protocols = set()
    for custom in interactive_pool:
        try:
            """
            url without protocol
            """
            custom_url = util.get_server_location_from_url(custom["url"])
            custom_protocol = util.get_protocol_from_url(custom["url"])
            """
            locate mirror in the full mirror pool
            """
            for mirror in mirror_pool:
                try:
                    _ = mirror_pool[0]
                    mirror_url = util.get_server_location_from_url(mirror["url"])
                    if custom_url == mirror_url:
                        if custom_url not in custom_urls:
                            custom_urls.add(custom_url)
                            custom_pool.append({
                                "country": mirror["country"],
                                "protocols": mirror["protocols"],
                                "url": mirror["url"]
                            })
                        try:
                            """
                            Try to replace protocols with user selection
                            if selection exist
                            """
                            _ = config["protocols"][0]
                            mirror["protocols"] = config["protocols"]
                        except IndexError:
                            pass

                        if custom_protocol not in custom_protocols:
                            custom_protocols.add(custom_protocol)
                            mirror_list.append({
                                "country": mirror["country"],
                                "branches": mirror["branches"],
                                "protocols": mirror["protocols"],
                                "resp_time": mirror["resp_time"],
                                "last_sync": mirror["last_sync"],
                                "url": "{}{}".format(custom_protocol, mirror_url)
                            })

                except (KeyError, IndexError):
                    print(".: {} {}! {}!".format(txt.WRN_CLR, txt.HOUSTON, txt.DEFAULT_POOL_EMPTY))
                    break
                custom_protocols = set()
        except KeyError:
            print(".: {} {}! {}!".format(txt.WRN_CLR, txt.HOUSTON, txt.CUSTOM_POOL_EMPTY))
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
            last_sync = str(mirror["last_sync"]).split(":")
            mirror_url = util.get_server_location_from_url(mirror["url"])
            for idx, protocol in enumerate(mirror["protocols"]):
                interactive_list.append({
                    "country": mirror["country"],
                    "resp_time": mirror["resp_time"],
                    "last_sync": "{}h {}m".format(last_sync[0], last_sync[1]),
                    "url": "{}{}".format(protocol, mirror_url)
                })
        except (KeyError, IndexError):
            print(".: {} {}! {}!".format(txt.WRN_CLR, txt.HOUSTON, txt.MIRROR_POOL_EMPTY))
            break
    return interactive_list


