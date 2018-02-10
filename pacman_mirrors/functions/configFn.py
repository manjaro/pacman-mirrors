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

"""Pacman-Mirrors Configuration Functions"""

import sys

from pacman_mirrors.config import configuration as conf
from pacman_mirrors.constants import txt


def build_config():
    """Get config informations
    :returns: config, custom
    :rtype: tuple
    """
    custom = False
    # default config
    config = {
        "branch": "stable",
        "branches": conf.BRANCHES,
        "config_file": conf.CONFIG_FILE,
        "country_pool": [],
        "custom_file": conf.CUSTOM_FILE,
        "method": "rank",
        "work_dir": conf.WORK_DIR,
        "mirror_file": conf.MIRROR_FILE,
        "mirror_list": conf.MIRROR_LIST,
        "no_update": False,
        "protocols": [],
        "repo_arch": conf.REPO_ARCH,
        "ssl_verify": True,
        "status_file": conf.STATUS_FILE,
        "url_mirrors_json": conf.URL_MIRROR_JSON,
        "url_status_json": conf.URL_STATUS_JSON
    }
    # try to replace default entries by reading conf file
    try:
        with open(config["config_file"]) as conf_file:
            for line in conf_file:
                line = line.strip()
                if line.startswith("#") or "=" not in line:
                    continue
                (key, value) = line.split("=", 1)
                key = key.rstrip()
                value = value.lstrip()
                if key and value:
                    if value.startswith("\"") and value.endswith("\""):
                        value = value[1:-1]
                    if key == "Method":
                        config["method"] = value
                    if key == "Branch":
                        config["branch"] = value
                    if key == "Protocols":
                        if "," in value:
                            config["protocols"] = value.split(",")
                        else:
                            config["protocols"] = value.split(" ")
                    if key == "SSLVerify":
                        config["ssl_verify"] = value.lower().capitalize()

    except (PermissionError, OSError) as err:
        print(".: {} {}: {}: {}".format(txt.ERR_CLR,
                                        txt.CANNOT_READ_FILE,
                                        err.filename,
                                        err.strerror))
        sys.exit(2)
    if not verify_config(config):
        sys.exit(2)
    return config, custom


def verify_config(config):
    """
    Verify configuration
    :param config:
    """
    errors = []
    header = ".: {}: {} `{}`".format(txt.ERR_CLR,
                                     txt.INVALID_SETTING_IN,
                                     conf.CONFIG_FILE)
    if config["method"] not in conf.METHODS:
        errors.append("     'Method = {}'; {} {}".format(
            config["method"], txt.EXP_CLR, "|".join(conf.METHODS)))
    if config["branch"] not in conf.BRANCHES:
        errors.append("     'Branch = {}'; {} {}".format(
            config["branch"], txt.EXP_CLR, "|".join(conf.BRANCHES)))
    if str(config["ssl_verify"]) not in conf.SSL:
        errors.append("     'SSLVerify = {}'; {} {}".format(
            config["ssl_verify"], txt.EXP_CLR, "|".join(conf.SSL)))
    for p in config["protocols"]:
        if p not in conf.PROTOCOLS:
            errors.append("     'Protocols = {}'; {} {}".format(
                config["protocols"], txt.EXP_CLR, ",".join(conf.PROTOCOLS)))
    if len(errors):
        print(header)
        for e in errors:
            print(e)
        return False
    return True
