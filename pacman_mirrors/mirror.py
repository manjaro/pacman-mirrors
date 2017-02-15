#!/usr/env python3
"""Pacman-Mirrors Mirrors Module"""

from operator import itemgetter


class Mirror:
    """Pacman-Mirrors Mirrors Class"""

    mirrors = []
    countries = []

    @property
    def mirrorlist(self):
        """Returns mirrorlist"""
        return self.mirrors

    @property
    def countrylist(self):
        for country in self.mirrors:
            self.countries.append(country["country"])
        return self.countries

    def add_mirror(self, country, url, protocols, branches=None, last_sync="99:99", resp_time="99.99"):
        """Append mirror
        :param country:
        :param url:
        :param protocols:
        :param branches:
        :param last_sync:
        :param resp_time:
        """
        if branches is None:
            branches = []
        mirror = {
            "country": country,
            "url": url,
            "protocols": protocols,
            "branches": branches,
            "last_sync": last_sync,
            "resp_time": resp_time
        }
        self.mirrors.append(mirror)

    def seed(self, mirrors, status=False):
        """Seed mirrorlist"""
        for server in mirrors:
            if status:
                self.add_mirror(server["country"],
                                server["url"],
                                server["protocols"],
                                server["branches"],
                                server["last_sync"])
            else:
                self.add_mirror(server["country"],
                                server["url"],
                                server["protocols"])

    def filter(self, selection):
        """Returns mirrors for country selection
        :param selection: list of country names
        :return: a condensed list with countries
        """
        result = []
        for mirror in self.mirrors:
            if mirror["country"] in selection:
                result.append(mirror)
        print(str(result))
        return result

    @staticmethod
    def sort_country(mirrors):
        """Returns a country sorted mirror list"""
        result = sorted(mirrors, key=itemgetter('country'))
        return result

    @staticmethod
    def sort_response(mirrors):
        """Returns a country sorted mirror list"""
        result = sorted(mirrors, key=itemgetter('resp_time'))
        return result
