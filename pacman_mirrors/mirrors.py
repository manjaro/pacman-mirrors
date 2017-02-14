#!/usr/env python3
"""Pacman-Mirrors Mirrors Module"""

from .files import Files


class Mirrors:
    """Pacman-Mirrors Mirrors Class"""

    def __init__(self):
        self.mirrors = []

    def add_mirror(self, country, url, protocols):
        """Append mirror
        :param country:
        :param url:
        :param protocols:
        """
        mirror = {
            "country": country,
            "url": url,
            "protocols": protocols,
            "lastsync": "",
            "resptime": ""
        }
        self.mirrors.append(mirror)

    def get_mirrors(self):
        """Return mirrorlist"""
        return self.mirrors

    def load_mjro_json(self, filename):
        """Load manjaro mirrors from file"""
        countries = Files.read_json(filename)

        for country in countries:
            for host in country:
                url = host[0]
                protocols = host["protocols"]
            print("country:" + country)
            print("url:" + url)
            print("protocols:" + protocols)
            self.add_mirror(country, url, protocols)

