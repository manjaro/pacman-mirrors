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

"""Pacman-Mirrors Outpout Functions"""

from pacman_mirrors.constants import txt
from pacman_mirrors.functions import fileFn
from pacman_mirrors.functions import jsonFn
from pacman_mirrors.functions import defaultPoolFn


def output_country_pool_console(self):
    """
    List all available countries
    """
    defaultPoolFn.load_default_mirror_pool(self)
    print("{}".format("\n".join(self.mirrors.country_pool)))


def output_custom_mirror_pool_file(self, selected_mirrors):
    """
    Output selected mirrors to custom mirror file
    :param self:
    :param selected_mirrors:
    :return:
    """
    print("\n.: {} {}".format(txt.INF_CLR,
                              txt.CUSTOM_MIRROR_LIST))
    print("--------------------------")
    # output mirror file
    jsonFn.write_json_file(selected_mirrors,
                           self.config["custom_file"])
    print(".: {} {}: {}".format(txt.INF_CLR,
                                txt.CUSTOM_MIRROR_FILE_SAVED,
                                self.config["custom_file"]))


def output_mirror_list(self, selected_servers):
    """
    Outputs selected servers to mirrorlist
    :param self:
    :param selected_servers:
    """
    if self.custom:
        fileFn.write_mirror_list(self.config,
                                 selected_servers,
                                 custom=self.custom,
                                 quiet=self.quiet,
                                 interactive=True)
    else:
        fileFn.write_mirror_list(self.config,
                                 selected_servers,
                                 quiet=self.quiet)

