#!/usr/bin/env python3
"""Conversion Module"""

import json
import os
from .configuration import CUSTOM_MIRROR_FILE, CUSTOM_MIRROR_JSON


class Converter:
    @staticmethod
    def convert_custom_to_json():
        """Convert custom mirror file to json"""
        # load custom mirror file
        if os.isfile(CUSTOM_MIRROR_FILE):
            with open(CUSTOM_MIRROR_FILE, "r") as mirrorfile:
                mirrors = []
                mirror_country = ""
                for line in mirrorfile:
                    # mirror country
                    country = Function.get_country(line)
                    if country:
                        mirror_country = country
                        continue
                    mirror_url = Function.get_url(line)
                    if not mirror_url:
                        continue
                    mirror_protocol = Function.get_protocol(mirror_url)
                    mirrors.append({mirror_country: {mirror_url: {"prococols": [mirror_protocol]}}})
            Function.write_json(mirrors, CUSTOM_MIRROR_JSON)


class Function:
    @staticmethod
    def write_json(data, filename):
        """Writes a named json file"""
        try:
            with open(filename, "w") as outfile:
                json.dump(data, outfile, sort_keys=True)
            return True
        except OSError:
            return False

    @staticmethod
    def get_protocol(data):
        """Extract protocol from url"""
        pos = data.find(":")
        return data[:pos]

    @staticmethod
    def get_country(data):
        """Extract mirror country from data"""
        line = data.strip()
        if line.startswith("[") and line.endswith("]"):
            return line[1:-1]
        elif line.startswith("## Country") or line.startswith("## Location"):
            return line[19:]

    @staticmethod
    def validate_country_list(countries, available_countries):
        """Check if the list of countries are valid."""
        for country in countries:
            if country not in available_countries:
                return False
        return True

    @staticmethod
    def get_url(data):
        """Extract mirror url from data"""
        line = data.strip()
        if line.startswith("Server"):
            return line[9:]
