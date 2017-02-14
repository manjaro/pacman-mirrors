#!/usr/env/python3
"""Pacman-Mirrors JSON Module"""

from collections import OrderedDict
import json
from .mirror import Mirror


class JsonFn:
    """Json Functions Class"""
    @staticmethod
    def read_json_file(filename, dictionary=False):
        """Read json data from file"""
        result = list()
        try:
            if dictionary:
                with open(filename, "rb") as infile:
                    result = json.loads(infile.read().decode(
                        "utf8"), object_pairs_hook=OrderedDict)
            else:
                with open(filename, "r") as infile:
                    result = json.load(infile)

        except OSError:
            return result
        return result

    @staticmethod
    def read_manjaro_file(filename, dictionary=False):
        """Load manjaro json file"""
        mirror = Mirror()
        if dictionary:
            countries = JsonFn.read_json_file(filename, dictionary=dictionary)
            for country in countries.keys():
                for url in countries[country]:
                    for protocols in countries[country][url]:
                        mirror.add_mirror(country, url, protocols)
            return mirror.mirrors

    @staticmethod
    def tranlate_mjro_dictionary(data):
        """Translate manjaro.json"""
        mirrors = Mirror()
        for country in data.keys():
            for url in data[country]:
                for protocols in data[country][url]:
                    mirrors.add_mirror(country, url, data[country][url][protocols])
        return mirrors.mirrors

    @staticmethod
    def write_json_file(data, filename, dictionary=False):
        """Writes data to file as json
        :param data
        :param filename:
        :param dictionary:
        """
        try:
            if dictionary:
                with open(filename, "wb") as outfile:
                    json.dump(data, outfile)
            else:
                with open(filename, "w") as outfile:
                    json.dump(data, outfile, sort_keys=True, indent=4)
            return True

        except OSError:
            return False
