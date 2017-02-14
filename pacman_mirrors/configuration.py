#!/usr/bin/env python3
"""Pacman-Mirrors Configuration"""
ENV = "dev"
# http constants
URL_MIRROR_JSON = "http://repo.manjaro.org/mirrors.json"
URL_STATUS_JSON = "http://repo.manjaro.org/status.json"

if ENV == "production":
    # dir constant
    MIRROR_DIR = "/var/lib/pacman-mirrors/"
    # file constant
    CUSTOM_FILE = MIRROR_DIR + "custom-mirrors.json"
    CONFIG_FILE = "/etc/pacman-mirrors.conf"
    HTTP_FALLBACK = MIRROR_DIR + "mirrors.json"
    MIRROR_FILE = "/usr/lib/pacman-mirrors/mirrors.json"
    MIRROR_LIST = "/etc/pacman.d/mirrorlist"
    STATUS_FILE = MIRROR_DIR + "status.json"
    # special case
    O_CUST_FILE = "/var/lib/pacman-mirrors/Custom"
else:
    # dir constant
    MIRROR_DIR = "root/var/lib/pacman-mirrors/"
    # file constant
    CUSTOM_FILE = MIRROR_DIR + "custom-mirrors.json"
    CONFIG_FILE = "root/etc/pacman-mirrors.conf"
    HTTP_FALLBACK = MIRROR_DIR + "mirrors.json"
    MIRROR_FILE = "root/usr/lib/pacman-mirrors/mirrors.json"
    MIRROR_LIST = "root/etc/pacman.d/mirrorlist"
    STATUS_FILE = MIRROR_DIR + "status.json"
    # special case
    O_CUST_FILE = "root/var/lib/pacman-mirrors/Custom"
# repo constants
BRANCHES = ("stable", "testing", "unstable")
REPO_ARCH = "$repo/$arch"
