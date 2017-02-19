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
# Authors: Frede Hundewadt <frede@hundewadt.dk>

"""Pacman-Mirrors Mirror"""


class Mirror:
    """Mirror Class"""

    def __init__(self):
        self.countrylist = []
        self.mirrorlist = []

    def add(self, country, url, protocols, branches=None, last_sync="00:00", resp_time="00.00"):
        """Append mirror
        :param country:
        :param url:
        :param protocols:
        :param branches: optional from status.json
        :param last_sync: optional from status.json
        :param resp_time: optional from status.json
        """
        if branches is None:
            branches = [0, 0, 0]
        if country not in self.countrylist:
            self.countrylist.append(country)
        # translate negative integer in status.json
        if last_sync == -1:
            last_sync = "9999:99"
            resp_time = "9999.99"
        mirror = {
            "branches": branches,
            "country": country,
            "last_sync": last_sync,
            "protocols": protocols,
            "resp_time": resp_time,
            "url": url
        }
        self.mirrorlist.append(mirror)

    def seed(self, mirrors, status=False, custom=False):
        """Seed mirrorlist
        :param mirrors:
        :param status:
        :param custom:
        """
        if custom:  # clear previous data
            self.countrylist = []
            self.mirrorlist = []
        for server in mirrors:
            if status:
                self.add(server["country"], server["url"], server["protocols"],
                         server["branches"], server["last_sync"])
            else:
                self.add(server["country"], server["url"], server["protocols"])
