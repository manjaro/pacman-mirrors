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
# Authors: Esclapion <esclapion@manjaro.org>
#          philm <philm@manjaro.org>
#          Ramon Buldó <rbuldo@gmail.com>
#          Hugo Posnic <huluti@manjaro.org>
#          Frede Hundewadt <echo ZmhAbWFuamFyby5vcmcK | base64 -d>

"""Pacman-Mirrors Main Module"""

import importlib.util
import sys

import pacman_mirrors.functions.util
from pacman_mirrors.builder import common, fasttrack, interactive
from pacman_mirrors.config import configuration as conf
from pacman_mirrors.functions import cliFn
from pacman_mirrors.functions import configFn
from pacman_mirrors.functions import defaultFn
from pacman_mirrors.functions import fileFn
from pacman_mirrors.functions import httpFn

from pacman_mirrors.functions import util
from pacman_mirrors.mirrors.mirror import Mirror
from pacman_mirrors.translation import i18n

try:
    importlib.util.find_spec("gi.repository.Gtk")
except ImportError:
    GTK_AVAILABLE = False
else:
    GTK_AVAILABLE = True
_ = i18n.language.gettext


class PacmanMirrors:
    """Class PacmanMirrors"""

    def __init__(self):
        """Init"""
        self.config = {
            "config_file": conf.CONFIG_FILE
        }
        self.custom = False
        self.default = False
        self.fasttrack = None
        self.geoip = False
        self.interactive = False
        self.max_wait_time = 2
        self.mirrors = Mirror()
        self.network = True
        self.no_display = False
        self.no_mirrorlist = False
        self.no_status = False
        self.quiet = False
        self.selected_countries = []

    def run(self):
        """
        Run
        # Setup config: retunrs the config dictionary and true/false on custom
        # Parse commandline
        # i686 check - change branch to x32-$branch
        # sanitize config
        # Check network
        # Check if mirrorlist is not to be touched - normal exit
        # Handle missing network
        # Load all mirrors
        # Build mirror list
        """
        (self.config, self.custom) = configFn.setup_config()
        fileFn.create_dir(self.config["work_dir"])
        cliFn.parse_command_line(self, GTK_AVAILABLE)
        util.i686_check(self, write=True)
        if not configFn.sanitize_config(self.config):
            sys.exit(2)
        self.network = httpFn.inet_conn_check()
        if self.network:
            httpFn.update_mirrors(self.config, quiet=self.quiet)
        if self.no_mirrorlist:
            sys.exit(0)
        if not self.network:
            if not self.quiet:
                pacman_mirrors.functions.util.internet_message()
            self.config["method"] = "random"
            self.fasttrack = False
        """
        # Load all mirrors
        """
        defaultFn.load_config_mirror_pool(self)
        """
        # Decide which type of mirrorlist to create
        * Fasttrack
        * Interactive
        * Default
        """
        if self.fasttrack:
            fasttrack.build_mirror_list(self, self.fasttrack)
        elif self.interactive:
            interactive.build_mirror_list(self)
        else:
            common.build_mirror_list(self)


if __name__ == "__main__":
    app = PacmanMirrors()
    app.run()

