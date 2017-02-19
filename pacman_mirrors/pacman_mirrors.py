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
    MIRROR_DIR, MIRROR_LIST, MIRROR_FILE, STATUS_FILE, REPO_ARCH
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
        self.only_country = []        # users selected countries
        # Decisions
        self.custom = False
        self.fasttrack = None
        self.geoip = False
        self.interactive = False
        self.manjaro_online = True
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
                                            txt.ERR_FILE_READ,
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
                print("{}pacman-mirrors {} {} {}".format(txt.YS, __version__, DESCRIPTION, txt.CE))
            else:
                print("pacman-mirrors {}".format(__version__))
            exit(0)

        if not DEVELOPMENT:
            if os.getuid() != 0:
                print(".: {} {}".format(txt.ERR_CLR, txt.ERR_NOT_ROOT))
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
            self.config["only_country"] = args.country.split(",")

        if args.fasttrack:
            self.fasttrack = args.fasttrack
            self.config["only_country"] = []
            self.geoip = False

    def gen_mirror_list_common(self):
        """Generate common mirrorlist"""
        args_c = self.config["only_country"] != self.mirrors.countrylist
        if self.config["method"] == "random":
            shuffle(self.mirrors.mirrorlist)
        else:
            templist = sorted(self.mirrors.mirrorlist, key=itemgetter("resp_time"))
            templist = MirrorFn.filter_mirror_list(templist, self.config["only_country"])
            self.output_mirror_list(templist)
            if self.custom or args_c:
                self.modify_config(custom=True)
            else:
                self.modify_config()

    def gen_mirror_list_interactive(self):
        """Prompt the user to select the mirrors with a gui.
        * Outputs a pacman mirrorlist,
        * Outputs a "custom" mirror file
        * Modify the configuration file to use the "custom" file.
        """
        random = self.config["method"] == "random"
        mirrorlist = []
        interactive_list = []
        for country in self.only_country:
            for mirror in self.mirrors.mirrorlist:
                if country == mirror["country"]:
                    mirrorlist.append(mirror)
                    interactive_list.append({
                        "country": mirror["country"],
                        "resp_time": mirror["resp_time"],
                        "last_sync": mirror["last_sync"],
                        "url": mirror["url"]
                    })
                    interactive_list = sorted(interactive_list, key=itemgetter("resp_time"))
                    if random:
                        shuffle(interactive_list)
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
                print("\n.: {}: {}".format(txt.INF_CLR, txt.INF_INTERACTIVE_LIST))
                print("--------------------------")
                # output mirror file
                JsonFn.write_json_file(mirrorfile, CUSTOM_FILE)
                print(".: {} {}: {}".format(txt.INF_CLR, txt.INF_MIRROR_FILE_SAVED, CUSTOM_FILE))
                # output pacman mirrorlist
                self.output_mirror_list(selected)
                # output custom configuration
                self.config["only_country"] = ["Custom"]
                self.modify_config(custom=True)
                print(".: {} {}: {}".format(txt.INF_CLR, txt.INF_INTERACTIVE_LIST_SAVED, CUSTOM_FILE))
            else:
                print(".: {} {}".format(txt.WRN_CLR, txt.INF_NO_SELECTION))
                print(".: {} {}".format(txt.WRN_CLR, txt.INF_NO_CHANGES))

    def gen_server_lists(self):
        """Generate server lists"""
        if self.config["method"] == "rank":
            self.run_test_mirror_list()
        else:
            print(".: {} {}".format(txt.INF_CLR, txt.INF_RANDOMIZE_SERVERS))
            shuffle(self.mirrors.mirrorlist)

    def load_all_mirrors(self):
        """Load mirrors"""
        self.only_country = self.config["only_country"]
        if self.config["only_country"] == ["Custom"]:
            self.config = True
            self.load_custom_mirrors()
            self.only_country = self.mirrors.countrylist
        else:
            self.load_default_mirrors()

        self.only_country = MirrorFn.build_country_list(self.only_country,
                                                        self.mirrors.countrylist,
                                                        self.geoip)

    def load_custom_mirrors(self):
        """Load custom mirror file"""
        valid = ValidFn.custom_config_is_valid()
        if valid:
            servers = FileFn.read_mirror_file(CUSTOM_FILE)
            self.mirrors.seed(servers)

    def load_default_mirrors(self):
        """Load default mirror file"""
        seeds = False  # status.json or mirrors.json
        if FileFn.check_file(STATUS_FILE):
            seeds = True
            file = STATUS_FILE
        elif FileFn.check_file(MIRROR_FILE):
            file = MIRROR_FILE
        else:
            file = FALLBACK
        mirrors = FileFn.read_mirror_file(file)
        if seeds:
            self.mirrors.seed(mirrors, status=True)
        else:
            self.mirrors.seed(mirrors)

    def modify_config(self, custom=False):
        """Modify configuration"""
        if not custom:
            # remove custom mirror file
            if os.path.isfile(CUSTOM_FILE):
                os.remove(CUSTOM_FILE)
        CustomFn.write_custom_config(CONFIG_FILE, self.config["only_country"], custom)

    def output_mirror_list(self, servers):
        """Write servers to /etc/pacman.d/mirrorlist
        :param: servers: list of servers to write
        """
        try:
            with open(self.config["mirror_list"], "w") as outfile:
                print(".: {} {}".format(txt.INF_CLR, txt.INF_MIRROR_LIST_WRITE))
                # write list header
                FileFn.write_mirrorlist_header(outfile)
                for server in servers:
                    url = server["url"]
                    for protocol in enumerate(server["protocols"]):
                        pos = url.find(":")
                        server["url"] = "{}{}{}{}".format(protocol[1],
                                                          url[pos:],
                                                          self.config["branch"],
                                                          REPO_ARCH)
                        # write list entry
                        FileFn.write_mirrorlist_entry(outfile, server)
                        if not self.quiet:
                            print("   {}{:<15}{} : {}".format(txt.YS, server["country"], txt.CE, server["url"]))
                print(".: {} {}: {}".format(txt.INF_CLR, txt.INF_MIRROR_LIST_SAVED, self.config["mirror_list"]))
        except OSError as err:
            print(".: {} {}: {}: {}".format(txt.ERR_CLR, txt.ERR_FILE_WRITE, err.filename, err.strerror))
            exit(1)

    def run_fast_track(self, number=5):
        """Fast-track the mirrorlist by aggressive filtering"""
        temp = sorted(self.mirrors.mirrorlist, key=itemgetter("branches", "last_sync"), reverse=True)
        temp = sorted(temp, key=itemgetter("last_sync"), reverse=False)
        ftlist = []
        print(".: {}: {}".format(txt.INF_CLR, txt.INF_QUERY_SERVERS))
        for x in range(number):
            mirror = temp[x]
            res = HttpFn.get_mirror_response(mirror["url"])
            if res == txt.SERVER_RES:
                continue
            mirror["resp_time"] = res
            print("   {}: {} {} {}".format(txt.INF_CLR, mirror["last_sync"], res, mirror["url"]))
            ftlist.append(mirror)
        ftlist = sorted(ftlist, key=itemgetter("resp_time"))
        self.output_mirror_list(ftlist)
        print(".: {}: {}".format(txt.INF_CLR, txt.INF_MIRROR_LIST_SAVED))

    def run_test_mirror_list(self):
        """Query server for response time"""
        if not self.config["only_country"] == ["Custom"]:
            print(".: {} {}".format(txt.INF_CLR, txt.INF_QUERY_SERVERS))
            print(".: {} {}".format(txt.INF_CLR, txt.INF_QUERY_DEFAULT_FILE))
        else:
            print(".: {} {}".format(txt.INF_CLR, txt.INF_QUERY_SERVERS))
            print(".: {} {}".format(txt.INF_CLR, txt.INF_QUERY_CUSTOM_FILE))
        for country in self.only_country:
            for mirror in self.mirrors.mirrorlist:
                if country == mirror["country"]:
                    print("   ..... {:<15}: {}".format(mirror["country"], mirror["url"]),
                          end='')
                    sys.stdout.flush()
                    resp_time = HttpFn.get_mirror_response(mirror["url"])
                    mirror["resp_time"] = resp_time
                    if resp_time == "99.99":
                        continue
                    print("\r   {:<5}{}{} ".format(txt.GS, resp_time, txt.CE))

    def run(self):
        """Run"""
        FileFn.dir_must_exist(MIRROR_DIR)
        self.config = self.build_config()
        self.command_line_parse()
        self.manjaro_online = HttpFn.manjaro_online_update()
        self.load_all_mirrors()
        # actual generation
        if self.fasttrack:
            self.run_fast_track(self.fasttrack)
        else:
            self.gen_server_lists()
            if self.interactive:
                self.gen_mirror_list_interactive()
            else:
                self.gen_mirror_list_common()

        # # TODO: Eventually remove in production
        if DEVELOPMENT:
            print("{}pacman-mirrors {} {} {}".format(txt.YS, __version__, DESCRIPTION, txt.CE))


if __name__ == "__main__":
    app = PacmanMirrors()
    app.run()
