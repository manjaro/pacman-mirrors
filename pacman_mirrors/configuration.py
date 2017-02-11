#!/usr/bin/env python3
"""Pacman-Mirrors Configuration"""

# http constants
MIRRORS_URL = "http://repo.manjaro.org/mirrors.json"
STATES_URL = "http://repo.manjaro.org/status.json"
# local file constants
MIRRORS_FILE = "/etc/pacman.d/mirrors/mirrors.json"
STATES_FILE = "/etc/pacman.d/mirrors/status.json"
# repo constants
BRANCHES = ("stable", "testing", "unstable")
REPO_ARCH = "$repo/$arch"
