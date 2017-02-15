#!/usr/env python3
"""Pacman-Mirrors Mirrors Module"""

from operator import itemgetter
from random import shuffle
from . import txt


class Mirror:
    """Pacman-Mirrors Mirrors Class"""

    def __init__(self):
        self.countrylist = []
        self.mirrorlist = []

    def add(self, country, url, protocols, branches=None, last_sync="99:99", resp_time="99.99"):
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
        mirror = {
            "branches": branches,
            "country": country,
            "last_sync": last_sync,
            "protocols": protocols,
            "resp_time": resp_time,
            "url": url
        }
        self.mirrorlist.append(mirror)

    def seed(self, mirrors, status=False):
        """Seed mirrorlist
        :param mirrors:
        :param status:
        """
        for server in mirrors:
            if status:
                self.add(server["country"], server["url"], server["protocols"],
                         server["branches"], server["last_sync"])
            else:
                self.add(server["country"], server["url"], server["protocols"])
