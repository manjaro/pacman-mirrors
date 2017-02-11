#/usr/bin/env python3
"""Manjaro-Mirrors HTTP Module"""

import json
import time
from http.client import HTTPException
from socket import timeout
from urllib.error import URLError
from urllib.request import urlopen
from collections import OrderedDict
from local_module import MIRRORS_FILE, STATES_FILE, FileHandler
from . import txt

MIRRORS_URL = "http://repo.manjaro.org/new/manjaro-web-repo/mirrors.json"
STATES_URL = "http://repo.manjaro.org/new/manjaro-web-repo/docs/status.json"
BRANCHES = ("stable", "testing", "unstable")
REPO_ARCH = "$repo/$arch"


class Fetcher():
    """Fetcher Class"""

    def get_mirrors_list(self):
        """Retrieve mirror list from manjaro.org"""
        mirrors = list()
        try:
            with urlopen(MIRRORS_URL) as response:
                mirrors = json.loads(response.read().decode(
                    "utf8"), object_pairs_hook=OrderedDict)
        except URLError:
            print("Error getting mirror list from server")

        FileHandler.write_json(self, mirrors, MIRRORS_FILE)

    def get_mirrors_state(self):
        """Retrieve state for all mirrors from manjaro.org"""
        states = list()
        try:
            with urlopen(STATES_URL) as response:
                states = json.loads(
                    response.read().decode(
                        "utf8"), object_pairs_hook=OrderedDict)
        except URLError:
            print("Error getting mirrors state from server")

        FileHandler.write_json(self, states, STATES_FILE)

    def get_response_time(self, _mirror_url, _timeout, _quiet):
        """Get a mirrors response time

        :param _mirror_url: mirrors url
        :param _timeout: wait for mirror response
        :param _quiet: controls message output
        :return string: response time
        """
        probe_start = time.time()
        probe_time = txt.SERVER_RES
        try:
            urlopen(_mirror_url, timeout=_timeout)
            probe_stop = time.time()
        except URLError as err:
            probe_stop = None
            if hasattr(err, "reason") and not _quiet:
                print("\n{}: {}: {}".format(txt.ERROR,
                                            txt.ERR_SERVER_NOT_REACHABLE,
                                            err.reason))
            elif hasattr(err, "code") and not _quiet:
                print("\n{}: {}: {}".format(txt.ERROR,
                                            txt.ERR_SERVER_REQUEST,
                                            err.errno))
        except timeout:
            probe_stop = None
            if not _quiet:
                print("\n{}: {}: {}".format(txt.ERROR,
                                            txt.ERR_SERVER_NOT_AVAILABLE,
                                            txt.TIMEOUT))
        except HTTPException:
            probe_stop = None
            if not _quiet:
                print("\n{}: {}: {}".format(txt.ERROR,
                                            txt.ERR_SERVER_HTTP_EXCEPTION,
                                            txt.HTTP_EXCEPTION))
        if probe_stop:
            probe_time = round((probe_stop - probe_start), 3)
            probe_time = format(probe_time, ".3f")
        return str(probe_time)
