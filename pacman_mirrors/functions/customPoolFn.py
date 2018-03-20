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

"""Pacman-Mirrors Custom Pool Functions"""

from pacman_mirrors.functions import customMirrorFn
from pacman_mirrors.functions import defaultMirrorFn
from pacman_mirrors.functions import defaultPoolFn
from pacman_mirrors.functions import fileFn
from pacman_mirrors.functions import validFn


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
    If user request the default mirror pool load the default pool
    """
    if self.default:
        defaultPoolFn.load_default_mirror_pool(self)
    else:
        defaultMirrorFn.seed_mirrors(self, self.config["custom_file"])
        self.mirrors.mirror_pool = customMirrorFn.set_custom_mirror_status(
            self.config, self.mirrors.mirror_pool)
