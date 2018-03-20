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

"""Pacman-Mirrors Filter Functions"""

from pacman_mirrors.config import configuration as conf


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


