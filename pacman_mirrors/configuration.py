#!/usr/bin/env python3
"""Pacman-Mirrors Configuration"""

# http constants
MIRRORS_URL = "http://repo.manjaro.org/mirrors.json"
STATES_URL = "http://repo.manjaro.org/status.json"
# local file constants
# commented while dev
# MIRRORS_JSON = "/var/lib/pacman-mirrors/mirrors.json"
# STATES_JSON = "/var/lib/pacman-mirrors/status.json"
# CUSTOM_MIRROR_JSON = "/var/lib/pacman-mirrors/custom-mirrors.json"
# CUSTOM_MIRROR_FILE = "/var/lib/pacman-mirrors/Custom"
# used while dev
MIRRORS_JSON = "data/mirrors.json"
STATES_JSON = "data/status.json"
CUSTOM_MIRROR_JSON = "data/custom-mirrors.json"
CUSTOM_MIRROR_FILE = "data/Custom"

# repo constants
BRANCHES = ("stable", "testing", "unstable")
REPO_ARCH = "$repo/$arch"
