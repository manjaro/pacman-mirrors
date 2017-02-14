#!/usr/env python3
"""Pacman-Mirrors Mirrors Module"""

from operator import itemgetter


class Mirror:
    """Pacman-Mirrors Mirrors Class"""

    def __init__(self):
        self.mirrors = []
        self.countries = []

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

    def seed(self, mirrors):
        """Seed mirrorlist"""
        for server in mirrors:
            self.add_mirror(server["country"],
                            server["url"],
                            server["protocols"],
                            server["branches"],
                            server["last_sync"])

    @staticmethod
    def filter_country(country):
        """Return mirrors for country
        :param country: name of country
        :return: a condensed mirror list for country
        """
        result = [x for x in Mirror().mirrorlist if x["country"] in country]
        return result

    def filter_countries(self, country_list):
        """Returns mirrors for list of countries
        :param country_list: list of countries
        :return: a condensed list with countries
        """
        print("DBEBUG >>> filter_countries -> country_list = " + str(country_list))
        result = []
        print("DBEBUG >>> filter_countries -> self.mirrors = " + str(self.mirrors))
        # result = [x for x in Mirror().mirrorlist if x["country"] in country_list]
        for mirror in self.mirrors:
            print("DBEBUG >>> filter_countries -> mirror = " + str(mirror))
            if mirror["country"] in country_list:
                result.append(mirror)
        print(str(result))
        return result

    @staticmethod
    def sort_country():
        """Returns a country sorted mirror list"""
        result = sorted(Mirror().mirrorlist, key=itemgetter('country'))
        return result

