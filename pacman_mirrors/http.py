#!/usr/bin/env python3
"""Manjaro-Mirrors HTTP Module"""

import collections
import json
from http.client import HTTPException
from os import system as system_call
from urllib.error import URLError
from urllib.request import urlopen
from .configuration import URL_MIRROR_JSON, URL_STATUS_JSON, MIRROR_FILE, STATUS_FILE
from .files import Files


class Http:
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
    def get_mirrors_file():
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
            Files.write_json(mirrors, MIRROR_FILE)
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
            Files.write_json(status, STATUS_FILE)
        return success

    @staticmethod
    def host_online(host, retry):
        """Check a hosts availability
        :rtype: boolean
        """
        return system_call("ping -c{} {} > /dev/null".format(retry, host)) == 0

    @staticmethod
    def query_mirror_available(url, timeout):
        """
        Get statefile
        :param: mirror_url
        :return: content
        """
        try:
            res = urlopen(url, timeout=timeout)
            content = res.read().decode("utf8")
        except URLError:
            content = ""

        return content
