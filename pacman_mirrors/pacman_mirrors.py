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
from . import apifn
from . import mirrorfn
from . import colors as color
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
        self.no_mirrorlist = False
        self.no_display = False
        self.quiet = False
        self.selected_countries = []  # users selected countries
        self.sync = False

    def command_line_parse(self):
        """Read the arguments of the command line"""
        parser = argparse.ArgumentParser(formatter_class=CustomHelpFormatter)
        # Method arguments
        methods = parser.add_argument_group("METHODS")
        methods.add_argument("-g", "--generate",
                             action="store_true",
                             help=txt.HLP_ARG_GENERATE)
        methods.add_argument("-f", "--fasttrack",
                             type=int,
                             metavar=txt.NUMBER,
                             help="{} {}".format(txt.HLP_ARG_FASTTRACK,
                                                 txt.OVERRIDE_OPT))
        methods.add_argument("-i", "--interactive",
                             action="store_true",
                             help=txt.HLP_ARG_INTERACTIVE)
        methods.add_argument("-d", "--default",
                             action="store_true",
                             help="Interactive: " + txt.HLP_ARG_DEFAULT)
        methods.add_argument("-m", "--method",
                             type=str,
                             choices=["rank", "random"],
                             help=txt.HLP_ARG_METHOD)
        country = parser.add_argument_group("COUNTRY")
        country.add_argument("-c", "--country",
                             type=str,
                             nargs="+",
                             help=txt.HLP_ARG_COUNTRY)
        country.add_argument("--geoip",
                             action="store_true",
                             help=txt.HLP_ARG_GEOIP)
        country.add_argument("-l", "--country-list", "--list",
                             action="store_true",
                             help=txt.HLP_ARG_LIST)
        # Branch arguments
        branch = parser.add_argument_group("BRANCH")
        only_one = branch.add_mutually_exclusive_group()
        only_one.add_argument("-b", "--branch",
                              type=str,
                              choices=["stable", "testing", "unstable"],
                              help=txt.HLP_ARG_BRANCH)
        only_one.add_argument("-G", "--get-branch",
                              action="store_true",
                              help=txt.HLP_ARG_API_GET_BRANCH)
        only_one.add_argument("-S", "--set-branch",
                              choices=["stable", "testing", "unstable"],
                              help=txt.HLP_ARG_API_SET_BRANCH)
        # Api arguments
        api = parser.add_argument_group("API")
        api.add_argument("-a", "--api",
                         action="store_true",
                         help="[-p PREFIX][-R][-S|-G BRANCH][-P PROTO [PROTO ...]]")
        api.add_argument("-p", "--prefix",
                         type=str,
                         help=txt.HLP_ARG_API_PREFIX + txt.PREFIX_TIP)
        api.add_argument("-P", "--proto", "--protocols",
                         choices=["all", "http", "https", "ftp", "ftps"],
                         type=str,
                         nargs="+",
                         help=txt.HLP_ARG_API_PROTOCOLS)
        api.add_argument("-R", "--re-branch",
                         action="store_true",
                         help=txt.HLP_ARG_API_RE_BRANCH)
        api.add_argument("-U", "--url",
                         type=str,
                         help=txt.HLP_ARG_API_URL)
        # Misc arguments
        misc = parser.add_argument_group("MISC")
        misc.add_argument("-q", "--quiet",
                          action="store_true",
                          help=txt.HLP_ARG_QUIET)
        misc.add_argument("-t", "--timeout",
                          type=int,
                          metavar=txt.SECONDS,
                          help=txt.HLP_ARG_TIMEOUT)
        misc.add_argument("-v", "--version",
                          action="store_true",
                          help=txt.HLP_ARG_VERSION)
        sync = misc.add_mutually_exclusive_group()
        sync.add_argument("-n", "--no-mirrorlist",
                          action="store_true",
                          help=txt.HLP_ARG_NO_MIRRORLIST)
        sync.add_argument("-y", "--sync",
                          action="store_true",
                          help=txt.HLP_ARG_SYNC)

        args = parser.parse_args()
        if len(sys.argv) == 1:
            print("pacman-mirrors version " + __version__)
            parser.print_help()
            sys.exit(0)

        if args.version:
            print("{}pacman-mirrors {}{}".format(color.GREEN, __version__, color.ENDCOLOR))
            sys.exit(0)

        if args.country_list:
            self.country_list = True

        if os.getuid() != 0:
            print(".: {} {}".format(txt.ERR_CLR, txt.MUST_BE_ROOT))
            sys.exit(1)

        if args.method:
            self.config["method"] = args.method

        if args.branch:
            self.config["branch"] = args.branch

        if args.timeout:
            self.max_wait_time = args.timeout

        if args.quiet:
            self.quiet = True

        if args.sync:
            self.sync = True

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
            getbranch = False
            rebranch = False
            url = args.url
            setbranch = bool(args.set_branch)
            if args.get_branch:
                getbranch = True
            if args.re_branch:
                rebranch = True
            if args.proto:
                proto = True
                if "all" in args.proto:
                    self.config["protocols"] = []
                else:
                    if "," in args.proto[0]:
                        self.config["protocols"] = args.proto[0].split(",")
                    else:
                        self.config["protocols"] = args.proto
            if args.set_branch:
                self.config["branch"] = args.set_branch

            self.api_config(prefix=args.prefix, set_branch=setbranch, re_branch=rebranch,
                            get_branch=getbranch, protocols=proto, url=url)

    def api_config(self, prefix=None, set_branch=False, re_branch=False,
                   get_branch=False, protocols=False, url=None):
        """Api functions
        :param prefix: prefix to the config paths
        :param set_branch: replace branch in pacman-mirrors.conf
        :param re_branch: replace branch in mirrorlist
        :param get_branch: sys.exit with branch
        :param protocols: replace protocols in pacman-mirrors.conf
        :param url: replace mirror url in mirrorlist
        """
        # Do not change the following sequence
        # Doing so will most certainly cause serious problems
        #   for any one relying on the api
        # Number 1
        if prefix:
            self.config["config_file"] = prefix + self.config["config_file"]
            self.config["custom_file"] = prefix + self.config["custom_file"]
            self.config["mirror_file"] = prefix + self.config["mirror_file"]
            self.config["mirror_list"] = prefix + self.config["mirror_list"]
            self.config["status_file"] = prefix + self.config["status_file"]
            self.config["work_dir"] = prefix + self.config["work_dir"]
            # to be removed long time after 2017-04-18
            self.config["to_be_removed"] = prefix + self.config["to_be_removed"]
            # end removal
        # Number 2
        if protocols:
            apifn.api_write_protocols(self.config["protocols"],
                                      self.config["config_file"],
                                      quiet=self.quiet)
        # Number 3
        if set_branch and not url:
            apifn.write_config_branch(self.config["branch"],
                                      self.config["config_file"],
                                      quiet=self.quiet)
        # Number 4
        if url:
            filefn.dir_must_exist(prefix + "/etc/pacman.d")
            mirror = [
                {
                    "url": apifn.check_url(url),
                    "country": "pkgbuild",
                    "protocols": [url[:url.find(":")]],
                    "resp_time": "00.00"
                 }
            ]
            filefn.output_mirror_list(self.config, mirror, quiet=self.quiet)
            sys.exit(0)
        # Number 5
        if re_branch:
            if not set_branch:
                print(".: {} {}".format(txt.ERR_CLR, txt.API_ERROR_BRANCH))
                sys.exit(1)
            apifn.write_mirrorlist_branch(self.config["branch"],
                                          self.config["config_file"],
                                          quiet=self.quiet)
        # Number 6
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
                    print("\r   {:<5}{}{} ".format(color.GREEN, resp_time, color.ENDCOLOR))
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
            mirror_list = []  # written to mirrorlist
            mirror_file = []  # written to custom-mirror.json
            custom_list = interactive.custom_list
            for item in custom_list:
                ipos = item["url"].find(":")
                iurl = item["url"][ipos:]
                for server in self.mirrors.mirrorlist:
                    spos = server["url"].find(":")
                    surl = server["url"][spos:]
                    if iurl == surl:
                        mirror_file.append({
                            "country": server["country"],
                            "protocols": server["protocols"],
                            "url": server["url"]
                        })
                        server["protocols"] = self.config["protocols"]
                        mirror_list.append(server)
            if self.default and mirror_list:
                if self.config["method"] == "rank":
                    mirror_list = self.test_mirrors(mirror_list)
                    mirror_list = sorted(mirror_list,
                                         key=itemgetter("resp_time"))
                else:
                    shuffle(mirror_list)
            if mirror_file:
                print("\n.: {} {}".format(txt.INF_CLR,
                                          txt.CUSTOM_MIRROR_LIST))
                print("--------------------------")
                # output mirror file
                jsonfn.write_json_file(mirror_file, self.config["custom_file"])
                print(".: {} {}: {}".format(txt.INF_CLR,
                                            txt.CUSTOM_MIRROR_FILE_SAVED,
                                            self.config["custom_file"]))
                # output pacman mirrorlist
                filefn.output_mirror_list(self.config,
                                          mirror_list,
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

    def output_country_list(self):
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

    def sort_mirror_countries(self):
        self.mirrors.mirrorlist = sorted(self.mirrors.mirrorlist, key=itemgetter("country"))
        self.mirrors.countrylist = sorted(self.mirrors.countrylist)

    def seed_mirrors(self, file, status=False):
        """Seed mirrors"""
        mirrors = filefn.read_mirror_file(file)
        # seed mirror object
        if status:
            self.mirrors.seed(mirrors, status=status)
        else:
            self.mirrors.seed(mirrors)
        # sort mirrors countrywise
        self.sort_mirror_countries()

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
            url = mirror["url"][pos:]
            for idx, proto in enumerate(mirror["protocols"]):
                mirror["url"] = "{}{}".format(proto, url)
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
                        print("\r   {:<5}{}{} ".format(color.GREEN, resp_time, color.ENDCOLOR))
        return worklist

    def run(self):
        """Run"""
        (self.config, self.custom) = configfn.build_config()
        filefn.dir_must_exist(self.config["work_dir"])
        self.command_line_parse()
        self.network = httpfn.inet_conn_check()
        if self.network:
            httpfn.update_mirrors(self.config, quiet=self.quiet)
        else:
            # negative on network
            if not self.quiet:
                miscfn.internet_message()
            self.config["method"] = "random"  # use random instead of rank
            self.fasttrack = False  # using fasttrack is not possible
        if self.no_mirrorlist:
            sys.exit(0)
        self.load_all_mirrors()
        if self.country_list:
            self.output_country_list()
            sys.exit(0)
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
