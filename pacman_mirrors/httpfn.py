#!/usr/bin/env python3
"""Manjaro-Mirrors HTTP Module"""

import collections
import json
import time
from http.client import HTTPException
from os import system as system_call
from urllib.error import URLError
from urllib.request import urlopen
from .configuration import \
    FALLBACK, MANJARO_FILE, MIRROR_FILE, \
    STATUS_FILE, URL_MIRROR_JSON, URL_STATUS_JSON
from .jsonfn import JsonFn
from . import txt


class HttpFn:
    """Http Function Class"""

    @staticmethod
    def get_geoip_country():
        """Try to get the user country via GeoIP
        :return: country name or nothing
        """
        country_name = None
        try:
            res = urlopen("http://freegeoip.net/json/")
            json_obj = json.loads(res.read().decode("utf8"))
        except (URLError, HTTPException, json.JSONDecodeError):
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
    def get_mirrors_file():
        """Retrieve mirror list from manjaro.org
        :return: True on success
        :rtype: boolean
        """
        countries = list()
        success = False
        try:
            with urlopen(URL_MIRROR_JSON) as response:
                countries = json.loads(response.read().decode(
                    "utf8"), object_pairs_hook=collections.OrderedDict)
        except URLError:
            print("Error getting mirror list from server")
        if countries:
            success = True
            JsonFn.write_json_file(countries, MANJARO_FILE)
            translated = JsonFn.tranlate_mjro_dictionary(countries)
            JsonFn.write_json_file(translated, MIRROR_FILE)
        return success

    @staticmethod
    def get_status_file():
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
            JsonFn.write_json_file(status, STATUS_FILE)
        return success

    @staticmethod
    def host_online(host, retry):
        """Check a hosts availability
        :rtype: boolean
        """
        return system_call("ping -c{} {} > /dev/null".format(retry, host)) == 0

    @staticmethod
    def manjaro_online_update():
        """Checking repo.manjaro.org"""
        mjro_online = HttpFn.host_online("repo.manjaro.org", 1)
        if mjro_online:
            print(":: {}".format(txt.INF_DOWNLOAD_MIRROR_FILE))
            HttpFn.get_mirrors_file()
            print(":: {}".format(txt.INF_DOWNLOAD_STATUS_FILE))
            HttpFn.get_status_file()
            return True
        else:
            if not JsonFn.check_file(MIRROR_FILE):
                print(":: {} '{}' {}".format(txt.INF_MIRROR_FILE,
                                             MIRROR_FILE,
                                             txt.INF_IS_MISSING))
                print(":: {} '{}'".format(txt.INF_FALLING_BACK, FALLBACK))
            return False

    @staticmethod
    def query_mirror_available(url, timeout, retry):
        """Query mirrors availability
        :returns string with response time
        """
        url += "state"
        probe_start = time.time()
        response_time = txt.SERVER_RES
        probe_stop = None
        _c = ""
        try:
            for _ in range(retry):
                res = urlopen(url, timeout=timeout)
                _c = res.read().decode("utf8")
            probe_stop = time.time()
        except URLError:
            _c
        if probe_stop:
            calc = round((probe_stop - probe_start), 3)
            response_time = str(format(calc, ".3f"))
        return response_time
