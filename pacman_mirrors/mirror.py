#!/usr/env python3
"""Pacman-Mirrors Mirrors Module"""

from operator import itemgetter


class Mirror:
    """Pacman-Mirrors Mirrors Class"""

    def __init__(self):
        self.mirror_list = []

    def get_mirrorlist(self):
        """Returns mirrorlist"""
        return self.mirror_list

    def add_mirror(self, country, url, protocols):
        """Append mirror
        :param country:
        :param url:
        :param protocols:
        """
        mirror = {
            "country": country,
            "url": url,
            "protocols": protocols
        }
        self.mirror_list.append(mirror)

    @staticmethod
    def get_mirrors(country):
        """Return mirrors for country"""
        result = [x for x in Mirror().mirror_list if x["country"] in country]
        return result

    @staticmethod
    def initialize_mirrors(mirrors):
        """Feed mirrors into class"""
        Mirror().mirror_list = mirrors

    @staticmethod
    def sort_mirrors():
        """Returns a country sorted mirror list"""
        result = sorted(Mirror().mirror_list, key=itemgetter('country'))
        return result

    @staticmethod
    def filter_mirrors(country_list):
        """Returns mirrors for list of countries"""
        result = [x for x in Mirror().mirror_list if x["country"] in country_list]
        return result
