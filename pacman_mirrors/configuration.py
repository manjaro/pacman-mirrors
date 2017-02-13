#!/usr/bin/env python3
"""Pacman-Mirrors Configuration"""
ENV = "dev"
# http constants
URL_MIRROR_JSON = "http://repo.manjaro.org/mirrors.json"
URL_STATUS_JSON = "http://repo.manjaro.org/status.json"
# local file constants
if ENV == "production":
    O_CUST_FILE = "/var/lib/pacman-mirrors/Custom"
    CUSTOM_FILE = "custom-mirrors.json"
    CONFIG_FILE = "/etc/pacman-mirrors"
    MIRROR_DIR = "/var/lib/manjaro-mirrors/"
    MIRROR_FILE = "mirrors.json"
    MIRROR_LIST = "/etc/pacman.d/mirrorlist"
    STATUS_FILE = "status.json"
else:
    O_CUST_FILE = "data/pacman-mirrors/Custom"
    CUSTOM_FILE = "custom-mirrors.json"
    CONFIG_FILE = "conf/pacman-mirrors.conf"
    MIRROR_DIR = "data/manjaro-mirrors/"
    MIRROR_FILE = "mirrors.json"
    MIRROR_LIST = "data/mirrorlist"
    STATUS_FILE = "status.json"
# repo constants
BRANCHES = ("stable", "testing", "unstable")
REPO_ARCH = "$repo/$arch"
