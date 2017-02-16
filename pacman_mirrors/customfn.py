#!/usr/bin/env python3
"""Conversion Module"""

import os
from .configuration import ENV, O_CUST_FILE, CUSTOM_FILE
from .jsonfn import JsonFn
from . import txt


class CustomFn:
    @staticmethod
    def convert_to_json():
        """Convert custom mirror file to json"""
        if os.path.isfile(O_CUST_FILE):
            print(".:> {}".format(txt.INF_CONVERT_MIRROR_FILE))
            mirrors = []
            with open(O_CUST_FILE, "r") as mirrorfile:
                mirror_country = None
                for line in mirrorfile:
                    country = CustomHelper.get_country(line)
                    if country:
                        mirror_country = country
                        continue
                    mirror_url = CustomHelper.get_url(line)
                    if not mirror_url:
                        continue
                    mirror_protocol = CustomHelper.get_protocol(mirror_url)
                    # add to mirrors
                    mirrors.append({
                        "country": mirror_country,
                        "protocols": [mirror_protocol],
                        "url": mirror_url
                    })
                # write new file
                JsonFn.write_json_file(mirrors, CUSTOM_FILE)
                # TODO: remove env check
                if not ENV:
                    CustomHelper.cleanup()


class CustomHelper:
    @staticmethod
    def cleanup():
        os.remove(O_CUST_FILE)

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
    def get_url(data):
        """Extract mirror url from data"""
        line = data.strip()
        if line.startswith("Server"):
            return line[9:].replace("$branch/$repo/$arch", "")
