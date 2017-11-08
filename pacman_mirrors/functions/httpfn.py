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
# Authors: Frede Hundewadt <echo ZmhAbWFuamFyby5vcmcK | base64 -d>

"""Manjaro-Mirrors HTTP Functions"""

import collections
import filecmp
import json
import os
import ssl
import time
import urllib.request
from http.client import HTTPException
from os import system as system_call
from socket import timeout
from urllib.error import URLError
from urllib.request import urlopen

from pacman_mirrors import __version__
from pacman_mirrors.config import configuration as conf
from pacman_mirrors.constants import txt
from pacman_mirrors.functions import filefn
from pacman_mirrors.functions import jsonfn


def download_mirrors(config):
    """Retrieve mirrors from manjaro.org
    :param config:
    :returns: tuple with bool for mirrors.json and status.json
    :rtype: tuple
    """
    fetchmirrors = False
    fetchstatus = False
    # mirrors.json
    try:
        with urlopen(config["url_mirrors_json"]) as response:
            mirrorlist = json.loads(response.read().decode("utf8"),
                                    object_pairs_hook=collections.OrderedDict)
        fetchmirrors = True
        tempfile = config["work_dir"] + "/temp.file"
        jsonfn.json_dump_file(mirrorlist, tempfile)
        filecmp.clear_cache()
        if filefn.check_file(conf.USR_DIR, folder=True):
            if not filefn.check_file(config["mirror_file"]):
                jsonfn.json_dump_file(mirrorlist, config["mirror_file"])
            elif not filecmp.cmp(tempfile, config["mirror_file"]):
                jsonfn.json_dump_file(mirrorlist, config["mirror_file"])
        os.remove(tempfile)
    except (HTTPException, json.JSONDecodeError, URLError):
        pass
    # status.json
    try:
        with urlopen(config["url_status_json"]) as response:
            statuslist = json.loads(
                response.read().decode("utf8"),
                object_pairs_hook=collections.OrderedDict)
        fetchstatus = True
        jsonfn.write_json_file(statuslist, config["status_file"])
    except (HTTPException, json.JSONDecodeError, URLError):
        pass
    # result
    return fetchmirrors, fetchstatus


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


def get_mirror_response(url, maxwait=2, count=1, quiet=False, ssl_verify=True):
    """Query mirrors availability
    :param ssl_verify:
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
    # context = None
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    headers = {"User-Agent": "pacman-mirrors {}".format(__version__)}
    if not ssl_verify:
        # context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(
        url + "state", headers=headers
    )
    # noinspection PyBroadException
    try:
        for _ in range(count):
            urlopen(req, timeout=maxwait, context=context)
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
    except ssl.CertificateError:
        message = "\n.: {} {} '{}'".format(txt.ERR_CLR,
                                           ssl.CertificateError,
                                           url)
    if message and not quiet:
        print(message)
    if probe_stop:
        calc = round((probe_stop - probe_start), 3)
        response_time = str(format(calc, ".3f"))
    return response_time


def inet_conn_check(maxwait=2):
    """Check for internet connection"""
    data = None
    hosts = conf.INET_CONN_CHECK_URLS
    for host in hosts:
        # noinspection PyBroadException
        try:
            data = urlopen(host, timeout=maxwait)
            break
        except:
            pass
    return bool(data)


def ping_host(host, count=1):
    """Check a hosts availability
    :param host:
    :param count:
    :rtype: boolean
    """
    print(".: {} ping {} x {}".format(txt.INF_CLR, host, count))
    return system_call("ping -c{} {} > /dev/null".format(count, host)) == 0


def update_mirrors(config, quiet=False):
    """Download updates from repo.manjaro.org
    :param config:
    :param quiet:
    :returns: tuple with result for mirrors.json and status.json
    :rtype: tuple
    """
    # one fallback file in /usr/share/pacman-mirrors should be enough.
    # the mirrors.json in /var/lib/pacman-mirrors is confusing.
    # so remove it
    if filefn.check_file(config["to_be_removed"]):
        os.remove(config["to_be_removed"])
    result = None
    connected = inet_conn_check()
    if connected:
        if not quiet:
            print(".: {} {} {}".format(txt.INF_CLR,
                                       txt.DOWNLOADING_MIRROR_FILE,
                                       txt.REPO_SERVER))
        result = download_mirrors(config)
    else:
        if not filefn.check_file(config["status_file"]):
            if not quiet:
                print(".: {} {} {} {}".format(txt.WRN_CLR,
                                              txt.MIRROR_FILE,
                                              config["status_file"],
                                              txt.IS_MISSING))
                print(".: {} {} {}".format(txt.WRN_CLR,
                                           txt.FALLING_BACK,
                                           conf.MIRROR_FILE))
            result = (True, False)
        if not filefn.check_file(config["mirror_file"]):
            if not quiet:
                print(".: {} {}".format(txt.ERR_CLR, txt.HOUSTON))
            result = (False, False)
    return result
