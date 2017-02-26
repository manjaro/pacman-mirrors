#!/usr/bin/env python
#
# This file is part of pacman-mirrors.
#
# pacman-mirrors is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pacman-mirrors is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pacman-mirrors.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Frede Hundewadt <frede@hundewadt.dk>

"""Manjaro-Mirrors HTTP Functions"""

import collections
import json
import time
from http.client import HTTPException
from os import system as system_call
from socket import timeout
from urllib.error import URLError
from urllib.request import urlopen

from .configuration import FALLBACK, MIRROR_FILE, \
    STATUS_FILE, URL_MIRROR_JSON, URL_STATUS_JSON
from . import filefn
from . import jsonfn
from . import txt


def download_mirrors(url, quiet=False):
    """Retrieve mirrors from manjaro.org
    :param url:
    :param quiet:
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
        if not quiet:
            print(".: {} {} {}".format(txt.ERROR,
                                       txt.CANNOT_DOWNLOAD_FILE,
                                       url))
    except (HTTPException, json.JSONDecodeError):
        pass

    if countries:
        success = True
        if url == URL_STATUS_JSON:
            jsonfn.write_json_file(countries, STATUS_FILE)
        else:
            jsonfn.write_json_file(countries, MIRROR_FILE)
    return success


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


def get_mirror_response(url, maxwait=2, count=1, quiet=False):
    """Query mirrors availability
    :param url:
    :param maxwait:
    :param count:
    :param quiet:
    :returns string with response time
    """
    probe_start = time.time()
    response_time = txt.SERVER_RES
    probe_stop = None
    message = ""
    try:
        for _ in range(count):
            urlopen(url, timeout=maxwait)
        probe_stop = time.time()
    except URLError as err:
        if hasattr(err, "reason"):
            message = "\n.: {} {} '{}'".format(txt.ERR_CLR,
                                               err.reason,
                                               url)
        elif hasattr(err, "code"):
            message = "\n.: {} {} '{}'".format(txt.ERR_CLR,
                                               err.reason,
                                               url)
    except timeout:
        message = "\n.: {} {} '{}'".format(txt.ERR_CLR,
                                           txt.TIMEOUT,
                                           url)
    except HTTPException:
        message = "\n.: {} {} '{}'".format(txt.ERR_CLR,
                                           txt.HTTP_EXCEPTION,
                                           url)
    if message and not quiet:
        print(message)
    if probe_stop:
        calc = round((probe_stop - probe_start), 3)
        response_time = str(format(calc, ".3f"))
    return response_time


def ping_host(host, count=1):
    """Check a hosts availability
    :param host:
    :param count:
    :rtype: boolean
    """
    return system_call("ping -c{} {} > /dev/null".format(count, host)) == 0


def update_mirrors():
    """Download updates from repo.manjaro.org"""
    mjro_online = get_mirror_response("http://repo.manjaro.org")
    if mjro_online != "99.99":
        print(".: {} {}".format(txt.INF_CLR, txt.DOWNLOADING_MIRROR_FILE))
        download_mirrors(URL_MIRROR_JSON)
        download_mirrors(URL_STATUS_JSON)
        return True
    else:
        if not filefn.check_file(MIRROR_FILE):
            print(".: {} {} {} {}".format(txt.WRN_CLR,
                                          txt.MIRROR_FILE,
                                          MIRROR_FILE,
                                          txt.IS_MISSING))
            print(".: {} {} {}".format(txt.WRN_CLR,
                                       txt.FALLING_BACK,
                                       FALLBACK))
        if not filefn.check_file(FALLBACK):
            print(".: {} {}".format(txt.ERR_CLR, txt.HOUSTON))
        return False
