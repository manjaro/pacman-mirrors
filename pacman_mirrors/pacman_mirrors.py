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
import datetime
import importlib.util
import json
import os
import sys
import time
from http.client import HTTPException
from operator import itemgetter
from random import shuffle
from socket import timeout
from urllib.error import URLError
from urllib.request import urlopen
from http_module import Fetcher
from local_module import FileHandler
from pacman_mirrors import __version__
from .custom_help_formatter import CustomHelpFormatter
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
        self.available_countries = []
        self.good_servers = []  # respond updated < 24h
        self.resp_servers = []  # respond updated > 24h
        self.bad_servers = []   # no response timeout > max_wait_time
        # Decisions
        self.geolocation = False
        self.interactive = False
        self.quiet = False
        self.no_display = False
        # Time out
        self.max_wait_time = 2
        # Files and dirs
        self.config_file = "/etc/pacman-mirrors.conf"
        self.default_mirror_dir = "/etc/pacman.d/mirrors"
        self.default_mirror_list = "/etc/pacman.d/mirrorlist"
        self.custom_mirror_dir = "/var/lib/pacman-mirrors"
        self.custom_mirror_file = "/var/lib/pacman-mirrors/Custom"
        # Define config
        self.config = {}

    def append_to_server_list(self, mirror, last_sync):
        """
        Append mirror to relevant list based on elapsed hours

        :param: mirror: object
        :param: last_sync: mirror last sync
        """
        elapsed_hours = int(last_sync[:-3])
        if elapsed_hours <= int(txt.LASTSYNC_OK[:-3]):
            self.good_servers.append(mirror)
        elif elapsed_hours <= int(txt.LASTSYNC_NA[:-3]):
            self.resp_servers.append(mirror)
        elif elapsed_hours == int(txt.SERVER_BAD[:-3]):
            self.bad_servers.append(mirror)

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
            print("pacman-mirrors {}".format(__version__))
            exit(0)

        if os.getuid() != 0:
            print("{}: {}".format(txt.ERROR, txt.ERR_NOT_ROOT))
            exit(1)

        if args.no_update:
            if self.config["no_update"] == "True":
                exit(0)

        if args.method:
            self.config["method"] = args.method

        if args.branch:
            self.config["branch"] = args.branch

        if args.mirror_dir:
            self.config["mirror_dir"] = args.mirror_dir
            self.default_mirror_dir = self.config["mirror_dir"]

        self.available_countries = sorted(
            os.listdir(self.config["mirror_dir"]))

        if args.geoip:
            self.geolocation = True

        if args.country:
            country = args.country.split(",")
            if country == ["Custom"]:
                self.config["only_country"] = country
            elif country == ["all"]:
                self.config["only_country"] = []
            else:
                try:
                    self.validate_country_list(country,
                                               self.available_countries)
                    self.config["only_country"] = country
                except argparse.ArgumentTypeError as err:
                    parser.error(err)

        if args.output:
            if args.output[0] == "/":
                self.config["mirror_list"] = args.output
            else:
                self.config["mirror_list"] = os.getcwd() + "/" + args.output
            self.default_mirror_list = self.config["mirror_list"]

        if args.interactive:
            self.interactive = True
            if not os.environ.get("DISPLAY") or not GTK_AVAILABLE:
                self.no_display = True

        if args.timeout:
            self.max_wait_time = args.timeout

        if args.quiet:
            self.quiet = True

    def config_init(self):
        """Get config informations"""
        # initialising defaults
        # information which can differ from these defaults
        # is fetched from config file
        config = {
            "branch": "stable",
            "method": "rank",
            "only_country": [],
            "mirror_dir": "/etc/pacman.d/mirrors",
            "mirror_list": "/etc/pacman.d/mirrorlist",
            "no_update": False,
        }
        try:
            # read configuration from file
            with open(self.config_file) as conf:
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
            print("{}: {}: {}: {}".format(txt.ERROR, txt.ERR_FILE_READ,
                                          err.filename, err.strerror))
        return config

    def gen_mirror_list_common(self):
        """Generate common mirrorlist"""
        server_list = self.good_servers # Avoid an empty mirrorlist
        if len(self.resp_servers) >= 3:
            server_list.extend(self.resp_servers)
        else:
            server_list.extend(self.resp_servers)
            server_list.extend(self.bad_servers)

        if server_list:
            if self.config["only_country"] == self.available_countries:
                self.modify_config()
            else:
                self.modify_config(custom=True)
            self.output_mirror_list(server_list, write_file=True)
        else:
            print("\n{}: {}\n".format(txt.ERROR, txt.ERR_SERVER_NOT_AVAILABLE))

    def gen_mirror_list_interactive(self):
        """
        Prompt the user to select the mirrors with a gui.

        * Write the mirrorlist file,
        * Write "Custom" mirror file
        * Modify the configuration file to use the "Custom" file.
        """
        # concat good servers and responding servers
        server_list = self.good_servers + self.resp_servers + self.bad_servers
        server_list = sorted(server_list, key=itemgetter("response_time"))

        if self.no_display:
            from . import console_ui as ui
        else:
            from . import graphical_ui as ui
        interactive = ui.run(server_list)

        if interactive.is_done:
            new_list = interactive.custom_list
            if new_list:
                print("\n:: {}".format(txt.INF_INTERACTIVE_LIST))
                print("--------------------------")
                self.output_mirror_file(new_list)
                self.output_mirror_list(new_list, write_file=True)
                self.modify_config(custom=True)
                print(":: {}: {}".format(txt.INF_INTERACTIVE_LIST_SAVED,
                                         self.custom_mirror_file))
            else:
                print("{}: {}".format(txt.INFO, txt.INF_NO_SELECTION))
                print("{}: {}".format(txt.INFO, txt.INF_NO_CHANGES))
        else:
            return

    def load_server_lists(self):
        """
        Generate a list of servers

        It will only use mirrors defined in only_country, and if empty will
        use all mirrors.
        """
        if self.config["only_country"]:
            if self.config["only_country"] == ["Custom"]:
                if not os.path.isfile(self.custom_mirror_file):
                    print("{}: {} '{} {}'\n".format(txt.WARN,
                                                    txt.INF_CUSTOM_MIRROR_FILE,
                                                    self.custom_mirror_file,
                                                    txt.INF_DOES_NOT_EXIST))
                    self.config["only_country"] = []
            elif self.config["only_country"] == ["all"]:
                self.config["only_country"] = []
        elif not self.config["only_country"]:
            if self.geolocation:
                geoip_country = self.get_geoip_country()
                if geoip_country and geoip_country in self.available_countries:
                    self.config["only_country"] = [geoip_country]
                else:
                    self.config["only_country"] = self.available_countries
            else:
                self.config["only_country"] = self.available_countries

        if self.config["method"] == "rank":
            self.query_servers(self.config["only_country"])
        elif self.config["method"] == "random":
            self.random_servers(self.config["only_country"])

    def modify_config(self, custom=False):
        """Modify configuration"""
        if not custom:
            # remove custom mirror file
            if os.path.isfile(self.custom_mirror_file):
                os.remove(self.custom_mirror_file)
                os.rmdir(self.custom_mirror_dir)
        FileHandler.write_config_to_file(self, 
                                         self.config_file,
                                         self.config["only_country"],
                                         custom)

    def output_mirror_file(self, servers):
        """Write a custom mirror file in custom mirror dir"""
        os.makedirs(self.custom_mirror_dir, mode=0o755, exist_ok=True)
        try:
            with open(self.custom_mirror_file, "w") as output:
                print(":: {}".format(txt.INF_OUTPUT_MIRROR_FILE))
                FileHandler.write_mirror_file_header(self, output)
                for server in servers:
                    FileHandler.write_mirror_list_entry(self,
                                                        output,
                                                        server,
                                                        mirror_file=True)
        except OSError as err:
            print("{}: {}: {}: {}".format(txt.ERROR, txt.ERR_FILE_WRITE,
                                          err.filename, err.strerror))
            exit(1)

    def output_mirror_list(self, servers, write_file=False):
        """
        Write servers to /etc/pacman.d/mirrorlist

        :param: servers: list of servers to write
        :param: write_file: if "True" the list is written to disk
        """
        try:
            with open(self.config["mirror_list"], "w") as outfile:
                if write_file:
                    print(":: {}".format(txt.INF_MIRROR_LIST_WRITE))
                    FileHandler.write_mirror_list_header(self, outfile)
                for server in servers:
                    if write_file:
                        # insert selected branch in url
                        server["url"] = server["url"].replace(
                            "$branch", self.config["branch"])
                        FileHandler.write_mirror_list_entry(self, outfile, server)
                        if not self.quiet:
                            print("==> {} : {}".format(server["country"],
                                                       server["url"]))
                print(":: {}: {}".format(txt.INF_MIRROR_LIST_SAVED,
                                         self.config["mirror_list"]))
        except OSError as err:
            print("{}: {}: {}: {}".format(txt.ERROR, txt.ERR_FILE_WRITE,
                                          err.filename, err.strerror))
            exit(1)

    def query_servers(self, countries):
        """
        Query the servers and put them in good_server, resp_server and
        bad_server depending on quality, and sort them by response time.

        :param countries: list of country files to use
        """
        print(":: {}".format(txt.INF_QUERY_TIME_INFO))
        for country in countries:
            if "Custom" in country:
                custom = True
                mirror_dir = self.custom_mirror_dir
                print("=> {}".format(txt.INF_QUERY_CUSTOM))
            else:
                custom = False
                mirror_dir = self.default_mirror_dir
                print("=> {} {}".format(txt.INF_QUERY_DEFAULT, country))
            # create a ref point for calculation
            point_in_time = datetime.datetime.utcnow()
            try:
                with open(os.path.join(mirror_dir, country), "r") as mirrorfile:
                    for line in mirrorfile:
                        mirror_country = self.get_mirror_country(line)
                        if mirror_country:
                            country = mirror_country
                            continue
                        server_url = self.get_mirror_url(line)
                        if not server_url:
                            continue
                        server = {"country": country,
                                  "response_time": txt.SERVER_RES,
                                  "last_sync": txt.SERVER_BAD,
                                  "url": server_url}
                        # create a probe start reference point
                        probe_start = time.time()
                        statefile = self.query_mirror_state(
                            server["url"], self.config["branch"],
                            self.max_wait_time, self.quiet)
                        # calculate response time
                        server_response_time = self.get_mirror_response_time(
                            probe_start, time.time())
                        if not self.quiet:
                            s_url = server_url.replace("$branch",
                                                       self.config["branch"])
                            if custom:
                                print("==> {} - {} - {}".format(country,
                                                                server_response_time,
                                                                s_url))
                            else:
                                print("==> {} - {}".format(server_response_time,
                                                           s_url))
                        if not statefile:
                            self.append_to_server_list(
                                server, server["last_sync"])
                            continue
                        server["response_time"] = server_response_time
                        # extract timestamp from statefile
                        statefile_timestamp = self.get_mirror_branch_timestamp(
                            statefile)
                        try:
                            branch_timestamp = datetime.datetime.strptime(
                                statefile_timestamp, "%Y-%m-%dT%H:%M:%S")
                        except ValueError:
                            server["last_sync"] = txt.LASTSYNC_NA
                            self.append_to_server_list(
                                server, server["last_sync"])
                            if not self.quiet:
                                print("\n{}: {}".format(txt.WARN,
                                                        txt.INF_QUERY_WRONG_DATE_FORMAT))
                        server["last_sync"] = self.get_mirror_branch_last_sync(
                            point_in_time, branch_timestamp)
                        self.append_to_server_list(server, server["last_sync"])
            except OSError as err:
                print("{}: {}: {}: {}".format(txt.ERROR, txt.ERR_FILE_READ,
                                              err.filename, err.strerror))
        self.good_servers = sorted(self.good_servers,
                                   key=itemgetter("response_time"))
        self.resp_servers = sorted(self.resp_servers,
                                   key=itemgetter("response_time"))

    def random_servers(self, countries):
        """
        Add all servers to bad_servers and shuffle them randomly.

        :param countries: list of country files to use
        """
        print(":: {}".format(txt.INF_RANDOMIZE_SERVERS))
        for country in countries:
            try:
                with open(os.path.join(
                        self.default_mirror_dir, country), "r") as conf:
                    for line in conf:
                        m_country = self.get_mirror_country(line)
                        if m_country:
                            country = m_country
                            continue
                        m_url = self.get_mirror_url(line)
                        if not m_url:
                            continue
                        server = {"country": country,
                                  "response_time": txt.SERVER_RES,
                                  "last_sync": txt.SERVER_BAD,
                                  "url": m_url}
                        self.append_to_server_list(server, txt.SERVER_RES)
            except OSError as err:
                print("{}: {}: {}: {}".format(txt.ERROR, txt.ERR_FILE_READ,
                                              err.filename, err.strerror))
        shuffle(self.bad_servers)

    @staticmethod
    def get_geoip_country():
        """
        Try to get the user country via GeoIP

        :return: return country name or empty list
        """
        country_name = None
        try:
            res = urlopen("http://freegeoip.net/json/", timeout=2)
            json_obj = json.loads(res.read().decode("utf8"))
        except (URLError, timeout, HTTPException, json.JSONDecodeError):
            pass
        else:
            if "country_name" in json_obj:
                country_name = json_obj["country_name"]
                country_fix = {
                    "Brazil": "Brasil",
                    "Costa Rica": "Costa_Rica",
                    "Czech Republic": "Czech",
                    "South Africa": "Africa",
                    "United Kingdom": "United_Kingdom",
                    "United States": "United_States",
                }
                if country_name in country_fix.keys():
                    country_name = country_fix[country_name]
        return country_name

    @staticmethod
    def validate_country_list(countries, available_countries):
        """
        Check if the list of countries are valid.

        :param countries: list of countries to check
        :param available_countries: list of available countries
        :raise argparse.ArgumentTypeError: if it finds and invalid country.
        """
        for country in countries:
            if country not in available_countries:
                msg = ("{}{}: '{}: {}'.\n\n{}: {}".format(
                    txt.INF_OPTION,
                    txt.OPT_COUNTRY,
                    txt.INF_UNKNOWN_COUNTRY,
                    country,
                    txt.INF_AVAILABLE_COUNTRIES,
                    ", ".join(available_countries)))
                raise argparse.ArgumentTypeError(msg)

    def run(self):
        """Run"""
        Fetcher.get_mirrors_list(self)
        Fetcher.get_mirrors_state(self)
        self.config = self.config_init()
        self.command_line_parse()
        self.load_server_lists()
        if self.interactive:
            self.gen_mirror_list_interactive()
        else:
            self.gen_mirror_list_common()


if __name__ == "__main__":
    app = PacmanMirrors()
    app.run()
