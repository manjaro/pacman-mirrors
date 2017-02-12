#!/usr/bin/env python3
"""Manjaro-Mirrors HTTP Module"""

import json
import time
import urllib.error
import urllib.request
import collections
from .configuration import MIRRORS_URL, STATES_URL, MIRRORS_JSON, STATES_JSON
from .local_module import FileHandler
from . import txt


class Fetcher():
    """Fetcher Class"""

    @staticmethod
    def get_mirrors_list():
        """Retrieve mirror list from manjaro.org"""
        mirrors = list()
        try:
            with urllib.request.urlopen(MIRRORS_URL) as response:
                mirrors = json.loads(response.read().decode(
                    "utf8"), object_pairs_hook=collections.OrderedDict)
        except URLError:
            print("Error getting mirror list from server")
        if mirrors:
            print(mirrors)
            FileHandler.write_json(mirrors, MIRRORS_JSON)

    @staticmethod
    def get_mirrors_state():
        """Retrieve state for all mirrors from manjaro.org"""
        states = list()
        try:
            with urllib.request.urlopen(STATES_URL) as response:
                states = json.loads(
                    response.read().decode(
                        "utf8"), object_pairs_hook=collections.OrderedDict)
        except URLError:
            print("Error getting mirrors state from server")
        if states:
            FileHandler.write_json(states, STATES_JSON)

    @staticmethod
    def get_response_time(mirror_url, timeout, quiet):
        """Get a mirrors response time

        :param mirror_url: mirrors url
        :param timeout: wait for mirror response
        :param quiet: controls message output
        :return string: response time
        """
        probe_start = time.time()
        probe_time = txt.SERVER_RES
        try:
            urllib.request.urlopen(mirror_url, timeout=timeout)
            probe_stop = time.time()
        except urllib.request.URLError as err:
            probe_stop = None
            if hasattr(err, "reason") and not quiet:
                print("\n{}: {}: {}".format(txt.ERROR,
                                            txt.ERR_SERVER_NOT_REACHABLE,
                                            err.reason))
            elif hasattr(err, "code") and not quiet:
                print("\n{}: {}: {}".format(txt.ERROR,
                                            txt.ERR_SERVER_REQUEST,
                                            err.errno))
        except timeout:
            probe_stop = None
            if not quiet:
                print("\n{}: {}: {}".format(txt.ERROR,
                                            txt.ERR_SERVER_NOT_AVAILABLE,
                                            txt.TIMEOUT))
        except HTTPException:
            probe_stop = None
            if not quiet:
                print("\n{}: {}: {}".format(txt.ERROR,
                                            txt.ERR_SERVER_HTTP_EXCEPTION,
                                            txt.HTTP_EXCEPTION))
        if probe_stop:
            probe_time = round((probe_stop - probe_start), 3)
            probe_time = format(probe_time, ".3f")
        return str(probe_time)
