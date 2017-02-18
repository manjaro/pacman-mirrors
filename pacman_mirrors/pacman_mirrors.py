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
import tempfile
from operator import itemgetter
from pacman_mirrors import __version__
from random import shuffle
# CHANGE CONTENT IN configuration
from .configuration import DEVELOPMENT, DESCRIPTION
from .configuration import CONFIG_FILE, CUSTOM_FILE, FALLBACK, \
    MIRROR_DIR, MIRROR_LIST, MIRROR_FILE, STATUS_FILE, REPO_ARCH
from .custom_help_formatter import CustomHelpFormatter
from .filefn import FileFn
from .httpfn import HttpFn
from .jsonfn import JsonFn
from .mirror import Mirror
from .mirrorfn import MirrorFn
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
        self.bad_servers = []         # timeout > max_wait_time
        self.good_servers = []        # respond updated < 24h
        self.random_servers = []
        self.resp_servers = []        # respond updated > 24h
        self.only_country = []        # users selected countries
        # Decisions
        self.custom = False
        self.geolocation = False
        self.interactive = False
        self.manjaro_online = True
        self.no_display = False
        self.quiet = False
        # Time out
        self.max_wait_time = 2
        self.config = {}

    @staticmethod
    def debug(where, what, value):
        print("\n{} @Function {} -> Object {} = {}".format(txt.DBG_CLR, where, what, value))

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
        args = parser.parse_args()

        if len(sys.argv) == 1:
            parser.print_help()
            exit(0)

        if args.version:
            if DEVELOPMENT:
                print("pacman-mirrors {}".format(__version__) + DESCRIPTION)
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
            self.geolocation = True

        if args.country and not args.geoip:
            self.config["only_country"] = args.country.split(",")

    def gen_mirror_list_common(self):
        """Generate common mirrorlist"""
        server_list = self.good_servers + self.resp_servers + self.bad_servers
        if self.config["method"] == "random":
            server_list = self.mirrors.mirrorlist

        if server_list:
            server_list = sorted(server_list, key=itemgetter("resp_time"))
            self.output_mirror_list(server_list, write_file=True)
            if self.custom:
                self.modify_config(custom=True)
            else:
                self.modify_config()
        else:
            print("\n.: {}: {}\n".format(txt.WRN_CLR, txt.ERR_NO_MIRRORS))

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
                self.output_mirror_list(selected, write_file=True)
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
            self.validate_mirror()
        elif self.config["method"] == "random":
            print(".: {} {}".format(txt.INF_CLR, txt.INF_RANDOMIZE_SERVERS))
            self.mirrors.randomize()

    @staticmethod
    def load_conf():
        """Get config informations"""
        # initialising defaults
        # information which can differ from these defaults
        # is fetched from config file
        config = {
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
                            config["method"] = value
                        elif key == "Branch":
                            config["branch"] = value
                        elif key == "OnlyCountry":
                            config["only_country"] = value.split(",")
                        elif key == "MirrorlistsDir":
                            config["mirror_dir"] = value
                        elif key == "OutputMirrorlist":
                            config["mirror_list"] = value
                        elif key == "NoUpdate":
                            config["no_update"] = value
        except (PermissionError, OSError) as err:
            print(".: {} {}: {}: {}".format(txt.ERR_CLR,
                                            txt.ERR_FILE_READ,
                                            err.filename,
                                            err.strerror))
        return config

    def load_mirror_file(self):
        """Load mirror file"""
        seed_status = False
        if FileFn.check_file(STATUS_FILE):
            seed_status = True
            servers = JsonFn.read_json_file(STATUS_FILE, dictionary=True)
        elif FileFn.check_file(MIRROR_FILE):
            servers = JsonFn.read_json_file(MIRROR_FILE, dictionary=True)
        else:
            servers = JsonFn.read_json_file(FALLBACK, dictionary=True)
        if seed_status:
            self.mirrors.seed(servers, seed_status)
        else:
            self.mirrors.seed(servers)

    def mirror_to_server_list(self, mirror):
        """Append mirror to relevant list based on elapsed hours
        :param: mirror: object
        :param: last_sync: mirror last sync
        """
        elapsed_hours = int(mirror["last_sync"][:-3])
        if elapsed_hours <= int(txt.LASTSYNC_OK[:-3]):
            self.good_servers.append(mirror)
        elif elapsed_hours <= int(txt.LASTSYNC_NA[:-3]):
            self.resp_servers.append(mirror)
        elif elapsed_hours == int(txt.SERVER_BAD[:-3]):
            self.bad_servers.append(mirror)

    def modify_config(self, custom=False):
        """Modify configuration"""
        if not custom:
            # remove custom mirror file
            if os.path.isfile(CUSTOM_FILE):
                os.remove(CUSTOM_FILE)
        self.write_custom_config(CONFIG_FILE, self.config["only_country"], custom)

    def output_mirror_list(self, servers, write_file=False):
        """Write servers to /etc/pacman.d/mirrorlist
        :param: servers: list of servers to write
        :param: write_file: if "True" the list is written to disk
        """
        try:
            with open(self.config["mirror_list"], "w") as outfile:
                if write_file:
                    print(".: {} {}".format(txt.INF_CLR, txt.INF_MIRROR_LIST_WRITE))
                    # write list header
                    MirrorFn.write_mirrorlist_header(outfile)
                for server in servers:
                    if write_file:
                        url = server["url"]
                        for protocol in enumerate(server["protocols"]):
                            pos = url.find(":")
                            server["url"] = "{}{}{}{}".format(protocol[1],
                                                              url[pos:],
                                                              self.config["branch"],
                                                              REPO_ARCH)
                            # write list entry
                            MirrorFn.write_mirrorlist_entry(outfile, server)
                            if not self.quiet:
                                print("   {}{:<15}{} : {}".format(txt.YS, server["country"], txt.CE, server["url"]))
                print(".: {} {}: {}".format(txt.INF_CLR, txt.INF_MIRROR_LIST_SAVED, self.config["mirror_list"]))
        except OSError as err:
            print(".: {} {}: {}: {}".format(txt.ERR_CLR, txt.ERR_FILE_WRITE, err.filename, err.strerror))
            exit(1)

    def validate_country_selection(self):
        """Do a check on the users country selection"""
        if self.config["only_country"]:
            if ["Custom"] == self.config["only_country"]:
                self.validate_custom_config()

            elif ["all"] == self.config["only_country"]:
                self.config["only_country"] = []  # reset to default
            else:
                if not ValidFn.is_list_valid(self.config["only_country"], self.mirrors.countrylist):
                    self.config["only_country"] = []  # validation fail
                else:
                    self.only_country = self.config["only_country"]

        if not self.config["only_country"]:
            if self.geolocation:
                country = ValidFn.is_geoip_valid(self.mirrors.countrylist)
                if country:  # geoip ok
                    self.only_country = [country]
                else:  # validation fail
                    self.only_country = self.mirrors.countrylist
            else:
                self.only_country = self.mirrors.countrylist

    def validate_custom_config(self):
        """Check for custom config and validate it"""
        self.custom = ValidFn.is_custom_conf_valid(self.config["only_country"])
        if self.custom:
            # read custom file
            servers = JsonFn.read_json_file(CUSTOM_FILE, dictionary=True)
            # reset mirrorlist to custom mirrorlist
            self.mirrors.seed(servers, custom=True)
            # set our work country list to countries from custom list
            self.only_country = self.mirrors.countrylist

    def validate_mirror(self):
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
                    self.mirror_to_server_list(mirror)
                    if resp_time == "99.99":
                        continue
                    print("\r   {:<5}{}{} ".format(txt.GS, resp_time, txt.CE))

    @staticmethod
    def write_custom_config(filename, selection, custom=False):
        """Writes the configuration to file
        :param filename:
        :param selection:
        :param custom:
        """
        if custom:
            if selection == ["Custom"]:
                new_config = "OnlyCountry = Custom\n"
            else:
                new_config = "OnlyCountry = {list}\n".format(
                    list=",".join(selection))
        else:
            new_config = "# OnlyCountry = \n"
        try:
            with open(
                filename) as cnf, tempfile.NamedTemporaryFile(
                "w+t", dir=os.path.dirname(
                    filename), delete=False) as tmp:
                replaced = False
                for line in cnf:
                    if "OnlyCountry" in line:
                        tmp.write(new_config)
                        replaced = True
                    else:
                        tmp.write("{}".format(line))
                if not replaced:
                    tmp.write(new_config)
            os.replace(tmp.name, filename)
            os.chmod(filename, 0o644)
        except OSError as err:
            print(".: {} {}: {}: {}".format(txt.ERR_CLR, txt.ERR_FILE_READ,
                                            err.filename, err.strerror))
            exit(1)

    def run(self):
        """Run"""
        self.config = self.load_conf()
        self.command_line_parse()
        FileFn.dir_must_exist(MIRROR_DIR)
        self.manjaro_online = HttpFn.manjaro_online_update()
        self.load_mirror_file()
        self.validate_custom_config()
        self.validate_country_selection()
        self.gen_server_lists()
        if self.interactive:
            self.gen_mirror_list_interactive()
        else:
            self.gen_mirror_list_common()
        # TODO: Eventually remove in production
        if DEVELOPMENT:
            print("pacman-mirrors {}".format(__version__) + DESCRIPTION)
if __name__ == "__main__":
    app = PacmanMirrors()
    app.run()
