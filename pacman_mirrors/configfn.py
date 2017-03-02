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
import tempfile

from . import txt
from . import configuration as conf


def build_config():
    """Get config informations"""
    # initialising defaults
    # information which can differ from these defaults
    # is fetched from config file
    config = {
        "branch": "stable",
        "config_file": conf.CONFIG_FILE,
        "custom_file": conf.CUSTOM_FILE,
        "method": "rank",
        "mirror_dir": conf.MIRROR_DIR,
        "mirror_file": conf.MIRROR_FILE,
        "mirror_list": conf.MIRROR_LIST,
        "no_update": False,
        "only_country": [],
    }
    try:
        # read configuration from file
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
                        config["only_country"] = value.split(",")
                    elif key == "MirrorlistsDir":
                        config["mirror_dir"] = value
                    elif key == "OutputMirrorlist":
                        config["mirror_list"] = value
                    elif key == "NoUpdate":
                        config["no_update"] = value
    except (PermissionError, OSError) as err:
        print(".: {} {}: {}: {}".format(txt.ERR_CLR,
                                        txt.CANNOT_READ_FILE,
                                        err.filename,
                                        err.strerror))
    return config


def modify_config(conf_file, cust_file, onlycountry, custom=False):
    """Modify configuration"""
    if not custom:
        if os.path.isfile(cust_file):
            os.remove(cust_file)
    write_configuration(conf_file, onlycountry, custom)


def write_configuration(filename, selection, custom=False):
    """Writes the configuration to file
    :param filename:
    :param selection:
    :param custom:
    """
    if custom:
        if selection == ["Custom"]:
            new_config = "OnlyCountry = Custom\n"
        else:
            new_config = "OnlyCountry = {list}\n".format(
                list=",".join(selection))
    else:
        new_config = "# OnlyCountry = \n"
    try:
        with open(
            filename) as cnf, tempfile.NamedTemporaryFile(
            "w+t", dir=os.path.dirname(
                filename), delete=False) as tmp:
            replaced = False
            for line in cnf:
                if "OnlyCountry" in line:
                    tmp.write(new_config)
                    replaced = True
                else:
                    tmp.write("{}".format(line))
            if not replaced:
                tmp.write(new_config)
        os.replace(tmp.name, filename)
        os.chmod(filename, 0o644)
    except OSError as err:
        print(".: {} {}: {}: {}".format(txt.ERR_CLR, txt.CANNOT_READ_FILE,
                                        err.filename, err.strerror))
        exit(1)
