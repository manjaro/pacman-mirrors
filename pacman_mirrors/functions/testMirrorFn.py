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

"""Pacman-Mirrors Test Mirror Functions"""

import sys

from pacman_mirrors.constants import txt, colors as color
from pacman_mirrors.functions import httpFn
from pacman_mirrors.functions import util


def test_mirrors(self, worklist):
    """
    Query server for response time
    """
    if self.custom:
        print(".: {} {}".format(txt.INF_CLR,
                                txt.USING_CUSTOM_FILE))
    else:
        print(".: {} {}".format(txt.INF_CLR,
                                txt.USING_DEFAULT_FILE))
    print(".: {} {} - {}".format(txt.INF_CLR,
                                 txt.QUERY_MIRRORS,
                                 txt.TAKES_TIME))
    cols, lines = util.terminal_size()
    # set connection timeouts
    http_wait = self.max_wait_time
    ssl_wait = self.max_wait_time * 2
    ssl_verify = self.config["ssl_verify"]
    for mirror in worklist:
        colon = mirror["url"].find(":")
        url = mirror["url"][colon:]
        for idx, proto in enumerate(mirror["protocols"]):
            mirror["url"] = "{}{}".format(proto, url)
            if not self.quiet:
                message = "   ..... {:<15}: {}".format(mirror["country"],
                                                       mirror["url"])
                print("{:.{}}".format(message, cols), end="")
                sys.stdout.flush()
            # https sometimes takes longer for handshake
            if proto == "https" or proto == "ftps":
                self.max_wait_time = ssl_wait
            else:
                self.max_wait_time = http_wait
            # let's see how responsive you are
            mirror["resp_time"] = httpFn.get_mirror_response(
                mirror["url"], maxwait=self.max_wait_time,
                quiet=self.quiet, ssl_verify=ssl_verify)

            if float(mirror["resp_time"]) >= self.max_wait_time:
                if not self.quiet:
                    print("\r")
            else:
                if not self.quiet:
                    print("\r   {:<5}{}{} ".format(color.GREEN,
                                                   mirror["resp_time"],
                                                   color.ENDCOLOR))
    return worklist

