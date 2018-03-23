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
# Authors: Frede Hundewadt <echo ZmhAbWFuamFyby5vcmcK | base64 -d>

"""Pacman-Mirrors Command Line Parser"""

import argparse
import os
import sys

from pacman_mirrors import __version__
from pacman_mirrors.api import api_handler
from pacman_mirrors.functions import customFn
from pacman_mirrors.constants import txt
from pacman_mirrors.functions import outputFn
from pacman_mirrors.translation.custom_help_formatter \
    import CustomHelpFormatter


def parse_command_line(self, gtk_available):
    """Read the arguments of the command line"""

    args_summary = "[-h] [-f [{}]] [-i [-d]] [-m {}]\n" \
                   "\t\t[-c {} [{}...] | [--geoip]]\n" \
                   "\t\t[-l] [-lc] [-q] [-t {}] [-v] [-n]\n" \
                   "\t\t[--api] [-S/-B {}] [-p {}]\n" \
                   "\t\t\t[-P {} [{}...]] [-R] [-U {}]\n".format(txt.NUMBER,
                                                                 txt.METHOD,
                                                                 txt.COUNTRY,
                                                                 txt.COUNTRY,
                                                                 txt.SECONDS,
                                                                 txt.BRANCH,
                                                                 txt.PREFIX,
                                                                 txt.PROTO,
                                                                 txt.PROTO,
                                                                 txt.URL)

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
    methods_exclusive.add_argument("-g", "--geoip",
                                   action="store_true",
                                   help=txt.HLP_ARG_GEOIP)
    # Api arguments
    api = parser.add_argument_group(txt.API)
    api.add_argument("-a", "--api",
                     action="store_true",
                     help="[-p {}][-R][-S/-B|-G {}][-P {} [{} ...]]".format(
                         txt.PREFIX, txt.BRANCH, txt.PROTO, txt.PROTO))
    api.add_argument("-S", "-B", "--set-branch",
                     choices=["stable", "testing", "unstable"],
                     help="{}: {}".format(
                         txt.API, txt.HLP_ARG_API_SET_BRANCH))
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
    Misc arguments
    """
    misc = parser.add_argument_group(txt.MISC)
    misc.add_argument("-G", "--get-branch",
                      action="store_true",
                      help="{}".format(txt.HLP_ARG_API_GET_BRANCH))
    misc.add_argument("-d", "--default",
                      action="store_true",
                      help="INTERACTIVE: " + txt.HLP_ARG_DEFAULT)
    misc.add_argument("-h", "--help",
                      action="store_true")
    misc.add_argument("-l", "--list", "--country-list",
                      action="store_true",
                      help=txt.HLP_ARG_LIST)
    misc.add_argument("-lc", "--country-config",
                      action="store_true",
                      help="lists configured mirror countries")
    misc.add_argument("-m", "--method",
                      type=str,
                      choices=["rank", "random"],
                      help=txt.HLP_ARG_METHOD)
    misc.add_argument("-n", "--no-mirrorlist",
                      action="store_true",
                      help=txt.HLP_ARG_NO_MIRRORLIST)
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
        outputFn.console_default_country_pool(self)
        sys.exit(0)

    if args.country_config:
        outputFn.console_custom_country_pool(self)
        sys.exit(0)

    if args.get_branch:
        print(self.config["branch"])
        sys.exit(0)

    """
    #############################################################
    Validate arg combinations
    #############################################################        
    """
    """
    If --set-branch, --protocols, --url, --prefix and not --api reject 
    """
    if args.set_branch or args.proto or args.url or args.prefix:
        if not args.api:
            print(".: {} {}".format(txt.ERR_CLR, txt.API_ARGUMENTS_ERROR))
            sys.exit(1)

    """
    If --default and not --interactive reject
    """
    if args.default:
        if not args.interactive:
            print(".: {} {}".format(txt.ERR_CLR, txt.INTERACTIVE_ARGUMENTS_ERROR))
            sys.exit(1)

    """
    #############################################################
    Root required
    #############################################################
    """
    if os.getuid() != 0:
        print(".: {} {}".format(
            txt.ERR_CLR, txt.MUST_BE_ROOT))
        sys.exit(1)

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
            customFn.delete_custom_pool(self)

    if args.fasttrack:
        self.fasttrack = args.fasttrack
        self.geoip = False
        self.config["method"] = "rank"

    if args.interactive:
        self.interactive = True
        if args.default:
            self.default = True
        if os.environ.get("XDG_SESSION_TYPE") == "wayland" or not os.environ.get("DISPLAY") or not gtk_available:
            self.no_display = True

    """
    API handling
    Setup variables for passing to the api_config function
    """
    if args.api:
        rebranch = False
        url = args.url
        setbranch = args.set_branch
        setprotocols = bool(args.proto)

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

        api_handler.api_config(self, set_pfx=args.prefix,
                               set_branch=setbranch, re_branch=rebranch,
                               set_protocols=setprotocols, set_url=url)
