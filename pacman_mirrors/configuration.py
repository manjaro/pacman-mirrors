#!/usr/bin/env python3
"""Pacman-Mirrors Configuration Module"""
# http constants
URL_MIRROR_JSON = "http://repo.manjaro.org/mirrors.json"
URL_STATUS_JSON = "http://repo.manjaro.org/status.json"
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
