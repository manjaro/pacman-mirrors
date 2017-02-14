#!/usr/bin/env python3
"""Manjaro-Mirrors HTTP Module"""

import json
import time
from http.client import HTTPException
from urllib.error import URLError
from urllib.request import urlopen
import collections
from .configuration import URL_MIRROR_JSON, URL_STATUS_JSON, MIRROR_FILE, STATUS_FILE
from .filemethods import FileMethods
from . import txt


class HttpFetcher:
    """HttpFetcher Class"""

    @staticmethod
    def get_geoip_country(timeout=2):
        """Try to get the user country via GeoIP
        :param timeout:
        :return: country name or nothing
        """
        country_name = None
        try:
            res = urlopen("http://freegeoip.net/json/", timeout)
            json_obj = json.loads(res.read().decode("utf8"))
        except (URLError, timeout, HTTPException, json.JSONDecodeError):
            pass
        else:
            if "country_name" in json_obj:
                country_name = json_obj["country_name"]
                country_fix = {
                    "Brazil": "Brasil",
                    "Costa Rica": "Costa_Rica",
                    "Czech Republic": "Czech",
                    "South Africa": "Africa",
                    "United Kingdom": "United_Kingdom",
                    "United States": "United_States",
                }
                if country_name in country_fix.keys():
                    country_name = country_fix[country_name]
        return country_name

    @staticmethod
    def download_mirrors():
        """Retrieve mirror list from manjaro.org
        :return: True on success
        :rtype: boolean
        """
        mirrors = list()
        success = False
        try:
            with urlopen(URL_MIRROR_JSON) as response:
                mirrors = json.loads(response.read().decode(
                    "utf8"), object_pairs_hook=collections.OrderedDict)
        except URLError:
            print("Error getting mirror list from server")
        if mirrors:
            success = True
            FileMethods.write_json(mirrors, MIRROR_FILE)
        return success

    @staticmethod
    def download_status():
        """Retrieve state for all mirrors from manjaro.org
        :return: True on success
        :rtype: boolean
        """
        status = list()
        success = False
        try:
            with urlopen(URL_STATUS_JSON) as response:
                status = json.loads(
                    response.read().decode(
                        "utf8"), object_pairs_hook=collections.OrderedDict)
        except URLError:
            print("Error getting mirrors state from server")
        if status:
            success = True
            FileMethods.write_json(status, STATUS_FILE)
        return success

    @staticmethod
    def get_response_time(mirror_url, timeout=2, quiet=False):
        """Get a mirrors response time
        :param mirror_url: mirrors url
        :param timeout: wait for mirror response
        :param quiet: controls message output
        :return: response time
        :rtype: string
        """
        probe_start = time.time()
        probe_time = txt.SERVER_RES  # default probe_time
        probe_stop = None
        try:
            # dont use ping - try open url in stead
            # open 3 times to get an average response time
            urlopen(mirror_url, timeout)
            urlopen(mirror_url, timeout)
            urlopen(mirror_url, timeout)
            probe_stop = time.time()
        except URLError as err:
            if hasattr(err, "reason") and not quiet:
                print("\n{}: {}: {}".format(txt.ERROR,
                                            txt.ERR_SERVER_NOT_REACHABLE,
                                            err.reason))
            elif hasattr(err, "code") and not quiet:
                print("\n{}: {}: {}".format(txt.ERROR,
                                            txt.ERR_SERVER_REQUEST,
                                            err.errno))
        except timeout:
            if not quiet:
                print("\n{}: {}: {}".format(txt.ERROR,
                                            txt.ERR_SERVER_NOT_AVAILABLE,
                                            txt.TIMEOUT))
        except HTTPException:
            if not quiet:
                print("\n{}: {}: {}".format(txt.ERROR,
                                            txt.ERR_SERVER_HTTP_EXCEPTION,
                                            txt.HTTP_EXCEPTION))
        if probe_stop:
            probe_time = (round((probe_stop - probe_start), 3) / 3)
            probe_time = format(probe_time, ".3f")
        return str(probe_time)
