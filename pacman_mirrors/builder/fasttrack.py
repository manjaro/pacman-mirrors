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

"""Pacman-Mirrors Interactive Fasttrack list Builder"""

import sys

from operator import itemgetter
from random import shuffle


from pacman_mirrors.constants import txt, colors as color
from pacman_mirrors.functions import filterFn
from pacman_mirrors.functions import httpFn
from pacman_mirrors.functions import outputFn
from pacman_mirrors.functions import util


def build_fasttrack_mirror_list(self, number):
    """
    Fast-track the mirrorlist by filtering only up-to-date mirrors
    The function takes into account the branch selected by the user
      either on commandline or in pacman-mirrors.conf.
    The function returns a filtered list consisting of a number of mirrors
    Only mirrors from the active mirror file is used
      either mirrors.json or custom-mirrors.json
    """
    # randomize the load on up-to-date mirrors
    worklist = self.mirrors.mirror_pool
    shuffle(worklist)
    if self.config["protocols"]:
        worklist = filterFn.filter_mirror_protocols(
            worklist, self.config["protocols"])

    """
    Only pick mirrors which are up-to-date for users selected branch
      by removing not up-to-date mirrors from the list
    UP-TO-DATE FILTERING NEXT
    """
    up_to_date_mirrors = filterFn.filter_user_branch(worklist, self.config)
    worklist = []
    print(".: {}: {} - {}".format(txt.INF_CLR,
                                  txt.QUERY_MIRRORS,
                                  txt.TAKES_TIME))
    counter = 0
    cols, lines = util.terminal_size()
    for mirror in up_to_date_mirrors:
        if not self.quiet:
            message = "   ..... {:<15}: {}: {}".format(
                mirror["country"], mirror["last_sync"], mirror["url"])
            print("{:.{}}".format(message, cols), end="")
            sys.stdout.flush()
        resp_time = httpFn.get_mirror_response(mirror["url"],
                                               maxwait=self.max_wait_time,
                                               quiet=self.quiet)
        mirror["resp_time"] = resp_time
        if float(resp_time) > self.max_wait_time:
            if not self.quiet:
                print("\r")
        else:
            if not self.quiet:
                print("\r   {:<5}{}{} ".format(color.GREEN,
                                               resp_time,
                                               color.ENDCOLOR))
            worklist.append(mirror)
            counter += 1
        """
        Equality check will stop execution
        when the desired number is reached.
        In the possible event the first mirror's
        response time exceeds the predefined response time,
        the loop would stop execution if the check for zero is not present
        """
        if counter is not 0 and counter == number:
            break
    worklist = sorted(worklist,
                      key=itemgetter("resp_time"))
    """
    Try to write mirrorlist
    """
    try:
        _ = worklist[0]
        outputFn.file_mirror_list(self, worklist)
    except IndexError:
        print(".: {} {}".format(txt.WRN_CLR, txt.NO_SELECTION))
        print(".: {} {}".format(txt.INF_CLR, txt.NO_CHANGE))

