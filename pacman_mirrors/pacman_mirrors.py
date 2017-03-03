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
from random import shuffle

from pacman_mirrors import __version__
from .custom_help_formatter import CustomHelpFormatter
from .mirror import Mirror
from . import mirrorfn
from . import configuration as conf
from . import configfn
from . import filefn
from . import httpfn
from . import i18n
from . import jsonfn
from . import miscfn
from . import txt
from . import validfn

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
            "config_file": conf.CONFIG_FILE  # purpose - testability
        }
        self.custom = False
        self.fasttrack = None
        self.geoip = False
        self.interactive = False
        self.max_wait_time = 2
        self.mirrors = Mirror()
        self.network = True
        self.no_display = False
        self.quiet = False
        self.selected_countries = []        # users selected countries

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
        parser.add_argument("-f", "--fasttrack",
                            type=int,
                            metavar=txt.DIGIT,
                            help=txt.HLP_ARG_FASTTRACK)

        args = parser.parse_args()

        if len(sys.argv) == 1:
            parser.print_help()
            exit(0)

        if args.version:
            print("pacman-mirrors {}".format(__version__))
            exit(0)

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
        worklist = mirrorfn.filter_mirror_list(self.mirrors.mirrorlist,
                                               self.selected_countries)
        if self.config["method"] == "rank":
            worklist = self.test_mirrors(worklist)
            worklist = sorted(worklist, key=itemgetter("resp_time"))
        else:
            shuffle(worklist)

        filefn.output_mirror_list(self.config["branch"],
                                  self.config["mirror_list"],
                                  worklist,
                                  quiet=self.quiet)
        if self.custom or \
                self.config["only_country"] != self.mirrors.mirrorlist:
            configfn.modify_config(self.config["config_file"],
                                   self.config["custom_file"],
                                   self.config["only_country"],
                                   custom=True)
        else:
            configfn.modify_config(self.config["config_file"],
                                   self.config["custom_file"],
                                   self.config["only_country"])

    def build_fasttrack_mirror_list(self, number):
        """Fast-track the mirrorlist by aggressive sorting"""
        temp = sorted(self.mirrors.mirrorlist,
                      key=itemgetter("branches", "last_sync"), reverse=True)
        temp = sorted(temp, key=itemgetter("last_sync"), reverse=False)
        ftlist = []
        print(".: {}: {} - {}".format(txt.INF_CLR,
                                      txt.QUERY_MIRRORS,
                                      txt.TAKES_TIME))
        counter = 0
        for mirror in temp:
            resp_time = httpfn.get_mirror_response(mirror["url"],
                                                   quiet=self.quiet)
            print("   ..... {:<15}: {}: {}".format(mirror["country"],
                                                   mirror["last_sync"],
                                                   mirror["url"]), end='')
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
        filefn.output_mirror_list(self.config["branch"],
                                  self.config["mirror_list"],
                                  ftlist,
                                  self.quiet)

    def build_interactive_mirror_list(self):
        """Prompt the user to select the mirrors with a gui.
        * Outputs a pacman mirrorlist,
        * Outputs a "custom" mirror file
        * Modify the configuration file to use the "custom" file.
        """
        worklist = mirrorfn.filter_mirror_list(self.mirrors.mirrorlist,
                                               self.selected_countries)
        if self.config["method"] == "rank":
            worklist = self.test_mirrors(worklist)
            worklist = sorted(worklist, key=itemgetter("resp_time"))
        else:
            shuffle(worklist)

        interactive_list = []
        for mirror in worklist:
            interactive_list.append({
                "country": mirror["country"],
                "resp_time": mirror["resp_time"],
                "last_sync": mirror["last_sync"],
                "url": mirror["url"]
            })

        if self.no_display:
            from . import consoleui as ui
        else:
            from . import graphical_ui as ui

        interactive = ui.run(interactive_list,
                             self.config["method"] == "random")

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
                print("\n.: {} {}".format(txt.INF_CLR,
                                          txt.CUSTOM_MIRROR_LIST))
                print("--------------------------")
                # output mirror file
                jsonfn.write_json_file(mirrorfile, self.config["custom_file"])
                print(".: {} {}: {}".format(txt.INF_CLR,
                                            txt.CUSTOM_MIRROR_FILE_SAVED,
                                            self.config["custom_file"]))
                # output pacman mirrorlist
                filefn.output_mirror_list(self.config["branch"],
                                          self.config["mirror_list"],
                                          worklist,
                                          custom=True,
                                          quiet=self.quiet)
                # always use "Custom" from interactive
                self.config["only_country"] = ["Custom"]
                configfn.modify_config(self.config["config_file"],
                                       self.config["custom_file"],
                                       self.config["only_country"],
                                       custom=True)
                print(".: {} {}: {}".format(txt.INF_CLR,
                                            txt.MIRROR_LIST_SAVED,
                                            self.config["custom_file"]))
                print(".: {} {}".format(txt.INF_CLR, txt.RESET_CUSTOM_CONFIG))
            else:
                print(".: {} {}".format(txt.WRN_CLR, txt.NO_SELECTION))
                print(".: {} {}".format(txt.INF_CLR, txt.NO_CHANGE))

    def disable_custom_config(self):
        """Perform reset of custom configuration"""
        self.config["only_country"] = []
        self.custom = False

    def load_all_mirrors(self):
        """Load mirrors"""
        if self.config["only_country"] == ["all"]:
            self.disable_custom_config()

        # decision on custom or default
        if self.config["only_country"] == ["Custom"]:
            if not validfn.custom_config_is_valid():
                self.disable_custom_config()
            else:
                self.custom = True
        else:
            self.selected_countries = self.config["only_country"]

        if self.custom:
            self.load_custom_mirrors()
            self.selected_countries = self.mirrors.countrylist
        else:
            self.load_default_mirrors()

        # build country list
        self.selected_countries = mirrorfn.build_country_list(
            self.selected_countries, self.mirrors.countrylist, self.geoip)

    def load_custom_mirrors(self):
        """Load available custom mirrors"""
        self.seed_mirrors(self.config["custom_file"])

    def load_default_mirrors(self):
        """Load all available mirrors"""
        (file, status) = filefn.return_mirror_filename()
        self.seed_mirrors(file, status)

    def seed_mirrors(self, file, status=False):
        """Seed mirrors"""
        mirrors = filefn.read_mirror_file(file)
        # seed mirror object
        if status:
            self.mirrors.seed(mirrors, status=status)
        else:
            self.mirrors.seed(mirrors)

    def test_mirrors(self, worklist):
        """Query server for response time"""
        if self.custom:
            print(".: {} {}".format(txt.INF_CLR, txt.USING_CUSTOM_FILE))
        else:
            print(".: {} {}".format(txt.INF_CLR, txt.USING_DEFAULT_FILE))
        print(".: {} {} - {}".format(txt.INF_CLR,
                                     txt.QUERY_MIRRORS,
                                     txt.TAKES_TIME))
        for mirror in worklist:
            if not self.quiet:
                print("   ..... {:<15}: {}".format(mirror["country"],
                                                   mirror["url"]), end='')
            sys.stdout.flush()
            resp_time = httpfn.get_mirror_response(mirror["url"],
                                                   quiet=self.quiet)
            mirror["resp_time"] = resp_time
            if resp_time == txt.SERVER_RES:
                continue
            if not self.quiet:
                print("\r   {:<5}{}{} ".format(txt.GS, resp_time, txt.CE))
        return worklist

    def run(self):
        """Run"""
        self.config = configfn.build_config()
        filefn.dir_must_exist(self.config["mirror_dir"])
        self.command_line_parse()
        self.load_all_mirrors()
        # network check
        self.network = httpfn.ping_host("google.com", 3)
        # all methods is available
        if self.network:
            httpfn.update_mirrors()
            # actual generation
            if self.fasttrack:
                self.build_fasttrack_mirror_list(self.fasttrack)
            else:
                if self.interactive:
                    self.build_interactive_mirror_list()
                else:
                    self.build_common_mirror_list()

        if not self.network:
            # only random is available if network is down
            if self.config["method"] == "random":
                if self.interactive:
                    self.build_interactive_mirror_list()
                else:
                    self.build_common_mirror_list()
            else:
                miscfn.internet_message()


if __name__ == "__main__":
    app = PacmanMirrors()
    app.run()
