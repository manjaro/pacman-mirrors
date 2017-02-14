#!/usr/bin/env python3
"""Conversion Module"""

import os
from .configuration import ENV, O_CUST_FILE, CUSTOM_FILE, MIRROR_DIR
from .mirrors import Mirrors
from .filemethods import FileMethods


class CustomFile:
    @staticmethod
    def custom_to_json():
        """Convert custom mirror file to json"""
        if os.path.isfile(O_CUST_FILE):
            with open(O_CUST_FILE, "r") as mirrorfile:
                mirror = Mirrors()
                mirror_country = None
                for line in mirrorfile:
                    country = ImportHelper.get_country(line)
                    if country:
                        mirror_country = country
                        continue
                    mirror_url = ImportHelper.get_url(line)
                    if not mirror_url:
                        continue
                    mirror_protocol = ImportHelper.get_protocol(mirror_url)

                    mirror.add_mirror(mirror_country, mirror_url, [mirror_protocol])

                FileMethods.write_json(mirror.get_mirrors(), CUSTOM_FILE)
                print("TODO: change this")
                print("calling ImportHelper.cleanup()")
                # ImportHelper.cleanup()


class ImportHelper:
    @staticmethod
    def cleanup():
        os.remove(O_CUST_FILE)
        os.rmdir(os.path.dirname(O_CUST_FILE))

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
            return line[9:]
