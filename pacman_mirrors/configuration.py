#!/usr/bin/env python3
"""Pacman-Mirrors Configuration Module"""
import os
import datetime
import tempfile
from . import txt

ENV = "dev"
# http constants
URL_MIRROR_JSON = "http://repo.manjaro.org/mirrors.json"
URL_STATUS_JSON = "http://repo.manjaro.org/status.json"

if ENV == "dev":
    # etc
    CONFIG_FILE = "mock/etc/pacman-mirrors.conf"
    MIRROR_LIST = "mock/etc/mirrorlist"
    # pacman-mirrors
    MIRROR_DIR = "mock/var/"
    CUSTOM_FILE = MIRROR_DIR + "custom-mirrors.json"
    MIRROR_FILE = MIRROR_DIR + "mirrors.json"
    STATUS_FILE = MIRROR_DIR + "status.json"
    # special cases
    FALLBACK = "mock/usr/mirrors.json"
    O_CUST_FILE = MIRROR_DIR + "Custom"
else:
    # etc
    CONFIG_FILE = "/etc/pacman-mirrors.conf"
    MIRROR_LIST = "/etc/pacman.d/mirrorlist"
    # pacman-mirrors
    MIRROR_DIR = "/var/lib/pacman-mirrors/"
    CUSTOM_FILE = MIRROR_DIR + "custom-mirrors.json"
    MIRROR_FILE = MIRROR_DIR + "mirrors.json"
    STATUS_FILE = MIRROR_DIR + "status.json"
    # special cases
    FALLBACK = "/usr/share/pacman-mirrors/mirrors.json"
    O_CUST_FILE = MIRROR_DIR + "Custom"

# repo constants
BRANCHES = ("stable", "testing", "unstable")
REPO_ARCH = "/$repo/$arch"


class Config:
    """Configuration class"""
    @staticmethod
    def initialize():
        """Get config informations"""
        # initialising defaults
        # information which can differ from these defaults
        # is fetched from config file
        config = {
            "mirror_file": MIRROR_FILE,
            "branch": "stable",
            "method": "rank",
            "mirror_dir": MIRROR_DIR,
            "mirror_list": MIRROR_LIST,
            "no_update": False,
            "only_country": [],
        }
        try:
            # read configuration from file
            with open(CONFIG_FILE) as conf:
                for line in conf:
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
            print(".:> {}: {}: {}: {}".format(txt.ERROR,
                                              txt.ERR_FILE_READ,
                                              err.filename,
                                              err.strerror))
        return config

    @staticmethod
    def write_custom_config(filename, selection, custom=False):
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
            print(".:> {}: {}: {}: {}".format(txt.ERROR, txt.ERR_FILE_READ,
                                              err.filename, err.strerror))
            exit(1)
