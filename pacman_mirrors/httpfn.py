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
    FALLBACK, MIRROR_FILE, \
    STATUS_FILE, URL_MIRROR_JSON, URL_STATUS_JSON
from .filefn import FileFn
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
    def download_mirrors(url):
        """Retrieve mirrors from manjaro.org
        :param url:
        :return: True on success
        :rtype: boolean
        """
        countries = list()
        success = False
        try:
            with urlopen(url) as response:
                countries = json.loads(response.read().decode(
                    "utf8"), object_pairs_hook=collections.OrderedDict)
        except URLError:
            print(".:> {}: {} `{}`".format(txt.ERROR, txt.ERR_DOWNLOAD_FAIL, url))
        if countries:
            success = True
            if url == URL_STATUS_JSON:
                JsonFn.write_json_file(countries, STATUS_FILE)
            else:
                JsonFn.write_json_file(countries, MIRROR_FILE)
        return success

    @staticmethod
    def check_host_online(host, count=1):
        """Check a hosts availability
        :rtype: boolean
        """
        return system_call("ping -c{} {} > /dev/null".format(count, host)) == 0

    @staticmethod
    def manjaro_online_update():
        """Checking repo.manjaro.org"""
        mjro_online = HttpFn.check_host_online("repo.manjaro.org", count=1)
        if mjro_online:
            print(".:> {}".format(txt.INF_DOWNLOAD_MIRROR_FILE))
            HttpFn.download_mirrors(URL_MIRROR_JSON)
            HttpFn.download_mirrors(URL_STATUS_JSON)
            return True
        else:
            if not FileFn.check_file(MIRROR_FILE):
                print(".:>{}: {} `{}` {}".format(txt.INFO, txt.INF_MIRROR_FILE, MIRROR_FILE, txt.INF_IS_MISSING))
                print(".:>{}: {} `{}`".format(txt.INFO, txt.INF_FALLING_BACK, FALLBACK))
            return False

    @staticmethod
    def get_mirror_response(url, timeout, count=1):
        """Query mirrors availability
        :returns string with response time
        """
        url += "state"
        probe_start = time.time()
        response_time = txt.SERVER_RES
        probe_stop = None
        _c = ""
        try:
            for _ in range(count):
                res = urlopen(url, timeout=timeout)
                _c = res.read().decode("utf8")
            probe_stop = time.time()
        except URLError:
            _c
        if probe_stop:
            calc = round((probe_stop - probe_start), 3)
            response_time = str(format(calc, ".3f"))
        return response_time
