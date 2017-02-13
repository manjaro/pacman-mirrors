#!/usr/bin/env python3
"""Pacman-Mirrors Configuration"""
ENV = "dev"
# http constants
URL_MIRROR_JSON = "http://repo.manjaro.org/mirrors.json"
URL_STATUS_JSON = "http://repo.manjaro.org/status.json"
# local file constants
if ENV == "production":
    CUSTOM_MIRROR_FILE = "/var/lib/pacman-mirrors/Custom"
    CUSTOM_MIRROR_JSON = "custom-mirrors.json"
    MIRRORS_DIR = "/var/lib/manjaro-mirrors/"
    MIRRORS_JSON = "mirrors.json"
    PACMAN_MIRROR_LIST = "/etc/pacman.d/mirrorlist"
    STATUS_JSON = "status.json"
else:
    CUSTOM_MIRROR_FILE = "data/pacman-mirrors/Custom"
    CUSTOM_MIRROR_JSON = "custom-mirrors.json"
    MIRRORS_DIR = "data/manjaro-mirrors/"
    MIRRORS_JSON = "mirrors.json"
    PACMAN_MIRROR_LIST = "data/mirrorlist"
    STATUS_JSON = "status.json"

# repo constants
BRANCHES = ("stable", "testing", "unstable")
REPO_ARCH = "$repo/$arch"
