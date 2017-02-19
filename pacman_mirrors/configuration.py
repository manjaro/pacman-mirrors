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

"""Pacman-Mirrors Configuration"""

# this is for runing in dev environment
# TODO: CHANGE BELOW IN PRODUCTION
DEVELOPMENT = "dev"
DESCRIPTION = "BETA UNSTABLE"
if DEVELOPMENT:
    # http constants
    URL_MIRROR_JSON = "http://repo.manjaro.org/mirrors.json"
    URL_STATUS_JSON = "http://repo.manjaro.org/status.json"
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
    # repo constants
    BRANCHES = ("stable", "testing", "unstable")
    REPO_ARCH = "/$repo/$arch"
else:
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
