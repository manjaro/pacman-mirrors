#!/usr/env python3
"""Pacman-Mirrors MirrorList Module"""


class MirrorList:
    """Pacman-Mirrors MirrorLists Class"""

    def __init__(self):
        self.mirrorlist = []

    def add_country(self, country):
        """Append country"""
        self.mirrorlist.append({
            "country": country,
            "mirrors": []
        })

    def add_country_mirror(self, country, url, protocols, last_sync="99:99",
                           stable="0", testing="0", unstable="0"):
        """Append mirror
        :param country:
        :param url:
        :param protocols:
        :param last_sync:
        :param stable:
        :param testing:
        :param unstable:
        """
        mirror = {
            "mirror": url,
            "protocols": protocols,
            "last_sync": last_sync,
            "branches": {
                "stable": stable,
                "testing": testing,
                "unstable": unstable
            },
        }
        self.mirrorlist[country]["mirrors"].append(mirror)

    def get_mirrorlist(self):
        """Return mirrorlist"""
        return self.mirrorlist
