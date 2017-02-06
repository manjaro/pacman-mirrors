#!/usr/bin/env python3
"""Manjaro Mirrors fetcher"""

import json
import urllib.request
from collections import OrderedDict
from .http_conf import MIRRORS_URL, STATUS_URL


class Fetcher():
    """HTTP Fetcher"""

    def get_mirror_list(self):
        """Get list of mirrors from manjaro.org"""
        mirrors = list()
        try:
            with urllib.request.urlopen(MIRRORS_URL) as response:
                mirrors = json.loads(response.read().decode(
                    "utf-8"), object_pairs_hook=OrderedDict)
        except urllib.error.URLError:
            print("Error getting mirror list from server")

        return mirrors

    def get_repo_states(self):
        """Get mirror states from manjaro.org"""
        states = list()
        try:
            with urllib.request.urlopen(STATUS_URL) as response:
                states = json.loads(
                    response.read().decode(
                        "utf-8"), object_pairs_hook=OrderedDict)
        except urllib.error.URLError:
            print("Error getting mirror states from server")

        return states
