#!/usr/bin/env python3

"""Manjaro-Mirrors Local Module"""

import json
from collections import OrderedDict

MIRRORS_FILE = "/etc/pacman.d/mirrors/mirrors.json"
STATES_FILE = "/etc/pacman.d/mirrors/states.json"


class LocalModule():
    """FileHandler class"""

    def write_json(self, data, filename):
        """
        Writes a named json file

        :param data:
        :param filename:
        """
        try:
            with open(filename, "w") as outfile:
                json.dump(data, outfile)
            return True

        except OSError:
            return False

    def read_json(self, filename):
        """
        Reads a named json file

        :param filename:
        :return data: OrderedDict
        """
        result = list()
        try:
            with open(filename, "r") as infile:
                result = json.loads(infile.read().decode(
                    "utf8"), object_pairs_hook=OrderedDict)
        except OSError:
            return False

        return result
