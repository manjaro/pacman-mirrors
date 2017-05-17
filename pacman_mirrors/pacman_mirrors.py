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
#          Frede Hundewadt <frede@hundewadt.dk>

"""Pacman-Mirrors Main Module"""

import argparse
import importlib.util
import sys
import os
from operator import itemgetter
from random import shuffle
import subprocess

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
        self.country_list = False
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
        self.quiet = False
        self.selected_countries = []  # users selected countries
        self.sync = False

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
        geo_country = parser.add_mutually_exclusive_group()
        geo_country.add_argument("-c", "--country",
                                 type=str,
                                 nargs="+",
                                 help=txt.HLP_ARG_COUNTRY)
        geo_country.add_argument("--geoip",
                                 action="store_true",
                                 help="{} {} {}".format(txt.HLP_ARG_GEOIP_P1,
                                                        txt.OPT_COUNTRY,
                                                        txt.HLP_ARG_GEOIP_P2))
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
                            help="{} {} {}".format(txt.HLP_ARG_NOUPDATE_P1,
                                                   txt.OPT_NOUPDATE,
                                                   txt.HLP_ARG_NOUPDATE_P2))
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
                            help="{} {}".format(txt.HLP_ARG_FASTTRACK,
                                                txt.OVERRIDE_OPT))
        parser.add_argument("-l", "--country-list", "--list",
                            action="store_true",
                            help=txt.HLP_ARG_LIST)
        parser.add_argument("--default",
                            action="store_true",
                            help=txt.HLP_ARG_DEFAULT)
        parser.add_argument("-u", "--update",
                            action="store_true",
                            help="pacman -Syy")
        parser.add_argument("-n", "--no-mirrorlist",
                            action="store_true",
                            help="no mirrorlist")
        # api arguments
        api = parser.add_argument_group("API")
        api.add_argument("-a", "--api",
                         action="store_true",
                         help="[--prefix] [--protocols] [--set-branch|--get-branch {-b <branch>}]")
        branch = api.add_mutually_exclusive_group()
        branch.add_argument("--get-branch",
                            action="store_true",
                            help="get-branch")
        branch.add_argument("--set-branch",
                            action="store_true",
                            help="set-branch")
        api.add_argument("--prefix",
                         type=str,
                         help="[--prefix {'$mnt'|'/some/path'}]")
        api.add_argument("--proto",
                         type=str,
                         nargs="+",
                         help="[--proto {all|http https ftp ftps}]")

        args = parser.parse_args()
        if len(sys.argv) == 1:
            parser.print_help()
            print("{}pacman-mirrors {}{}".format(txt.GS, __version__, txt.CE))
            sys.exit(0)

        if args.version:
            print("{}pacman-mirrors {}{}".format(txt.GS, __version__, txt.CE))
            sys.exit(0)

        if args.no_update:
            if self.config["no_update"] == "True":
                sys.exit(0)

        if os.getuid() != 0:
            print(".: {} {}".format(txt.ERR_CLR, txt.MUST_BE_ROOT))
            sys.exit(1)

        if args.country_list:
            self.country_list = True

        if args.method:
            self.config["method"] = args.method

        if args.branch:
            self.config["branch"] = args.branch

        if args.timeout:
            self.max_wait_time = args.timeout

        if args.quiet:
            self.quiet = True

        if args.update:
            self.sync = True

        if args.mirror_dir:
            self.config["work_dir"] = args.mirror_dir

        if args.output:
            if args.output[0] == "/":
                self.config["mirror_list"] = args.output
            else:
                self.config["mirror_list"] = os.getcwd() + "/" + args.output

        if args.interactive:
            self.interactive = True
            if not os.environ.get("DISPLAY") or not GTK_AVAILABLE:
                self.no_display = True

        if args.interactive and args.default:
            self.default = True

        # geoip and country are mutually exclusive
        if args.geoip:
            self.geoip = True
        if args.country and not args.geoip:
            self.custom = True
            if "," in args.country[0]:
                self.config["only_country"] = args.country[0].split(",")
            else:
                self.config["only_country"] = args.country

        if args.fasttrack:
            self.fasttrack = args.fasttrack
            self.geoip = False
            self.custom = False
            self.config["only_country"] = []

        if args.no_mirrorlist:
            self.no_mirrorlist = True

        if args.api:
            proto = False
            if args.proto:
                proto = True
                if args.proto == ["all"]:
                    self.config["protocols"] = []
                else:
                    if "," in args.proto[0]:
                        self.config["protocols"] = args.proto[0].split(",")
                    else:
                        self.config["protocols"] = args.proto
            if args.set_branch:
                if args.branch:
                    self.api_config(prefix=args.prefix, set_branch=True, protocols=proto)
            elif args.get_branch:
                if not args.branch:
                    self.api_config(prefix=args.prefix, get_branch=True)
            else:
                self.api_config(prefix=args.prefix, protocols=proto)

    def api_config(self, prefix=None, set_branch=False, get_branch=False, protocols=False):
        """Api functions
        :param prefix: prefix to the config paths
        :param set_branch: writes branch to pacman-mirrors.conf
        :param get_branch: exit with branch
        :param protocols: writes list of protocols to pacman-mirrors.con
        """
        if prefix:
            if "$" in prefix:
                prefix = os.environ.get(prefix)
            self.config["config_file"] = \
                prefix + self.config["config_file"]
            self.config["custom_file"] = \
                prefix + self.config["custom_file"]
            self.config["to_be_removed"] = \
                prefix + self.config["to_be_removed"]
            self.config["work_dir"] = \
                prefix + self.config["work_dir"]
            self.config["mirror_file"] = \
                prefix + self.config["to_be_removed"]
            self.config["mirror_list"] = \
                prefix + self.config["mirror_list"]
            self.config["status_file"] = \
                prefix + self.config["status_file"]
        if set_branch:
            configfn.api_write_branch(self.config["branch"],
                                      self.config["config_file"])
        if protocols:
            configfn.api_write_protocols(self.config["protocols"],
                                         self.config["config_file"])
        if get_branch:
            sys.exit(self.config["branch"])

    def build_common_mirror_list(self):
        """Generate common mirrorlist"""
        worklist = mirrorfn.filter_mirror_country(self.mirrors.mirrorlist,
                                                  self.selected_countries)
        if self.config["protocols"]:
            worklist = mirrorfn.filter_mirror_protocols(
                worklist, self.config["protocols"])
        if self.config["method"] == "rank":
            worklist = self.test_mirrors(worklist)
            worklist = sorted(worklist, key=itemgetter("resp_time"))
        else:
            shuffle(worklist)
        if worklist:
            filefn.output_mirror_list(self.config, worklist, quiet=self.quiet)
            if self.custom:
                configfn.modify_config(self.config, custom=self.custom)
            else:
                configfn.modify_config(self.config, custom=self.custom)
        else:
            print(".: {} {}".format(txt.WRN_CLR, txt.NO_SELECTION))
            print(".: {} {}".format(txt.INF_CLR, txt.NO_CHANGE))

    def build_fasttrack_mirror_list(self, number):
        """Fast-track the mirrorlist by filtering only up2date mirrors"""
        # randomize the load on up2date mirrors
        worklist = self.mirrors.mirrorlist
        shuffle(worklist)
        if self.config["protocols"]:
            worklist = mirrorfn.filter_mirror_protocols(
                worklist, self.config["protocols"])
        up2date = [item for item in worklist if item["branches"] == [1, 1, 1]]
        worklist = []
        print(".: {}: {} - {}".format(txt.INF_CLR,
                                      txt.QUERY_MIRRORS,
                                      txt.TAKES_TIME))
        counter = 0
        cols, lines = miscfn.terminal_size()
        for mirror in up2date:
            if not self.quiet:
                message = "   ..... {:<15}: {}: {}".format(
                    mirror["country"], mirror["last_sync"], mirror["url"])
                print("{:.{}}".format(message, cols), end="")
                sys.stdout.flush()
            resp_time = httpfn.get_mirror_response(mirror["url"],
                                                   maxwait=self.max_wait_time,
                                                   quiet=self.quiet)
            mirror["resp_time"] = resp_time
            if float(resp_time) > self.max_wait_time:
                if not self.quiet:
                    print("\r")
            else:
                if not self.quiet:
                    print("\r   {:<5}{}{} ".format(txt.GS, resp_time, txt.CE))
                worklist.append(mirror)
                counter += 1
            if counter == number:
                break
        worklist = sorted(worklist, key=itemgetter("resp_time"))
        if worklist:
            filefn.output_mirror_list(self.config, worklist, quiet=self.quiet)
        else:
            print(".: {} {}".format(txt.WRN_CLR, txt.NO_SELECTION))
            print(".: {} {}".format(txt.INF_CLR, txt.NO_CHANGE))

    def build_interactive_mirror_list(self):
        """Prompt the user to select the mirrors with a gui.
        * Outputs a pacman mirrorlist,
        * Outputs a "custom" mirror file
        * Modify the configuration file to use the "custom" file.
        """
        worklist = mirrorfn.filter_mirror_country(self.mirrors.mirrorlist,
                                                  self.selected_countries)
        if self.config["protocols"]:
            worklist = mirrorfn.filter_mirror_protocols(
                worklist, self.config["protocols"])
        if not self.default:
            if self.config["method"] == "rank":
                worklist = self.test_mirrors(worklist)
                worklist = sorted(worklist, key=itemgetter("resp_time"))
            else:
                shuffle(worklist)
        interactive_list = []
        for mirror in worklist:
            for protocol in enumerate(mirror["protocols"]):
                pos = mirror["url"].find(":")
                interactive_list.append({
                    "country": mirror["country"],
                    "resp_time": mirror["resp_time"],
                    "last_sync": mirror["last_sync"],
                    "url": "{}{}".format(protocol[1], mirror["url"][pos:])
                })
        if self.no_display:
            from . import consoleui as ui
        else:
            from . import graphicalui as ui
        interactive = ui.run(interactive_list,
                             self.config["method"] == "random",
                             self.default)
        if interactive.is_done:
            custom_list = interactive.custom_list
            if self.default and custom_list:
                if self.config["method"] == "rank":
                    custom_list = self.test_mirrors(custom_list)
                    custom_list = sorted(custom_list,
                                         key=itemgetter("resp_time"))
                else:
                    shuffle(custom_list)
            selected = []  # written to mirrorlist
            mirrorfile = []  # written to custom-mirror.json
            for item in custom_list:
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
                filefn.output_mirror_list(self.config,
                                          selected,
                                          custom=True,
                                          quiet=self.quiet,
                                          interactive=True)
                # always use "Custom" from interactive
                self.config["only_country"] = ["Custom"]
                configfn.modify_config(self.config, custom=True)
                print(".: {} {} {}".format(txt.INF_CLR,
                                           txt.RESET_CUSTOM_CONFIG,
                                           txt.RESET_TIP))
            else:
                print(".: {} {}".format(txt.WRN_CLR, txt.NO_SELECTION))
                print(".: {} {}".format(txt.INF_CLR, txt.NO_CHANGE))

    def disable_custom_config(self):
        """Perform reset of custom configuration"""
        self.config["only_country"] = []
        self.custom = False

    def list_all_countries(self):
        """List all available countries"""
        print("{}".format("\n".join(self.mirrors.countrylist)))

    def load_all_mirrors(self):
        """Load mirrors"""
        if self.config["only_country"] == ["all"]:
            self.disable_custom_config()

        # decision on custom or default
        if self.config["only_country"] == ["Custom"]:
            if validfn.custom_config_is_valid():
                self.custom = True
            else:
                self.disable_custom_config()
        else:
            self.selected_countries = self.config["only_country"]

        # decision on custom vs countries from conf or argument
        if self.custom and not self.selected_countries:
            self.load_custom_mirrors()
            self.selected_countries = self.mirrors.countrylist
        else:
            self.load_default_mirrors()
        # validate selection and build country list
        self.selected_countries = mirrorfn.build_country_list(
            self.selected_countries, self.mirrors.countrylist, self.geoip)

    def load_custom_mirrors(self):
        """Load available custom mirrors"""
        if self.default:
            self.load_default_mirrors()
        else:
            self.seed_mirrors(self.config["custom_file"])

    def load_default_mirrors(self):
        """Load all available mirrors"""
        (file, status) = filefn.return_mirror_filename(self.config)
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
        cols, lines = miscfn.terminal_size()
        http_wait = self.max_wait_time
        ssl_wait = self.max_wait_time * 2
        ssl_verify = self.config["ssl_verify"]
        for mirror in worklist:
            pos = mirror["url"].find(":")
            proto = mirror["url"][:pos]
            # for idx, proto in enumerate(mirror["protocols"]):
            #     mirror["url"] = "{}{}".format(proto, url)
            if not self.quiet:
                message = "   ..... {:<15}: {}".format(mirror["country"],
                                                       mirror["url"])
                print("{:.{}}".format(message, cols), end="")
                sys.stdout.flush()
            # https sometimes takes a short while for handshake
            if proto == "https" or proto == "ftps":
                self.max_wait_time = ssl_wait
            else:
                self.max_wait_time = http_wait
            # let's see how responsive you are
            resp_time = httpfn.get_mirror_response(mirror["url"],
                                                   maxwait=self.max_wait_time,
                                                   quiet=self.quiet,
                                                   ssl_verify=ssl_verify)
            mirror["resp_time"] = resp_time
            if float(resp_time) >= self.max_wait_time:
                if not self.quiet:
                    print("\r")
            else:
                if not self.quiet:
                    print("\r   {:<5}{}{} ".format(txt.GS, resp_time, txt.CE))
        return worklist

    def run(self):
        """Run"""
        (self.config, self.custom) = configfn.build_config()
        filefn.dir_must_exist(self.config["work_dir"])
        self.command_line_parse()
        self.network = httpfn.inet_conn_check()
        if self.network:
            httpfn.update_mirrors(self.config)
        else:
            # negative on network
            miscfn.internet_message()
            self.config["method"] = "random"  # use random instead of rank
            self.fasttrack = False  # using fasttrack is not possible
        if self.no_mirrorlist:
            exit(0)
        self.load_all_mirrors()
        if self.country_list:
            self.list_all_countries()
            exit(0)
        if self.fasttrack:
            self.build_fasttrack_mirror_list(self.fasttrack)
        elif self.interactive:
            self.build_interactive_mirror_list()
        else:
            self.build_common_mirror_list()
        if self.network and self.sync:
            subprocess.call(["pacman", "-Syy"])

if __name__ == "__main__":
    app = PacmanMirrors()
    app.run()
