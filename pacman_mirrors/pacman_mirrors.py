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
# Authors   : Esclapion
#             philm
#             Ramon Buldó <rbuldo@gmail.com>
#             Hugo Posnic <huluti@manjaro.org>
#             Frede Hundewadt <frede@hundewadt.dk>

"""
Pacman-Mirrors
Main Module
"""

import argparse
import importlib.util
import os
import sys
import datetime
import os
import tempfile
from operator import itemgetter
from pacman_mirrors import __version__
from random import shuffle
from .configuration import \
    ENV, CONFIG_FILE, CUSTOM_FILE, FALLBACK, \
    MIRROR_DIR, MIRROR_FILE, MIRROR_LIST, STATUS_FILE, \
    REPO_ARCH, BRANCHES
from .customfn import CustomFn
from .custom_help_formatter import CustomHelpFormatter
from .filefn import FileFn
from .httpfn import HttpFn
from .jsonfn import JsonFn
from .mirror import Mirror
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
        self.selection = []  # users selected countries
        # Decisions
        self.custom = False
        self.geolocation = False
        self.interactive = False
        self.manjaro_online = True
        self.no_display = False
        self.quiet = False
        # Time out
        self.max_wait_time = 2
        # Define config
        self.config = {}

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
        parser.add_argument("--no_update",
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
            print("pacman-mirrors {}".format(__version__))
            exit(0)

        if not ENV:
            print("TODO: Remove ENV check in command_line_parse()")
            if os.getuid() != 0:
                print(".:> {}: {}".format(txt.ERROR, txt.ERR_NOT_ROOT))
                exit(1)

        if args.no_update:
            if self.config["no_update"] == "True":
                exit(0)

        if args.method:
            self.config["method"] = args.method

        if args.branch:
            self.config["branch"] = args.branch

        if args.geoip:
            self.geolocation = True

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
            self.config["mirror_list"] = self.config["mirror_list"]

        if args.interactive:
            self.interactive = True
            if not os.environ.get("DISPLAY") or not GTK_AVAILABLE:
                self.no_display = True

        if args.country:
            self.config["only_country"] = args.country.split(",")

    def gen_mirror_list_common(self):
        """Generate common mirrorlist"""
        server_list = self.good_servers + self.resp_servers
        if self.config["method"] == "random":
            server_list = self.random_servers
        if server_list:
            if self.custom:
                self.modify_config(custom=True)
            else:
                self.modify_config()
            self.output_mirror_list(server_list, write_file=True)
        else:
            print("\n.: {}: {}\n".format(txt.ERROR, txt.ERR_NO_MIRRORS))

    def gen_mirror_list_interactive(self):
        """Prompt the user to select the mirrors with a gui.
        * Outputs a pacman mirrorlist,
        * Outputs a "custom" mirror file
        * Modify the configuration file to use the "custom" file.
        """
        mirrorlist = []
        interactive_list = []
        for country in self.selection:
            for mirror in self.mirrors.mirrorlist:
                if country == mirror["country"]:
                    mirrorlist.append(mirror)
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
        interactive = ui.run(interactive_list)

        if interactive.is_done:
            selection = []
            mirrorfile = []
            for selected in interactive.custom_list:
                for server in self.mirrors.mirrorlist:
                    if selected["url"] == server["url"]:
                        selection.append(server)
                        mirrorfile.append({
                            "country": server["country"],
                            "protocols": server["protocols"],
                            "url": server["url"]
                        })
            if mirrorfile:
                print("\n.:> {}: {}".format(txt.INFO, txt.INF_INTERACTIVE_LIST))
                print("--------------------------")
                # write custom mirror file
                JsonFn.write_json_file(mirrorfile, CUSTOM_FILE)
                # output pacman mirrorlist
                self.output_mirror_list(mirrorfile, write_file=True)
                self.modify_config()
                print(".:> {}: {}: `{}`".format(txt.INFO, txt.INF_INTERACTIVE_LIST_SAVED, CUSTOM_FILE))
            else:
                print(".:> {}: {}".format(txt.INFO, txt.INF_NO_SELECTION))
                print(".:> {}: {}".format(txt.INFO, txt.INF_NO_CHANGES))
        else:
            return

    def gen_server_list(self):
        """Generate server lists"""
        if not self.manjaro_online:
            self.config["method"] = "random"
            print(".:> {}: {}".format(txt.INFO, txt.INF_NETWORK_DOWN))
            print(".:> {}: {} {}".format(txt.INFO, txt.INF_FALLING_BACK, txt.OPT_RANDOM))
        if self.config["method"] == "rank":
            self.validate_mirror()
        elif self.config["method"] == "random":
            self.randomize_servers()

    def load_mirror_file(self):
        """Load mirror file"""
        load_status = False
        if self.custom:
            servers = JsonFn.read_json_file(CUSTOM_FILE, dictionary=True)
        else:
            if FileFn.check_file(STATUS_FILE):
                load_status = True
                servers = JsonFn.read_json_file(STATUS_FILE, dictionary=True)
            elif FileFn.check_file(MIRROR_FILE):
                servers = JsonFn.read_json_file(MIRROR_FILE, dictionary=True)
            else:
                servers = JsonFn.read_json_file(FALLBACK, dictionary=True)
                JsonFn.write_json_file(servers, MIRROR_FILE)
        if load_status:
            self.mirrors.seed(servers, status=True)
        else:
            self.mirrors.seed(servers)

    def mirror_to_server_list(self, mirror):
        """Append mirror to relevant list based on elapsed hours
        :param: mirror: object
        :param: last_sync: mirror last sync
        """
        if mirror["last_sync"] == -1:
            elapsed_hours = -1
        else:
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
        self.write_mirror_config(CONFIG_FILE, self.selection, custom)

    def output_mirror_list(self, servers, write_file=False):
        """Write servers to /etc/pacman.d/mirrorlist
        :param: servers: list of servers to write
        :param: write_file: if "True" the list is written to disk
        """
        try:
            with open(self.config["mirror_list"], "w") as outfile:
                if write_file:
                    print(".:> {}: {}".format(txt.INFO, txt.INF_MIRROR_LIST_WRITE))
                    self.write_mirror_list_header(outfile)
                for server in servers:
                    if write_file:
                        url = server["url"]
                        for protocol in enumerate(server["protocols"]):
                            pos = url.find(":")
                            server["url"] = "{}{}{}{}".format(protocol[1],
                                                              url[pos:],
                                                              self.config["branch"],
                                                              REPO_ARCH)
                            self.write_mirror_list_server(outfile, server)
                            if not self.quiet:
                                print(".:> {} : `{}`".format(server["country"], server["url"]))
                print(".:> {}: {}: `{}`".format(txt.INFO, txt.INF_MIRROR_LIST_SAVED, self.config["mirror_list"]))
        except OSError as err:
            print(".:> {}: {}: {}: {}".format(txt.ERROR, txt.ERR_FILE_WRITE, err.filename, err.strerror))
            exit(1)

    def randomize_servers(self):
        """Randomize selected servers"""
        print(".:> {}: {}".format(txt.INFO, txt.INF_RANDOMIZE_SERVERS))
        mirrors = []
        for country in self.selection:
            for mirror in self.mirrors.mirrorlist:
                if country == mirror["country"]:
                    mirrors.append(mirror)
        self.random_servers = mirrors

    def validate_mirror(self):
        """Query server for response time"""
        if self.custom:
            print(".:> {}: {}".format(txt.INFO, txt.INF_QUERY_CUSTOM_SERVERS))
            print(".:> {}: {}".format(txt.INFO, txt.INF_QUERY_CUSTOM))
        else:
            print(".:> {}: {}".format(txt.INFO, txt.INF_QUERY_ALL_SERVERS))
            print(".:> {}: {}".format(txt.INFO, txt.INF_QUERY_DEFAULT))

        mirrors = []
        for country in self.selection:
            for mirror in self.mirrors.mirrorlist:
                if country == mirror["country"]:
                    mirrors.append(mirror)

        for mirror in mirrors:
            print("-> ..... {}: `{}`".format(mirror["country"], mirror["url"]),
                  end='')
            sys.stdout.flush()
            resp_time = HttpFn.get_mirror_response(mirror["url"], timeout=2, count=1)
            print("\r-> {} ".format(resp_time))
            mirror["resp_time"] = resp_time
            self.mirror_to_server_list(mirror)

    def validate_country_selection(self):
        """Do a check on the users country selection"""
        self.selection = self.check_list(self.config["only_country"],
                                         self.mirrors.countrylist)
        self.selection = self.check_selection(self.selection,
                                              self.mirrors.countrylist,
                                              self.geolocation)
        if self.selection == self.mirrors.countrylist:
            self.config["only_country"] = []

    @staticmethod
    def check_list(selection, countrylist):
        """Check if the list of countries are valid.
        :param selection: list of countries to check
        :param countrylist: list of available countries
        """
        if not selection == ["all"]:
            for country in selection:
                if country not in countrylist:
                    print(".:> {}{}: '{}: {}'.\n\n{}".format(
                        txt.INF_OPTION,
                        txt.OPT_COUNTRY,
                        txt.INF_UNKNOWN_COUNTRY,
                        country,
                        txt.INF_USING_ALL_SERVERS))
                    selection = []
        return selection

    @staticmethod
    def check_selection(selection, country_list, geoip):
        """Check validity of country selection"""
        if selection:
            if selection == ["Custom"]:
                if not os.path.isfile(CUSTOM_FILE):
                    print(".:> {}: {} '{} {}'\n".format(
                        txt.WARN, txt.INF_CUSTOM_MIRROR_FILE, CUSTOM_FILE, txt.INF_DOES_NOT_EXIST))
                    print(".:> {}")
                    selection = []
            if geoip or selection == ["all"]:
                selection = []

        if not selection:
            if geoip:
                geoip_country = HttpFn.get_geoip_country()
                if geoip_country and geoip_country in country_list:
                    selection = [geoip_country]
            else:
                selection = country_list
        return selection

    @staticmethod
    def config_init():
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
            print(".:> {}: {}: {}: {}".format(txt.ERROR,
                                            txt.ERR_FILE_READ,
                                            err.filename,
                                            err.strerror))
        return config

    @staticmethod
    def write_mirror_config(config_file, selection, custom=False):
        """Writes the configuration to file
        :param config_file:
        :param selection:
        :param custom:
        """
        if custom:
            if selection == ["Custom"]:
                selection = "OnlyCountry = Custom\n"
            else:
                selection = "OnlyCountry = {list}\n".format(
                    list=",".join(selection))
        else:
            selection = "# OnlyCountry = \n"
        try:
            with open(
                config_file) as cnf, tempfile.NamedTemporaryFile(
                "w+t", dir=os.path.dirname(
                    config_file), delete=False) as tmp:
                replaced = False
                for line in cnf:
                    if "OnlyCountry" in line:
                        tmp.write(selection)
                        replaced = True
                    else:
                        tmp.write("{}".format(line))
                if not replaced:
                    tmp.write(selection)
            os.replace(tmp.name, config_file)
            os.chmod(config_file, 0o644)
        except OSError as err:
            print(".:> {}: {}: {}: {}".format(txt.ERROR, txt.ERR_FILE_READ,
                                          err.filename, err.strerror))
            exit(1)

    @staticmethod
    def write_mirror_list_header(handle, custom=False):
        """Write mirrorlist header
        :param handle: handle to a file opened for writing
        :param custom: controls content of the header
        """
        handle.write("##\n")
        if custom:
            handle.write("## Manjaro Linux Custom mirrorlist\n")
            handle.write("## Generated on {}\n".format(
                datetime.datetime.now().strftime("%d %B %Y %H:%M")))
            handle.write("##\n")
            handle.write("## Use 'pacman-mirrors -c all' to reset\n")
        else:
            handle.write("## Manjaro Linux mirrorlist\n")
            handle.write("## Generated on {}\n".format(
                datetime.datetime.now().strftime("%d %B %Y %H:%M")))
            handle.write("##\n")
            handle.write("## Use pacman-mirrors to modify\n")
        handle.write("##\n\n")

    @staticmethod
    def write_mirror_list_server(handle, mirror):
        """Write mirror to mirror list or file
        :param handle: handle to a file opened for writing
        :param mirror: mirror object
        """
        workitem = mirror
        handle.write("## Country       : {}\n".format(workitem["country"]))
        # if workitem["resp_time"] == txt.SERVER_RES:
        #     workitem["resp_time"] = "N/A"
        # handle.write("## Response time : {}\n".format(
        #     workitem["resp_time"]))
        # if workitem["last_sync"] == txt.SERVER_BAD or \
        #         workitem["last_sync"] == txt.LASTSYNC_NA:
        #     workitem["last_sync"] = "N/A"
        # handle.write("## Last Upd hh:mm: {}\n".format(
        #     workitem["last_sync"]))
        handle.write("Server = {}\n\n".format(workitem["url"]))

    def run(self):
        """Run"""
        FileFn.check_directory(MIRROR_DIR)
        CustomFn.convert_to_json()
        self.config = self.config_init()
        self.command_line_parse()
        self.manjaro_online = HttpFn.manjaro_online_update()
        self.load_mirror_file()
        self.validate_country_selection()

        self.gen_server_list()
        if self.interactive:
            self.gen_mirror_list_interactive()
        else:
            self.gen_mirror_list_common()


if __name__ == "__main__":
    app = PacmanMirrors()
    app.run()
