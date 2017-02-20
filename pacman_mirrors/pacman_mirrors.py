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
# Authors: Esclapion
#          philm
#          Ramon Buldó <rbuldo@gmail.com>
#          Hugo Posnic <huluti@manjaro.org>
#          Frede Hundewadt <frede@hundewadt.dk>

"""Pacman-Mirrors Main Module"""

import argparse
import importlib.util
import sys
import os
from operator import itemgetter
from pacman_mirrors import __version__
from random import shuffle
# CHANGE CONTENT IN configuration
from .configuration import DEVELOPMENT, DESCRIPTION
from .configuration import CONFIG_FILE, CUSTOM_FILE, FALLBACK, \
    MIRROR_DIR, MIRROR_LIST, MIRROR_FILE, STATUS_FILE
from .custom_help_formatter import CustomHelpFormatter
from .customfn import CustomFn
from .filefn import FileFn
from .httpfn import HttpFn
from .jsonfn import JsonFn
from .mirror import Mirror
from .mirrorfn import MirrorFn
from .miscfn import MiscFn
from .validfn import ValidFn
from . import i18n
from . import txt

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
        # Lists
        self.mirrors = Mirror()
        self.selected_countries = []        # users selected countries
        # Decisions
        self.custom = False
        self.fasttrack = None
        self.geoip = False
        self.interactive = False
        self.network = True
        self.no_display = False
        self.quiet = False
        # Time out
        self.max_wait_time = 2
        self.config = {}

    @staticmethod
    def build_config():
        """Get config informations"""
        # initialising defaults
        # information which can differ from these defaults
        # is fetched from config file
        build_cfg = {
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
                            build_cfg["method"] = value
                        elif key == "Branch":
                            build_cfg["branch"] = value
                        elif key == "OnlyCountry":
                            build_cfg["only_country"] = value.split(",")
                        elif key == "MirrorlistsDir":
                            build_cfg["mirror_dir"] = value
                        elif key == "OutputMirrorlist":
                            build_cfg["mirror_list"] = value
                        elif key == "NoUpdate":
                            build_cfg["no_update"] = value
        except (PermissionError, OSError) as err:
            print(".: {} {}: {}: {}".format(txt.ERR_CLR,
                                            txt.CANNOT_READ_FILE,
                                            err.filename,
                                            err.strerror))
        return build_cfg

    def command_line_parse(self):
        """Read the arguments of the command line"""
        parser = argparse.ArgumentParser(formatter_class=CustomHelpFormatter)
        parser.add_argument("-g", "--generate",
                            action="store_true",
                            help=txt.HLP_ARG_GENERATE)
        parser.add_argument("-m", "--method",
                            type=str,
                            choices=["rank", "random"],
                            help=txt.HLP_ARG_METHOD)
        parser.add_argument("-b", "--branch",
                            type=str,
                            choices=["stable", "testing", "unstable"],
                            help=txt.HLP_ARG_BRANCH)
        parser.add_argument("-c", "--country",
                            type=str,
                            help=txt.HLP_ARG_COUNTRY)
        parser.add_argument("--geoip",
                            action="store_true",
                            help=txt.HLP_ARG_GEOIP_P1 + txt.OPT_COUNTRY +
                            txt.HLP_ARG_GEOIP_P2)
        parser.add_argument("-d", "--mirror_dir",
                            type=str,
                            metavar=txt.PATH,
                            help=txt.HLP_ARG_PATH)
        parser.add_argument("-o", "--output",
                            type=str,
                            metavar=txt.FILE,
                            help=txt.HLP_ARG_FILE)
        parser.add_argument("-t", "--timeout",
                            type=int,
                            metavar=txt.SECONDS,
                            help=txt.HLP_ARG_TIMEOUT)
        parser.add_argument("--no-update",
                            action="store_true",
                            help=txt.HLP_ARG_NOUPDATE_P1 + txt.OPT_NOUPDATE +
                            txt.HLP_ARG_NOUPDATE_P2)
        parser.add_argument("-i", "--interactive",
                            action="store_true",
                            help=txt.HLP_ARG_INTERACTIVE)
        parser.add_argument("-v", "--version",
                            action="store_true",
                            help=txt.HLP_ARG_VERSION)
        parser.add_argument("-q", "--quiet",
                            action="store_true",
                            help=txt.HLP_ARG_QUIET)
        # TODO: experimental arguments
        parser.add_argument("-f", "--fasttrack",
                            type=int,
                            metavar=txt.DIGIT,
                            help=txt.HLP_ARG_FASTTRACK)

        args = parser.parse_args()

        if len(sys.argv) == 1:
            parser.print_help()
            exit(0)

        if args.version:
            if DEVELOPMENT:
                print("{}pacman-mirrors {} {} {}".format(txt.YS,
                                                         __version__,
                                                         DESCRIPTION,
                                                         txt.CE))
            else:
                print("pacman-mirrors {}".format(__version__))
            exit(0)

        if not DEVELOPMENT:
            if os.getuid() != 0:
                print(".: {} {}".format(txt.ERR_CLR, txt.MUST_BE_ROOT))
                exit(1)

        if args.no_update:
            if self.config["no_update"] == "True":
                exit(0)

        if args.method:
            self.config["method"] = args.method

        if args.branch:
            self.config["branch"] = args.branch

        if args.timeout:
            self.max_wait_time = args.timeout

        if args.quiet:
            self.quiet = True

        if args.mirror_dir:
            self.config["mirror_dir"] = args.mirror_dir

        if args.output:
            if args.output[0] == "/":
                self.config["mirror_list"] = args.output
            else:
                self.config["mirror_list"] = os.getcwd() + "/" + args.output

        if args.interactive:
            self.interactive = True
            if not os.environ.get("DISPLAY") or not GTK_AVAILABLE:
                self.no_display = True
        # geoip and country are mutually exclusive
        if args.geoip:
            self.geoip = True

        if args.country and not args.geoip:
            self.custom = True
            self.config["only_country"] = args.country.split(",")

        if args.fasttrack:
            self.fasttrack = args.fasttrack
            self.config["only_country"] = []
            self.geoip = False

    def build_common_mirror_list(self):
        """Generate common mirrorlist"""
        worklist = MirrorFn.filter_mirror_list(self.mirrors.mirrorlist,
                                               self.selected_countries)
        if self.config["method"] == "random":
            shuffle(worklist)
        else:
            self.test_mirrors()
            worklist = sorted(worklist, key=itemgetter("resp_time"))

        FileFn.output_mirror_list(self.config["branch"],
                                  self.config["mirror_list"],
                                  worklist,
                                  self.quiet)
        if self.custom or self.config["only_country"] != self.mirrors.mirrorlist:
            CustomFn.modify_config(self.config["only_country"],
                                   custom=True)
        else:
            CustomFn.modify_config(self.config["only_country"])

    def build_interactive_mirror_list(self):
        """Prompt the user to select the mirrors with a gui.
        * Outputs a pacman mirrorlist,
        * Outputs a "custom" mirror file
        * Modify the configuration file to use the "custom" file.
        """
        if self.config["method"] == "rank":
            self.test_mirrors()
        interactive_list = []
        worklist = MirrorFn.filter_mirror_list(self.mirrors.mirrorlist, self.selected_countries)
        for mirror in worklist:
            interactive_list.append({
                "country": mirror["country"],
                "resp_time": mirror["resp_time"],
                "last_sync": mirror["last_sync"],
                "url": mirror["url"]
            })
        if self.config["method"] == "random":
            shuffle(interactive_list)
        else:
            interactive_list = sorted(interactive_list, key=itemgetter("resp_time"))
        if self.no_display:
            from . import consoleui as ui
        else:
            from . import graphical_ui as ui

        interactive = ui.run(interactive_list, random)

        if interactive.is_done:
            selected = []
            mirrorfile = []
            for item in interactive.custom_list:
                for server in self.mirrors.mirrorlist:
                    if item["url"] == server["url"]:
                        selected.append(server)
                        mirrorfile.append({
                            "country": server["country"],
                            "protocols": server["protocols"],
                            "url": server["url"]
                        })
            if mirrorfile:
                print("\n.: {}: {}".format(txt.INF_CLR, txt.CUSTOM_MIRROR_LIST))
                print("--------------------------")
                # output mirror file
                JsonFn.write_json_file(mirrorfile, CUSTOM_FILE)
                print(".: {} {}: {}".format(txt.INF_CLR,
                                            txt.CUSTOM_MIRROR_FILE_SAVED,
                                            CUSTOM_FILE))
                # output pacman mirrorlist
                FileFn.output_mirror_list(self.config["branch"],
                                          self.config["mirror_list"],
                                          worklist,
                                          custom=True,
                                          quiet=self.quiet)
                # output custom configuration
                self.config["only_country"] = ["Custom"]
                CustomFn.modify_config(self.config["only_country"], custom=True)
                print(".: {} {}: {}".format(txt.INF_CLR,
                                            txt.MIRROR_LIST_SAVED,
                                            CUSTOM_FILE))
                print(".: {} {}".format(txt.INF_CLR, txt.RESET_CUSTOM_CONFIG))
            else:
                print(".: {} {}".format(txt.WRN_CLR, txt.NO_SELECTION))
                print(".: {} {}".format(txt.INF_CLR, txt.NO_CHANGE))

    def load_all_mirrors(self):
        """Load mirrors"""
        self.selected_countries = self.config["only_country"]
        if self.selected_countries == ["all"]:
            self.config["only_country"] = []
            self.custom = False  # reset args -c
        # decision on custom or default
        if self.custom is True:
            if self.config["only_country"] == ["Custom"]:
                if ValidFn.custom_config_is_valid():
                    self.load_custom_mirrors()
                    self.selected_countries = self.mirrors.countrylist
            else:
                self.selected_countries = self.config["only_country"]
                self.load_default_mirrors()
        else:
            self.load_default_mirrors()
        # build country list
        self.selected_countries = MirrorFn.build_country_list(self.selected_countries,
                                                              self.mirrors.countrylist,
                                                              self.geoip)

    def load_custom_mirrors(self):
        servers = FileFn.read_mirror_file(CUSTOM_FILE)
        self.mirrors.seed(servers)

    def load_default_mirrors(self):
        """Load default mirror file"""
        file = ""
        status = False  # status.json or mirrors.json
        # decision on file avaiablity
        if FileFn.check_file(STATUS_FILE):
            status = True
            file = STATUS_FILE
        elif FileFn.check_file(MIRROR_FILE):
            file = MIRROR_FILE
        elif FileFn.check_file(FALLBACK):
            file = FALLBACK
        else:
            print("\n{}.:! {}{}\n".format(txt.RS, "Houston?! we have a problem", txt.CE))
            exit(1)
        mirrors = FileFn.read_mirror_file(file)
        # seed mirror object
        if status:
            self.mirrors.seed(mirrors, status)
        else:
            self.mirrors.seed(mirrors)

    def build_fasttrack_mirror_list(self, number):
        """Fast-track the mirrorlist by aggressive sorting"""
        temp = sorted(self.mirrors.mirrorlist, key=itemgetter("branches",
                                                              "last_sync"),
                      reverse=True)
        temp = sorted(temp, key=itemgetter("last_sync"), reverse=False)
        ftlist = []
        print(".: {}: {} - {}".format(txt.INF_CLR, txt.QUERY_MIRRORS, txt.TAKES_TIME))
        counter = 0
        for mirror in temp:
            resp_time = HttpFn.get_mirror_response(mirror["url"])
            print("   ..... {:<15}: {}: {}".format(mirror["country"],
                                                   mirror["last_sync"],
                                                   mirror["url"]),
                  end='')
            sys.stdout.flush()
            mirror["resp_time"] = resp_time
            print("\r   {:<5}{}{} ".format(txt.GS, resp_time, txt.CE))
            if resp_time == txt.SERVER_RES:
                continue
            ftlist.append(mirror)
            counter += 1
            if counter == number:
                break
        ftlist = sorted(ftlist, key=itemgetter("resp_time"))
        FileFn.output_mirror_list(self.config["branch"],
                                  self.config["mirror_list"],
                                  ftlist,
                                  self.quiet)

    def test_mirrors(self):
        """Query server for response time"""
        print(".: {} {} - {}".format(txt.INF_CLR, txt.QUERY_MIRRORS, txt.TAKES_TIME))
        if self.custom:
            print(".: {} {}".format(txt.INF_CLR, txt.USING_CUSTOM_FILE))
        else:
            print(".: {} {}".format(txt.INF_CLR, txt.USING_DEFAULT_FILE))

        for mirror in self.mirrors.mirrorlist:
            if mirror["country"] in self.selected_countries:
                print("   ..... {:<15}: {}".format(mirror["country"],
                                                   mirror["url"]), end='')
                # sys.stdout.flush()
                resp_time = HttpFn.get_mirror_response(mirror["url"])
                print("\r   {:<5}{}{} ".format(txt.GS, resp_time, txt.CE))
                mirror["resp_time"] = resp_time

    def run(self):
        """Run"""
        FileFn.dir_must_exist(MIRROR_DIR)
        self.config = self.build_config()
        self.command_line_parse()
        self.network = HttpFn.update_mirrors()
        self.load_all_mirrors()

        # actual generation
        if self.fasttrack:
            self.build_fasttrack_mirror_list(self.fasttrack)
        else:
            if self.interactive:
                self.build_interactive_mirror_list()
            else:
                self.build_common_mirror_list()

        # # TODO: Eventually remove in production
        if DEVELOPMENT:
            print("{}.:! Pacman-Mirrors {} - {} {}".format(txt.YS,
                                                           __version__,
                                                           DESCRIPTION,
                                                           txt.CE))


if __name__ == "__main__":
    app = PacmanMirrors()
    app.run()
