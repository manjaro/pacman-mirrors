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

"""Pacman-Mirrors Default Mirror Functions"""

from operator import itemgetter
from pacman_mirrors.functions import countryFn
from pacman_mirrors.functions import customFn
from pacman_mirrors.functions import fileFn


def load_all_mirrors(self):
    """
    Load all mirrors from active mirror pool
    """
    if customFn.check_custom_mirror_pool(self) and not self.config["country_pool"]:
        customFn.load_custom_mirror_pool(self)
        self.selected_countries = self.mirrors.country_pool
    else:
        if self.config["country_pool"]:
            self.selected_countries = self.config["country_pool"]
        load_default_mirror_pool(self)
    """
    Validate the list of selected countries        
    """
    self.selected_countries = countryFn.build_country_list(self.selected_countries,
                                                           self.mirrors.country_pool,
                                                           self.geoip)


def load_default_mirror_pool(self):
    """
    Load all available mirrors
    """
    (file, status) = fileFn.return_mirror_filename(self.config)
    seed_mirrors(self, file, status)


def seed_mirrors(self, file, status=False):
    """
    Seed mirrors
    """
    mirrors = fileFn.read_mirror_file(file)
    if status:
        self.mirrors.seed(mirrors, status=status)
    else:
        self.mirrors.seed(mirrors)
    sort_mirror_countries(self)


def sort_mirror_countries(self):
    self.mirrors.mirror_pool = sorted(self.mirrors.mirror_pool,
                                      key=itemgetter("country"))
    self.mirrors.country_pool = sorted(self.mirrors.country_pool)

