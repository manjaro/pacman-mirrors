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

"""Pacman-Mirrors Configuration Functions"""

import os
import sys
import tempfile

from . import txt
from . import configuration as conf


def api_write_branch(branch, filename):
    """Write branch"""
    if branch == "stable":
        branch = "# Branch = stable\n"
    else:
        branch = "Branch = {}\n".format(branch)
    try:
        with open(
            filename) as cnf, tempfile.NamedTemporaryFile(
            "w+t", dir=os.path.dirname(
                filename), delete=False) as tmp:
            replaced = False
            for line in cnf:
                if "Branch = " in line:
                    tmp.write(branch)
                    replaced = True
                else:
                    tmp.write("{}".format(line))
            if not replaced:
                tmp.write(branch)
        os.replace(tmp.name, filename)
        os.chmod(filename, 0o644)
    except OSError as err:
        print(".: {} {}: {}: {}".format(txt.ERR_CLR,
                                        txt.CANNOT_READ_FILE,
                                        err.filename,
                                        err.strerror))
        sys.exit(1)


def api_write_protocols(protocols, filename):
    """Write branch"""
    if protocols:
        protocols = "Protocols = {}\n".format(",".join(protocols))
    else:
        protocols = "# Protocols = \n"
    try:
        with open(
            filename) as cnf, tempfile.NamedTemporaryFile(
            "w+t", dir=os.path.dirname(
                filename), delete=False) as tmp:
            replaced = False
            for line in cnf:
                if "Protocols = " in line:
                    tmp.write(protocols)
                    replaced = True
                else:
                    tmp.write("{}".format(line))
            if not replaced:
                tmp.write(protocols)
        os.replace(tmp.name, filename)
        os.chmod(filename, 0o644)
    except OSError as err:
        print(".: {} {}: {}: {}".format(txt.ERR_CLR,
                                        txt.CANNOT_READ_FILE,
                                        err.filename,
                                        err.strerror))
        sys.exit(1)


def build_config():
    """Get config informations
    :returns: config, custom
    :rtype: tuple
    """
    custom = False
    # default config
    config = {
        "to_be_removed": conf.TO_BE_REMOVED,  # long after 2017-04-18
        "branch": "stable",
        "branches": conf.BRANCHES,
        "config_file": conf.CONFIG_FILE,
        "custom_file": conf.CUSTOM_FILE,
        "method": "rank",
        "work_dir": conf.WORK_DIR,
        "mirror_file": conf.MIRROR_FILE,
        "mirror_list": conf.MIRROR_LIST,
        "no_update": False,
        "only_country": [],
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
                    elif key == "Branch":
                        config["branch"] = value
                    elif key == "OnlyCountry":
                        custom = True
                        if "," in value:
                            config["only_country"] = value.split(",")
                        else:
                            config["only_country"] = value.split(" ")
                    elif key == "MirrorlistsDir":
                        config["work_dir"] = value
                    elif key == "OutputMirrorlist":
                        config["mirror_list"] = value
                    elif key == "NoUpdate":
                        config["no_update"] = value
                    elif key == "SSLVerify":
                        if value == "False":
                            config["ssl_verify"] = False
                    elif key == "Protocols":
                        if "," in value:
                            config["protocols"] = value.split(",")
                        else:
                            config["protocols"] = value.split(" ")
    except (PermissionError, OSError) as err:
        print(".: {} {}: {}: {}".format(txt.ERR_CLR,
                                        txt.CANNOT_READ_FILE,
                                        err.filename,
                                        err.strerror))
    return config, custom


def modify_config(config, custom=False):
    """Modify configuration
    :param config: dictionary
    :param custom:
    """
    if not custom:
        # remove custom file if present
        if os.path.isfile(config["custom_file"]):
            os.remove(config["custom_file"])
    write_configuration(config["config_file"],
                        config["only_country"],
                        custom=custom)


def write_configuration(filename, selection, custom=False):
    """Writes the configuration to file
    :param filename:
    :param selection:
    :param custom:
    """
    if custom:
        if selection == ["Custom"]:
            selection = "OnlyCountry = Custom\n"
        else:
            selection = "OnlyCountry = {list}\n".format(
                list=",".join(selection))
    else:
        selection = "# OnlyCountry = \n"
    try:
        with open(
            filename) as cnf, tempfile.NamedTemporaryFile(
            "w+t", dir=os.path.dirname(
                filename), delete=False) as tmp:

            replaced = False
            for line in cnf:
                if "OnlyCountry" in line:
                    tmp.write(selection)
                    replaced = True
                else:
                    tmp.write("{}".format(line))
            if not replaced:
                tmp.write(selection)
        os.replace(tmp.name, filename)
        os.chmod(filename, 0o644)
    except OSError as err:
        print(".: {} {}: {}: {}".format(txt.ERR_CLR, txt.CANNOT_READ_FILE,
                                        err.filename, err.strerror))
        sys.exit(1)
