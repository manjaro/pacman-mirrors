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

"""Pacman-Mirrors Common Mirror list Builder"""

from operator import itemgetter
from random import shuffle

from pacman_mirrors.constants import txt
from pacman_mirrors.functions import filterFn
from pacman_mirrors.functions import outputFn
from pacman_mirrors.functions import testMirrorFn


def build_common_mirror_list(self):
    """
    Generate common mirrorlist
    """
    """
    Create a list based on the content of selected_countries
    """
    mirror_selection = filterFn.filter_mirror_country(self.mirrors.mirror_pool,
                                                      self.selected_countries)
    """
    Check the length of selected_countries against the full countrylist
    If selected_countries is the lesser then we build a custom pool file
    """
    if len(self.selected_countries) < len(self.mirrors.country_pool):
        try:
            _ = self.selected_countries[0]
            outputFn.output_custom_mirror_pool_file(self, mirror_selection)
        except IndexError:
            pass
    """
    Prototol filtering if applicable
    """
    try:
        _ = self.config["protocols"][0]
        mirror_selection = filterFn.filter_mirror_protocols(
            mirror_selection, self.config["protocols"])
    except IndexError:
        pass

    """
    only list mirrors which are up-to-date for users selected branch
    by removing not up-to-date mirrors from the list
    UP-TO-DATE FILTERING NEXT
    """
    mirror_selection = filterFn.filter_user_branch(mirror_selection, self.config)

    if self.config["method"] == "rank":
        mirror_selection = testMirrorFn.test_mirrors(self, mirror_selection)
        mirror_selection = sorted(mirror_selection,
                                  key=itemgetter("resp_time"))
    else:
        shuffle(mirror_selection)

    """
    Try to write mirrorlist
    """
    try:
        _ = mirror_selection[0]
        outputFn.output_mirror_list(self, mirror_selection)
        if self.custom:
            print(".: {} {} 'sudo {}'".format(txt.INF_CLR,
                                              txt.REMOVE_CUSTOM_CONFIG,
                                              txt.RESET_ALL))
    except IndexError:
        print(".: {} {}".format(txt.WRN_CLR, txt.NO_SELECTION))
        print(".: {} {}".format(txt.INF_CLR, txt.NO_CHANGE))

