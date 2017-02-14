#!/usr/env python3
"""Pacman-Mirrors Mirrors Module"""


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


