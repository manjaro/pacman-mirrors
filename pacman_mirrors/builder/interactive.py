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

"""Pacman-Mirrors Interactive Mirror List Builder Module"""

from operator import itemgetter
from random import shuffle

from pacman_mirrors.constants import txt
from pacman_mirrors.functions import convertFn
from pacman_mirrors.functions import filterFn
from pacman_mirrors.functions import outputFn
from pacman_mirrors.functions import testMirrorFn


def build_mirror_list(self):
    """
    Prompt the user to select the mirrors with a gui.
    Outputs a "custom" mirror file
    Modify the configuration file to use the "custom" file.
    Outputs a pacman mirrorlist,
    """
    """
    Remove known bad mirrors from the list
    mirrors where status.json has -1 for last_sync or branches is -1,-1,-1
    """
    worklist = filterFn.filter_bad_mirrors(self.mirrors.mirror_pool)
    """
    It would seem reasonable to implement a filter
    based on the users branch and the mirrors update status
    On the other hand, the interactive mode is for the user
    to have total control over the mirror file.
    So though it might seem prudent to only include updated mirrors,
    we will not do it when user has selected interactive mode.
    The final mirrorfile will include all mirrors selected by the user
    The final mirrorlist will exclude (if possible) mirrors not up-to-date
    """
    worklist = filterFn.filter_mirror_country(worklist, self.selected_countries)
    """
    If config.protols has content, that is a user decision and as such
    it has nothing to do with the reasoning regarding mirrors
    which might or might not be up-to-date
    """
    try:
        _ = self.config["protocols"][0]
        worklist = filterFn.filter_mirror_protocols(
            worklist, self.config["protocols"])
    except IndexError:
        pass

    # rank or shuffle the mirrorlist before showing the ui
    if not self.default:
        if self.config["method"] == "rank":
            worklist = testMirrorFn.test_mirrors(self, worklist)
            worklist = sorted(worklist, key=itemgetter("resp_time"))
        else:
            shuffle(worklist)
    """
    Create a list for display in ui.
    The gui and the console ui expect the supplied list
    to be in the old country dictionary format.
    {
        "country": "country_name",
        "resp_time": "m.sss",
        "last_sync": "HHh MMm",
        "url": "http://server/repo/"
    }
    Therefore we have to create a list in the old format,
    thus avoiding rewrite of the ui and related functions.
    We subseqently need to translate the result into:
    a. a mirrorfile in the new json format,
    b. a mirrorlist in pacman format.
    As of version 4.8.x the last sync field contents is a string
    with the hours and minutes more human readable eg. 03h 33m
    """
    interactive_list = convertFn.translate_pool_to_interactive(worklist)
    # import the right ui
    if self.no_display:
        # in console mode
        from pacman_mirrors.dialogs import consoleui as ui
    else:
        # gobject introspection is present and accounted for
        from pacman_mirrors.dialogs import graphicalui as ui
    interactive = ui.run(interactive_list,
                         self.config["method"] == "random",
                         self.default)
    # process user choices
    if interactive.is_done:
        """
        translate interactive list back to our json format
        """
        custom_pool, mirror_list = convertFn.translate_interactive_to_pool(interactive.custom_list,
                                                                           self.mirrors.mirror_pool,
                                                                           self.config)
        """
        Try selected method on the mirrorlist
        """
        try:
            _ = mirror_list[0]
            if self.default:
                if self.config["method"] == "rank":
                    mirror_list = testMirrorFn.test_mirrors(self, mirror_list)
                    mirror_list = sorted(mirror_list, key=itemgetter("resp_time"))
                else:
                    shuffle(mirror_list)
        except IndexError:
            pass

        """
        Try to write the mirrorfile and mirrorlist
        """
        try:
            _ = custom_pool[0]
            self.custom = True
            self.config["country_pool"] = ["Custom"]
            """
            Writing the custom mirror pool file
            """
            outputFn.file_custom_mirror_pool(self, custom_pool)
            """
            Unless the user has provided the --no-status argument we only 
            write mirrors which are up-to-date for users selected branch
            """
            if self.no_status:
                pass
            else:
                mirror_list = filterFn.filter_user_branch(mirror_list, self.config)
            """
            Writing mirrorlist
            If the mirror list is empty because 
            no up-to-date mirrors exist for users branch
            raise IndexError to the outer try-catch
            """
            try:
                _ = mirror_list[0]
                outputFn.file_mirror_list(self, mirror_list)
                if self.no_status:
                    print("{} {}\n{} {}".format(txt.WRN_CLR, txt.OVERRIDE_STATUS_CHOICE,
                                                txt.WRN_CLR, txt.OVERRIDE_STATUS_MIRROR))
            except IndexError:
                raise IndexError
        except IndexError:
            print(".: {} {}".format(txt.WRN_CLR, txt.NO_SELECTION))
            print(".: {} {}".format(txt.INF_CLR, txt.NO_CHANGE))
