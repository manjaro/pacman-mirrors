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

"""Pacman-Mirrors Custom Pool/Mirror Functions"""

from pacman_mirrors.functions import defaultFn
from pacman_mirrors.functions import fileFn
from pacman_mirrors.functions import jsonFn
from pacman_mirrors.functions import validFn


def apply_status_to_custom_mirror_pool(config, custom_pool):
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


def check_custom_mirror_pool(self):
    """
    Custom mirror pool or countries from CLI
    :return: True/False
    """
    if validFn.custom_config_is_valid():
        self.custom = True
    else:
        self.selected_countries = self.config["country_pool"]
    return self.custom


def delete_custom_pool(self):
    """
    Delete custom mirror pool
    """
    self.custom = False
    self.config["country_pool"] = []
    fileFn.delete_file(self.config["custom_file"])


def load_custom_mirror_pool(self):
    """
    Load available custom mirrors and update their status from status.json
    If user request reset (--default) load the default pool
    """
    if self.default:
        defaultFn.load_default_mirror_pool(self)
    else:
        defaultFn.seed_mirrors(self, self.config["custom_file"])
        self.mirrors.mirror_pool = apply_status_to_custom_mirror_pool(self.config, self.mirrors.mirror_pool)

