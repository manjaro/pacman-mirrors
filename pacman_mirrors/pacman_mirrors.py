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

import argparse
import importlib.util
import os
import platform
import shutil
import sys
from operator import itemgetter
from random import shuffle

import pacman_mirrors.functions.util
from pacman_mirrors import __version__
from pacman_mirrors.api import apifn
from pacman_mirrors.config import configuration as conf
from pacman_mirrors.constants import colors as color
from pacman_mirrors.constants import txt
from pacman_mirrors.functions import fileFn, configFn
from pacman_mirrors.functions import httpFn
from pacman_mirrors.functions import jsonFn
from pacman_mirrors.functions import validFn
from pacman_mirrors.functions import util
from pacman_mirrors.mirrors import mirrorfn
from pacman_mirrors.mirrors.mirror import Mirror
from pacman_mirrors.translation import i18n
from pacman_mirrors.translation.custom_help_formatter \
    import CustomHelpFormatter

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

    def command_line_parse(self):
        """Read the arguments of the command line"""

        args_summary = "[-h] [-f [{}]] [-i [-d]] [-m {}]\n" \
                       "\t\t[-c {} [{}...]] [--geoip] [-l]\n" \
                       "\t\t[-b {} | -G | -S/-B {}] [-a] [-p {}]\n" \
                       "\t\t[-P {} [{}...]] [-R] [-U {}]\n" \
                       "\t\t[-q] [-t {}] [-v] [-n]".format(txt.NUMBER,
                                                           txt.METHOD,
                                                           txt.COUNTRY,
                                                           txt.COUNTRY,
                                                           txt.BRANCH,
                                                           txt.BRANCH,
                                                           txt.PREFIX,
                                                           txt.PROTO,
                                                           txt.PROTO,
                                                           txt.URL,
                                                           txt.SECONDS)

        nusage = "\rVersion {}\n{}:\n pacman-mirrors".format(__version__, txt.USAGE)
        usage = "{} {}".format(nusage, args_summary)

        parser = argparse.ArgumentParser(formatter_class=CustomHelpFormatter,
                                         add_help=False, usage=usage)

        # Method arguments
        methods = parser.add_argument_group(txt.METHODS)
        methods.add_argument("-i", "--interactive",
                             action="store_true",
                             help=txt.HLP_ARG_INTERACTIVE)
        methods_exclusive = methods.add_mutually_exclusive_group()
        methods_exclusive.add_argument("-f", "--fasttrack",
                                       nargs="?",
                                       const=0,
                                       type=int,
                                       default=0,
                                       metavar=txt.NUMBER,
                                       help="{} {}".format(txt.HLP_ARG_FASTTRACK, txt.OVERRIDE_OPT))
        methods_exclusive.add_argument("-c", "--country",
                                       type=str,
                                       nargs="+",
                                       metavar=txt.COUNTRY,
                                       help=txt.HLP_ARG_COUNTRY)
        methods_exclusive.add_argument("--geoip",
                                       action="store_true",
                                       help=txt.HLP_ARG_GEOIP)
        # Branch arguments
        branch = parser.add_argument_group(txt.BRANCH)
        branch_exclusive = branch.add_mutually_exclusive_group()
        branch_exclusive.add_argument("-b", "--branch",
                                      type=str,
                                      choices=["stable", "testing", "unstable"],
                                      help=txt.HLP_ARG_BRANCH)
        branch_exclusive.add_argument("-G", "--get-branch",
                                      action="store_true",
                                      help="{}: {}".format(
                                          txt.API, txt.HLP_ARG_API_GET_BRANCH))
        branch_exclusive.add_argument("-S", "-B", "--set-branch",
                                      choices=["stable", "testing", "unstable"],
                                      help="{}: {}".format(
                                          txt.API, txt.HLP_ARG_API_SET_BRANCH))
        # Api arguments
        api = parser.add_argument_group(txt.API)
        api.add_argument("-a", "--api",
                         action="store_true",
                         help="[-p {}][-R][-S/-B|-G {}][-P {} [{} ...]]".format(
                             txt.PREFIX, txt.BRANCH, txt.PROTO, txt.PROTO))
        api.add_argument("-p", "--prefix",
                         type=str,
                         metavar=txt.PREFIX,
                         help="{}: {} {}".format(
                             txt.API, txt.HLP_ARG_API_PREFIX, txt.PREFIX_TIP))
        api.add_argument("-P", "--proto", "--protocols",
                         choices=["all", "http", "https", "ftp", "ftps"],
                         type=str,
                         nargs="+",
                         help="{}: {}".format(
                             txt.API, txt.HLP_ARG_API_PROTOCOLS))
        api.add_argument("-R", "--re-branch",
                         action="store_true",
                         help="{}: {}".format(
                             txt.API, txt.HLP_ARG_API_RE_BRANCH))
        api.add_argument("-U", "--url",
                         type=str,
                         metavar=txt.URL,
                         help="{}: {}".format(
                             txt.API, txt.HLP_ARG_API_URL))
        """
        Misc arguments for changing various aspects
        """
        misc = parser.add_argument_group(txt.MISC)
        misc.add_argument("-d", "--default",
                          action="store_true",
                          help="INTERACTIVE: " + txt.HLP_ARG_DEFAULT)
        misc.add_argument("-h", "--help",
                          action="store_true")
        misc.add_argument("-l", "--list", "--country-list",
                          action="store_true",
                          help=txt.HLP_ARG_LIST)
        misc.add_argument("-m", "--method",
                          type=str,
                          choices=["rank", "random"],
                          help=txt.HLP_ARG_METHOD)
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
        misc.add_argument("-n", "--no-mirrorlist",
                          action="store_true",
                          help=txt.HLP_ARG_NO_MIRRORLIST)

        args = parser.parse_args()

        """
        #############################################################
        No root required
        #############################################################
        """
        if len(sys.argv) == 1 or args.help:
            parser.print_help()
            sys.exit(0)

        if args.version:
            print("Version {}".format(__version__))
            sys.exit(0)

        if args.list:
            self.output_country_pool_console()
            sys.exit(0)

        if args.api and args.get_branch:
            self.api_config(get_branch=True)
            sys.exit(0)

        """
        #############################################################
        Root required
        #############################################################
        """
        if os.getuid() != 0:
            print(".: {} {}".format(
                txt.ERR_CLR, txt.MUST_BE_ROOT))
            sys.exit(1)

        if args.branch:
            self.config["branch"] = args.branch

        if args.geoip:
            self.geoip = True

        if args.method:
            self.config["method"] = args.method

        if args.no_mirrorlist:
            self.no_mirrorlist = True

        if args.quiet:
            self.quiet = True

        if args.timeout:
            self.max_wait_time = args.timeout

        """
        Generation methods
        """
        if args.country:
            self.geoip = False
            if "," in args.country[0]:
                self.config["country_pool"] = args.country[0].split(",")
            else:
                self.config["country_pool"] = args.country

            if self.config["country_pool"] == ["all"]:
                self.delete_custom_pool()

        if args.fasttrack:
            self.fasttrack = args.fasttrack
            self.geoip = False
            self.config["method"] = "rank"

        if args.interactive:
            self.interactive = True
            if args.default:
                self.default = True
            if os.environ.get("XDG_SESSION_TYPE") == "wayland" or not os.environ.get("DISPLAY") or not GTK_AVAILABLE:
                self.no_display = True

        """
        API handling
        Setup variables for passing to the api_config function
        """
        if args.api:
            getbranch = False
            rebranch = False
            url = args.url
            setbranch = args.set_branch
            setprotocols = bool(args.proto)
            if args.get_branch:
                getbranch = True
            if args.re_branch:
                rebranch = True
            if args.proto:
                if "all" in args.proto:
                    self.config["protocols"] = []
                else:
                    if "," in args.proto:
                        self.config["protocols"] = args.proto.split(",")
                    else:
                        self.config["protocols"] = args.proto

            self.api_config(set_pfx=args.prefix,
                            set_branch=setbranch,
                            re_branch=rebranch,
                            get_branch=getbranch,
                            set_protocols=setprotocols,
                            set_url=url)

    def api_config(self, set_pfx=None, set_branch=None, re_branch=False,
                   get_branch=False, set_protocols=False, set_url=None):
        """
        Api configuration function
        :param set_pfx: prefix to the config paths
        :param set_branch: replace branch in pacman-mirrors.conf
        :param re_branch: replace branch in mirrorlist
        :param get_branch: sys.exit with branch
        :param set_protocols: replace protocols in pacman-mirrors.conf
        :param set_url: replace mirror url in mirrorlist
        """
        if set_url is None:
            set_url = ""

        if set_pfx is None:
            set_pfx = ""

        """
        # Order of API tasks does matter
        # First API task
        """
        if get_branch:
            print(self.config["branch"])
            return

        """
        # apply api configuration to internal configuration object
        # Apply prefix if present
        """
        if set_pfx:
            set_pfx = apifn.sanitize_prefix(set_pfx)
            self.config["config_file"] = set_pfx + self.config["config_file"]
            self.config["custom_file"] = set_pfx + self.config["custom_file"]
            self.config["mirror_file"] = set_pfx + self.config["mirror_file"]
            self.config["mirror_list"] = set_pfx + self.config["mirror_list"]
            self.config["status_file"] = set_pfx + self.config["status_file"]
            self.config["work_dir"] = set_pfx + self.config["work_dir"]

        """
        # Second API task: Set branch
        """
        if set_branch:
            # Apply branch to internal config
            self.config["branch"] = set_branch
            self.i686_check(write=False)
            """
            # pacman-mirrors.conf could absent so check for it
            """
            if not fileFn.check_existance_of(self.config["config_file"]):
                """
                # Copy from host system
                """
                fileFn.create_dir(set_pfx + "/etc")
                shutil.copyfile("/etc/pacman-mirrors.conf",
                                self.config["config_file"])
                """
                # Normalize config
                """
                apifn.normalize_config(self.config["config_file"])
            """
            # Write branch to config
            """
            apifn.write_config_branch(self.config["branch"],
                                      self.config["config_file"],
                                      quiet=self.quiet)
        """
        # Third API task: Create a mirror list
        """
        if set_url:
            """
            # mirror list dir could absent so check for it
            """
            fileFn.create_dir(set_pfx + "/etc/pacman.d")
            mirror = [
                {
                    "url": apifn.sanitize_url(set_url),
                    "country": "BUILDMIRROR",
                    "protocols": [set_url[:set_url.find(":")]],
                    "resp_time": "00.00"
                }
            ]
            fileFn.write_mirror_list(self.config, mirror, quiet=self.quiet)
            # exit gracefully
            sys.exit(0)
        """
        # Fourth API task: Write protocols to config
        """
        if set_protocols:
            apifn.write_protocols(self.config["protocols"],
                                  self.config["config_file"],
                                  quiet=self.quiet)
        """
        # Fifth API task: Rebranch the mirrorlist
        """
        if re_branch:
            if not set_branch:
                print(".: {} {}".format(txt.ERR_CLR, txt.API_ERROR_BRANCH))
                sys.exit(1)
            apifn.write_mirrorlist_branch(self.config["branch"],
                                          self.config["config_file"],
                                          quiet=self.quiet)

    def build_common_mirror_list(self):
        """
        Generate common mirrorlist
        """
        """
        Create a list based on the content of selected_countries
        """
        mirror_selection = mirrorfn.filter_mirror_country(self.mirrors.mirror_pool,
                                                          self.selected_countries)
        """
        Check the length of selected_countries against the full countrylist
        If selected_countries is the lesser then we build a custom pool file
        """
        if len(self.selected_countries) < len(self.mirrors.country_pool):
            try:
                _ = self.selected_countries[0]
                self.output_custom_mirror_pool_file(mirror_selection)
            except IndexError:
                pass
        """
        Prototol filtering if applicable
        """
        try:
            _ = self.config["protocols"][0]
            mirror_selection = mirrorfn.filter_mirror_protocols(
                mirror_selection, self.config["protocols"])
        except IndexError:
            pass

        """
        only list mirrors which are up-to-date for users selected branch
        by removing not up-to-date mirrors from the list
        UP-TO-DATE FILTERING NEXT
        """
        mirror_selection = self.filter_user_branch(mirror_selection)

        if self.config["method"] == "rank":
            mirror_selection = self.test_mirrors(mirror_selection)
            mirror_selection = sorted(mirror_selection,
                                      key=itemgetter("resp_time"))
        else:
            shuffle(mirror_selection)

        """
        Try to write mirrorlist
        """
        try:
            _ = mirror_selection[0]
            self.output_mirror_list(mirror_selection)
            if self.custom:
                print(".: {} {} 'sudo {}'".format(txt.INF_CLR,
                                                  txt.REMOVE_CUSTOM_CONFIG,
                                                  txt.RESET_ALL))
        except IndexError:
            print(".: {} {}".format(txt.WRN_CLR, txt.NO_SELECTION))
            print(".: {} {}".format(txt.INF_CLR, txt.NO_CHANGE))

    def build_fasttrack_mirror_list(self, number):
        """
        Fast-track the mirrorlist by filtering only up-to-date mirrors
        The function takes into account the branch selected by the user
          either on commandline or in pacman-mirrors.conf.
        The function returns a filtered list consisting of a number of mirrors
        Only mirrors from the active mirror file is used
          either mirrors.json or custom-mirrors.json
        """
        # randomize the load on up-to-date mirrors
        worklist = self.mirrors.mirror_pool
        shuffle(worklist)
        if self.config["protocols"]:
            worklist = mirrorfn.filter_mirror_protocols(
                worklist, self.config["protocols"])

        """
        Only pick mirrors which are up-to-date for users selected branch
          by removing not up-to-date mirrors from the list
        UP-TO-DATE FILTERING NEXT
        """
        up_to_date_mirrors = self.filter_user_branch(worklist)
        worklist = []
        print(".: {}: {} - {}".format(txt.INF_CLR,
                                      txt.QUERY_MIRRORS,
                                      txt.TAKES_TIME))
        counter = 0
        cols, lines = pacman_mirrors.functions.util.terminal_size()
        for mirror in up_to_date_mirrors:
            if not self.quiet:
                message = "   ..... {:<15}: {}: {}".format(
                    mirror["country"], mirror["last_sync"], mirror["url"])
                print("{:.{}}".format(message, cols), end="")
                sys.stdout.flush()
            resp_time = httpFn.get_mirror_response(mirror["url"],
                                                   maxwait=self.max_wait_time,
                                                   quiet=self.quiet)
            mirror["resp_time"] = resp_time
            if float(resp_time) > self.max_wait_time:
                if not self.quiet:
                    print("\r")
            else:
                if not self.quiet:
                    print("\r   {:<5}{}{} ".format(color.GREEN,
                                                   resp_time,
                                                   color.ENDCOLOR))
                worklist.append(mirror)
                counter += 1
            """
            Equality check will stop execution
            when the desired number is reached.
            In the possible event the first mirror's
            response time exceeds the predefined response time,
            the loop would stop execution if the check for zero is not present
            """
            if counter is not 0 and counter == number:
                break
        worklist = sorted(worklist,
                          key=itemgetter("resp_time"))
        """
        Try to write mirrorlist
        """
        try:
            _ = worklist[0]
            self.output_mirror_list(worklist)
        except IndexError:
            print(".: {} {}".format(txt.WRN_CLR, txt.NO_SELECTION))
            print(".: {} {}".format(txt.INF_CLR, txt.NO_CHANGE))

    def build_interactive_mirror_list(self):
        """
        Prompt the user to select the mirrors with a gui.
        Outputs a "custom" mirror file
        Modify the configuration file to use the "custom" file.
        Outputs a pacman mirrorlist,
        """

        """
        It would seem reasonable to implement a filter
        based on the users branch and the mirrors update status
        On the other hand, the interactive mode is for the user
        to have total control over the mirror file.
        So though it might seem prudent to only include updated mirrors,
        we will not do it when user has selected interactive mode.
        The final mirrorfile will include all mirrors selected by the user
        The final mirrorlist will exclude (if possible) mirrors not up-to-date
        """
        worklist = mirrorfn.filter_mirror_country(self.mirrors.mirror_pool,
                                                  self.selected_countries)
        """
        If config.protols has content, that is a user decision and as such
        it has nothing to do with the reasoning regarding mirrors
        which might or might not be up-to-date
        """
        try:
            _ = self.config["protocols"][0]
            worklist = mirrorfn.filter_mirror_protocols(
                worklist, self.config["protocols"])
        except IndexError:
            pass

        # rank or shuffle the mirrorlist before showing the ui
        if not self.default:
            if self.config["method"] == "rank":
                worklist = self.test_mirrors(worklist)
                worklist = sorted(worklist, key=itemgetter("resp_time"))
            else:
                shuffle(worklist)
        interactive_list = []
        """
        Create a list for display in ui.
        The gui and the console ui expect the supplied list
        to be in the old country dictionary format.
        {
            "country": "country_name",
            "resp_time": "m.sss",
            "last_sync": "HH:MM",
            "url": "http://server/repo/"
        }
        Therefor we have to create a list in the old format,
        thus avoiding rewrite of the ui and related functions.
        We subseqently need to translate the result into:
        a. a mirrorfile in the new json format,
        b. a mirrorlist in pacman format.
        """
        for mirror in worklist:
            # create an entry for all protocols related to a mirror
            for protocol in enumerate(mirror["protocols"]):
                interactive_list.append({
                    "country": mirror["country"],
                    "resp_time": mirror["resp_time"],
                    "last_sync": mirror["last_sync"],
                    "url": "{}{}".format(protocol[1],
                                         util.strip_protocol(mirror["url"]))
                })
        #
        # import the right ui
        if self.no_display:
            # in console mode
            from pacman_mirrors.dialogs import consoleui as ui
        else:
            # gobject introspection is present and accounted for
            from pacman_mirrors.dialogs import graphicalui as ui
        interactive = ui.run(interactive_list,
                             self.config["method"] == "random",
                             self.default)
        # process user choices
        if interactive.is_done:
            mirror_list = []  # to be written to mirrorlist
            mirror_selection = []  # to be written to custom-mirror.json
            custom_list = interactive.custom_list  # grabbing a copy
            # loop custom list
            for custom in custom_list:
                # get url without protocol
                custom_string = util.strip_protocol(custom["url"])
                # locate mirror in the full mirrorlist
                for mirror in self.mirrors.mirror_pool:
                    mirror_string = util.strip_protocol(mirror["url"])
                    # compare urls
                    if custom_string == mirror_string:
                        #
                        # create list for mirror file
                        mirror_selection.append({
                            "country": mirror["country"],
                            "protocols": mirror["protocols"],
                            "url": mirror["url"]
                        })
                        #
                        # create list for mirror list
                        try:
                            # assign user defined protocol if exist
                            _ = self.config["protocols"][0]
                            mirror["protocols"] = self.config["protocols"]
                        except IndexError:
                            pass
                        mirror_list.append(mirror)
            """
            Try selected method on the mirrorlist
            """
            try:
                _ = mirror_list[0]
                if self.default:
                    if self.config["method"] == "rank":
                        mirror_list = self.test_mirrors(mirror_list)
                        mirror_list = sorted(mirror_list,
                                             key=itemgetter("resp_time"))
                    else:
                        shuffle(mirror_list)
            except IndexError:
                pass

            """
            Try to write the mirrorfile and mirrorlist
            """
            try:
                _ = mirror_selection[0]
                self.custom = True
                self.config["country_pool"] = ["Custom"]
                self.output_custom_mirror_pool_file(mirror_selection)
                """
                Writing the final mirrorlist
                only write mirrors which are up-to-date for users selected branch
                UP-TO-DATE FILTERING NEXT
                """
                mirror_list = self.filter_user_branch(mirror_list)
                """
                Try writing mirrorlist
                If no up-to-date mirrors exist for users branch
                
                """
                try:
                    _ = mirror_list[0]
                    self.output_mirror_list(mirror_list)
                except IndexError:
                    raise IndexError
            except IndexError:
                print(".: {} {}".format(txt.WRN_CLR, txt.NO_SELECTION))
                print(".: {} {}".format(txt.INF_CLR, txt.NO_CHANGE))

    def check_custom_mirror_pool(self):
        """
        Custom mirror pool or countries from CLI
        :return: True/False
        """
        if validFn.custom_config_is_valid():
            self.custom = True
        else:
            self.selected_countries = self.config["country_pool"]
        return self.custom

    def delete_custom_pool(self):
        """
        Delete custom mirror pool
        """
        self.custom = False
        self.config["country_pool"] = []
        fileFn.delete_file(self.config["custom_file"])

    def filter_user_branch(self, mirror_pool):
        """
        Filter mirrorlist on users branch and branch sync state
        """
        for idx, branch in enumerate(conf.BRANCHES):
            if self.config["x32"]:
                config_branch = self.config["branch"][4:]
            else:
                config_branch = self.config["branch"]
            if branch == config_branch:
                filtered = []
                for mirror in mirror_pool:
                    try:
                        if mirror["branches"][idx] == 1:
                            filtered.append(mirror)
                    except IndexError:
                        pass
                if len(filtered) > 0:
                    return filtered
        return mirror_pool

    def load_all_mirrors(self):
        """
        Load all mirrors from active mirror pool
        """
        if self.check_custom_mirror_pool() and not self.config["country_pool"]:
            self.load_custom_mirror_pool()
            self.selected_countries = self.mirrors.country_pool
        else:
            if self.config["country_pool"]:
                self.selected_countries = self.config["country_pool"]
            self.load_default_mirror_pool()
        """
        Validate the list of selected countries        
        """
        self.selected_countries = mirrorfn.build_country_list(
            self.selected_countries, self.mirrors.country_pool, self.geoip)

    def load_custom_mirror_pool(self):
        """
        Load available custom mirrors and update their status from status.json
        If user request the default mirror pool load the default pool
        """
        if self.default:
            self.load_default_mirror_pool()
        else:
            self.seed_mirrors(self.config["custom_file"])
            self.mirrors.mirror_pool = mirrorfn.set_custom_mirror_status(
                self.config, self.mirrors.mirror_pool)

    def load_default_mirror_pool(self):
        """
        Load all available mirrors
        """
        (file, status) = fileFn.return_mirror_filename(self.config)
        self.seed_mirrors(file, status)

    def output_country_pool_console(self):
        """
        List all available countries
        """
        self.load_default_mirror_pool()
        print("{}".format("\n".join(self.mirrors.country_pool)))

    def output_custom_mirror_pool_file(self, selected_mirrors):
        """
        Output selected mirrors to custom mirror file
        :param selected_mirrors:
        :return:
        """
        print("\n.: {} {}".format(txt.INF_CLR,
                                  txt.CUSTOM_MIRROR_LIST))
        print("--------------------------")
        # output mirror file
        jsonFn.write_json_file(selected_mirrors,
                               self.config["custom_file"])
        print(".: {} {}: {}".format(txt.INF_CLR,
                                    txt.CUSTOM_MIRROR_FILE_SAVED,
                                    self.config["custom_file"]))

    def output_mirror_list(self, selected_servers):
        """
        Outputs selected servers to mirrorlist
        :param selected_servers:
        """
        if self.custom:
            fileFn.write_mirror_list(self.config,
                                     selected_servers,
                                     custom=self.custom,
                                     quiet=self.quiet,
                                     interactive=True)
        else:
            fileFn.write_mirror_list(self.config,
                                     selected_servers,
                                     quiet=self.quiet)

    def sort_mirror_countries(self):
        self.mirrors.mirror_pool = sorted(self.mirrors.mirror_pool,
                                          key=itemgetter("country"))
        self.mirrors.country_pool = sorted(self.mirrors.country_pool)

    def seed_mirrors(self, file, status=False):
        """
        Seed mirrors
        """
        mirrors = fileFn.read_mirror_file(file)
        # seed mirror object
        if status:
            self.mirrors.seed(mirrors, status=status)
        else:
            self.mirrors.seed(mirrors)
        # sort mirrors country wise
        self.sort_mirror_countries()

    def test_mirrors(self, worklist):
        """
        Query server for response time
        """
        if self.custom:
            print(".: {} {}".format(txt.INF_CLR,
                                    txt.USING_CUSTOM_FILE))
        else:
            print(".: {} {}".format(txt.INF_CLR,
                                    txt.USING_DEFAULT_FILE))
        print(".: {} {} - {}".format(txt.INF_CLR,
                                     txt.QUERY_MIRRORS,
                                     txt.TAKES_TIME))
        cols, lines = pacman_mirrors.functions.util.terminal_size()
        # set connection timeouts
        http_wait = self.max_wait_time
        ssl_wait = self.max_wait_time * 2
        ssl_verify = self.config["ssl_verify"]
        for mirror in worklist:
            colon = mirror["url"].find(":")
            url = mirror["url"][colon:]
            for idx, proto in enumerate(mirror["protocols"]):
                mirror["url"] = "{}{}".format(proto, url)
                if not self.quiet:
                    message = "   ..... {:<15}: {}".format(mirror["country"],
                                                           mirror["url"])
                    print("{:.{}}".format(message, cols), end="")
                    sys.stdout.flush()
                # https sometimes takes longer for handshake
                if proto == "https" or proto == "ftps":
                    self.max_wait_time = ssl_wait
                else:
                    self.max_wait_time = http_wait
                # let's see how responsive you are
                mirror["resp_time"] = httpFn.get_mirror_response(
                    mirror["url"], maxwait=self.max_wait_time,
                    quiet=self.quiet, ssl_verify=ssl_verify)

                if float(mirror["resp_time"]) >= self.max_wait_time:
                    if not self.quiet:
                        print("\r")
                else:
                    if not self.quiet:
                        print("\r   {:<5}{}{} ".format(color.GREEN,
                                                       mirror["resp_time"],
                                                       color.ENDCOLOR))
        return worklist

    def i686_check(self, write=False):
        if platform.machine() == "i686":
            self.config["x32"] = True
            if "x32" not in self.config["branch"]:
                self.config["branch"] = "x32-{}".format(self.config["branch"])
                if write:
                    apifn.write_config_branch(self.config["branch"], self.config["config_file"], quiet=True)

    def run(self):
        """
        Run
        # Build internal config dictionary
        # Returns the config dictionary and true/false on custom
        # Parse commandline
        # i686 check - change branch to x32-$branch
        # Check network
        # Check if mirrorlist is not to be touched - normal exit
        # Handle missing network
        """
        (self.config, self.custom) = configFn.build_config()
        fileFn.create_dir(self.config["work_dir"])
        self.command_line_parse()
        self.i686_check(write=True)
        if not configFn.verify_config(self.config):
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
        self.load_all_mirrors()
        """
        # Decide which type of mirrorlist to create
        * Fasttrack
        * Interactive
        * Default
        """
        if self.fasttrack:
            self.build_fasttrack_mirror_list(self.fasttrack)
        elif self.interactive:
            self.build_interactive_mirror_list()
        else:
            self.build_common_mirror_list()


if __name__ == "__main__":
    app = PacmanMirrors()
    app.run()
