#!/usr/bin/env python3
"""Pacman-Mirrors Configuration"""
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
REPO_ARCH = "$repo/$arch"
