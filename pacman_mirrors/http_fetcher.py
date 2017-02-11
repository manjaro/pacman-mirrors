#/usr/bin/env python3
"""Manjaro-Mirrors HTTP Fetcher"""

import json
import urllib.request
from collections import OrderedDict
from http_conf import MIRRORS_URL, STATUS_URL


class HttpFetcher():
    """Http Fetcher"""

    def get_mirror_list(self):
        """Retrieve mirror list from manjaro.org"""
        mirrors = list()
        try:
            with urllib.request.urlopen(MIRRORS_URL) as response:
                mirrors = json.loads(response.read().decode(
                    "utf8"), object_pairs_hook=OrderedDict)
        except urllib.error.URLError:
            print("Error getting mirror list from server")

        return mirrors

    def get_mirrors_state(self):
        """Retrieve state for all mirrors from manjaro.org"""
        states = list()
        try:
            with urllib.request.urlopen(STATUS_URL) as response:
                states = json.loads(
                    response.read().decode(
                        "utf8"), object_pairs_hook=OrderedDict)
        except urllib.error.URLError:
            print("Error getting mirrors state from server")

        return states
