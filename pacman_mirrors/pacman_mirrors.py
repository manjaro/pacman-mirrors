#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
# Author(s): Esclapion
#            philm
#            Ramon Buldó <rbuldo@gmail.com

import argparse
from builtins import staticmethod
import datetime
import sys
import time
from urllib.request import Request, urlopen
from urllib.error import URLError
from socket import timeout
from operator import itemgetter
from decimal import Decimal
import os
import importlib.util
from random import shuffle

from pacman_mirrors_gui import chooseMirrors
from custom_help_formatter import CustomHelpFormatter

import i18n
_ = i18n.language.gettext


def print_write_error(e):
    print(_("Error: Cannot write file '{filename}': {error}"
          .format(filename=e.filename, error=e.strerror)))


def print_read_error(e):
    print(_("Error: Cannot read file '{filename}': {error}"
          .format(filename=e.filename, error=e.strerror)))


class PacmanMirrors:

    def __init__(self):
        self.path_conf = "/etc/pacman-mirrors.conf"
        self.interactive = False
        self.method = "rank"
        self.branch = "stable"
        self.only_country = []
        self.mirror_dir = "/etc/pacman.d/mirrors"
        self.output_mirrorlist = "/etc/pacman.d/mirrorlist"
        self.max_wait_time = 2
        self.available_countries = []
        self.arch = os.uname().machine  # i686 or X86_64
        self.no_update = True

        # good_server: respond back and updated in the last 24h
        # resp_server: respond back but not updated in the last 24h or
        #              can't get last update time
        # bad_server: can't connect or it takes more than max_wait_time
        self.good_servers = []
        self.resp_servers = []
        self.bad_servers = []
        try:
            self.parse_configuration_file(self.path_conf)
        except PermissionError as e:
            print(_("Warning: Cannot read file '{filename}': {error}"
                  .format(filename=e.filename, error=e.strerror)))
        except OSError:
            pass
        self.parse_cmd()

    def parse_configuration_file(self, conf_file):
        """ Parse the configuration file """
        with open(conf_file) as fi:
            for line in fi:
                line = line.strip()
                if line == "":
                    continue
                if line[0] == '#' or line[0] == '\n':
                    continue
                if '=' not in line:
                    continue
                (key, value) = [x.strip() for x in line.split('=', 1)]
                if not key or not value:
                    continue
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                if key == "Branch":
                    self.branch = value
                elif key == "OnlyCountry":
                    self.only_country = value.split(',')
                elif key == "MirrorlistsDir":
                    self.mirror_dir = value
                elif key == "OutputMirrorlist":
                    self.output_mirrorlist = value
                elif key == "NoUpdate":
                    self.no_update = value

    def parse_cmd(self):
        """ Read the arguments of the command line """

        # The interactive argument will be only available if Gtk is installed
        try:
            importlib.util.find_spec('gi.repository.Gtk')
        except ImportError:
            gtk_available = False
        else:
            gtk_available = True

        parser = argparse.ArgumentParser(formatter_class=CustomHelpFormatter)
        parser.add_argument("-g", "--generate",
                            action="store_true",
                            help=_("generate new mirrorlist"))
        parser.add_argument("-m", "--method",
                            type=str,
                            choices=["rank", "random"],
                            help=_("generation method"))
        parser.add_argument("-b", "--branch",
                            type=str,
                            choices=["stable", "testing", "unstable"],
                            help=_("branch name"))
        parser.add_argument("-c", "--country",
                            type=str,
                            help=_("comma separated list of countries "
                                   "where mirrors will be used"))
        parser.add_argument("-d", "--mirror_dir",
                            type=str,
                            metavar=_("PATH"),
                            help=_("mirrors list path"))
        parser.add_argument("-o", "--output",
                            type=str,
                            metavar=_('FILE'),
                            help=_("output file"))
        parser.add_argument("-t", "--timeout",
                            type=int,
                            metavar=_("SECONDS"),
                            help=_("server maximum waiting time"))
        parser.add_argument("--no-update",
                            action="store_true",
                            help=_("don't generate mirrorlist if NoUpdate is"
                                   "set to True in the configuration file"))
        if gtk_available:
            parser.add_argument("-i", "--interactive",
                                action="store_true",
                                help=_("interactively generate a custom "
                                       "mirrorlist"))
        parser.add_argument("-v", "--version",
                            action="store_true",
                            help=_("print the pacman-mirrors version"))
        args = parser.parse_args()

        if len(sys.argv) == 1:
            parser.print_help()
            exit(0)

        if args.version:
            print("pacman-mirrors 20150808")
            exit(0)

        if args.no_update:
            if self.no_update == "True":
                exit(0)

        if args.method:
            self.method = args.method

        if args.branch:
            self.branch = args.branch

        if args.mirror_dir:
            self.mirror_dir = args.mirror_dir
        self.available_countries = self.get_available_countries(self.mirror_dir)

        if args.country:
            try:
                self.only_country = self.valid_country(args.country,
                                                       self.available_countries)
            except argparse.ArgumentTypeError as e:
                parser.error(e)
            if self.only_country == ["all"]:
                # When using all, comment "OnlyCountry=Custom" in
                # the configuration file
                try:
                    with open(self.path_conf, "r") as fi:
                        buf = fi.read().split('\n')
                except OSError as e:
                    print_read_error(e)
                    exit(1)
                try:
                    with open(self.path_conf, "w") as fo:
                        for line in buf:
                            if '=' not in line:
                                fo.write(line + "\n")
                            else:
                                (key, value) = [x.strip()
                                                for x in line.split('=', 1)]
                                if key == "OnlyCountry" and value == "Custom":
                                    fo.write("# OnlyCountry = \n")
                                else:
                                    fo.write(line + "\n")
                except OSError as e:
                    print_write_error(e)
                    exit(1)
                try:
                    os.remove(self.mirror_dir + "/Custom", )
                except FileNotFoundError:
                    pass
                except OSError as e:
                    print(_("Warning: Cannot remove '{filename}': {error}"
                          .format(filename=e.filename,
                                  error=e.strerror)))
                else:
                    self.available_countries.remove('Custom')
                self.only_country = []

        if args.output:
            if args.output[0] == '/':
                self.output_mirrorlist = args.output
            else:
                self.output_mirrorlist = os.getcwd() + "/" + args.output

        if gtk_available and args.interactive:
            self.interactive = args.interactive

        if args.timeout:
            self.max_wait_time = args.timeout

    @staticmethod
    def get_available_countries(mirrors_dir):
        """
        Returns a sorted list of countries.
        The name of mirror file is the country.

        :param mirrors_dir: path with the mirror list
        :return: list of countries
        """
        available_countries = os.listdir(mirrors_dir)
        available_countries.sort()
        return available_countries

    @staticmethod
    def valid_country(string, available_countries):
        """
        Check if the list of countries are valid.

        Raises argparse.ArgumentTypeError if it finds and invalid country.

        :param string: string with comma separated countries
        :param available_countries: list of countries
        :return: return the list of valid countries
        """
        countries = string.split(",")
        if countries == ["all"]:
            return countries
        for country in countries:
            if country not in available_countries:
                msg = _("argument -c/--country: unknown country '{country}'"
                        "\nAvailable countries are: {country_list}"
                        .format(country=country,
                                country_list=", ".join(available_countries)))
                raise argparse.ArgumentTypeError(msg)
        return countries

    def generate_servers_lists(self):
        """
        Generate a list of servers

        It will only use mirrors defined in only_country, and if empty will
        use all mirrors.
        """
        if self.only_country:
            countries = self.only_country
        else:
            countries = self.available_countries

        if self.method == "rank":
            self.query_servers(countries)
        elif self.method == "random":
            self.random_servers(countries)

    def query_servers(self, countries):
        """
        Query the servers and put them in good_server, resp_server and
        bad_server depending on quality, and sort them by response time.

        :param countries: list of country files to use
        """
        print(_(":: Querying servers, this may take some time..."))
        date_now = datetime.datetime.utcnow()
        for country in countries:
            print(country)
            current_country = country
            with open(os.path.join(self.mirror_dir, country), "r") as fi:
                for line in fi:
                    line = line.strip()
                    if line.startswith('[') and line.endswith(']'):
                        current_country = line[1:-1]
                        continue
                    if not line.startswith('Server'):
                        continue
                    server_url = line[9:]
                    server_url = server_url.replace("$branch", self.branch)

                    print("-> ..... {}".format(server_url), end='')
                    sys.stdout.flush()
                    j = server_url.find(self.branch)
                    url = server_url[0:j] + "state"

                    start = time.time()
                    req = Request(url)
                    try:
                        with urlopen(req, timeout=self.max_wait_time) as r:
                            resp = r.read()
                            d = resp.find(b"date=")
                    except URLError as e:
                        if hasattr(e, 'reason'):
                            print(_("\nError: Failed to reach "
                                    "the server: {reason}"
                                    .format(reason=e.reason)))
                        elif hasattr(e, 'code'):
                            print(_("\nError: The server couldn\'t "
                                    "fulfill the request: {code}"
                                    .format(code=e.code)))
                        self.bad_servers.append({'country': current_country,
                                                 'response_time': "99.99",
                                                 'last_sync': "99:99",
                                                 'url': server_url,
                                                 'selected': False})
                        continue
                    except timeout:
                        print(_("\nError: Timeout"))
                        self.bad_servers.append({'country': current_country,
                                                 'response_time': "99.99",
                                                 'last_sync': "99:99",
                                                 'url': server_url,
                                                 'selected': False})
                        continue

                    response_time = round((time.time() - start), 3)
                    date = resp[d+5:d+24].decode('utf-8')
                    response_seconds = "{:6.4}".format(
                        Decimal(response_time).quantize(Decimal('.001')))
                    print("\r->{} ".format(response_seconds))
                    try:
                        date_server = datetime.datetime.strptime(
                            date, "%Y-%m-%dT%H:%M:%S")
                    except ValueError:
                        self.resp_servers.append({'country': current_country,
                                                  'response_time': response_seconds,
                                                  'last_sync': "99:99",
                                                  'url': server_url,
                                                  'selected': False})
                        print(_("\nWarning: Wrong date format in 'state' file."))
                        continue
                    total_seconds = (date_now - date_server).total_seconds()
                    total_minutes = total_seconds // 60
                    hours = total_minutes // 60
                    minutes = total_minutes % 60
                    datesync = '{}:{}'.format(int(hours),
                                              str(int(minutes)).zfill(2))
                    if hours < 24:
                        self.good_servers.append({'country': current_country,
                                                  'response_time': response_seconds,
                                                  'last_sync': datesync,
                                                  'url': server_url,
                                                  'selected': False})
                    else:
                        self.resp_servers.append({'country': current_country,
                                                  'response_time': response_seconds,
                                                  'last_sync': datesync,
                                                  'url': server_url,
                                                  'selected': False})
        # Sort by response time
        self.good_servers = sorted(self.good_servers,
                                   key=itemgetter('response_time'))
        self.resp_servers = sorted(self.resp_servers,
                                   key=itemgetter('response_time'))

    def random_servers(self, countries):
        """
        Add all servers to bad_server and shuffle them randomly.

        :param countries: list of country files to use
        """
        print(_(":: Randomizing server list..."))
        for country in countries:
            current_country = country
            with open(os.path.join(self.mirror_dir, country), "r") as fi:
                for line in fi:
                    line = line.strip()
                    if line.startswith('[') and line.endswith(']'):
                        current_country = line[1:-1]
                        continue
                    if not line.startswith('Server'):
                        continue
                    server_url = line[9:]
                    server_url = server_url.replace("$branch", self.branch)

                    self.bad_servers.append({'country': current_country,
                                             'response_time': "99.99",
                                             'last_sync': "99:99",
                                             'url': server_url,
                                             'selected': False})
        shuffle(self.bad_servers)

    def write_mirrorlist(self):
        """ Write the output file """
        try:
            with open(self.output_mirrorlist, "w") as fo:
                if len(self.good_servers) >= 3:  # Avoid an empty mirrorlist
                    server_list = self.good_servers
                elif len(self.resp_servers) >= 3:
                    server_list = self.good_servers + self.resp_servers
                else:
                    server_list = (self.good_servers + self.resp_servers +
                                   self.bad_servers)
                    if not server_list:
                        print(_("\nError: no server available !\n"))

                fo.write("##\n")
                fo.write("## Manjaro Linux repository mirrorlist\n")
                fo.write("## Generated on {}\n"
                         .format(datetime.datetime.now()
                                 .strftime("%d %B %Y %H:%M")))
                fo.write("##\n")
                fo.write("## Use pacman-mirrors to modify\n")
                fo.write("##\n\n")
                for server in server_list:
                    fo.write("## Location  : {}\n"
                             .format(server['country']))
                    if self.method == "rank":
                        fo.write("## Time      : {}\n"
                                 .format(server['response_time']))
                        fo.write("## Last Sync : \n"
                                 .format(server['last_sync']))
                    fo.write("Server = {}\n\n"
                             .format(server['url']))
                print(_(":: Generated and saved '{output_file}' mirrorlist."
                      .format(output_file=self.output_mirrorlist)))
        except OSError as e:
            print_write_error(e)
            exit(1)

    def write_interactive_mirrorlist(self):
        """ Write the interactive output file and the "Custom" country"""
        # Open custom mirrorlist selector
        finished = False
        server_list = self.good_servers + self.resp_servers + self.bad_servers
        for server in server_list:
            server['url'] = server['url'].replace("/" + self.branch + "/",
                                                  "/$branch/")
        while not finished:
            chooseMirrors(True, server_list)
            custom_list = []
            for server in server_list:
                if server['selected']:
                    custom_list.append(server)
            if len(custom_list) == 0:
                continue
            finished = chooseMirrors(False, custom_list)

        # Write Custom country
        custom_path = self.mirror_dir + "/Custom"
        try:
            with open(custom_path, "w") as fo:
                fo.write("##\n")
                fo.write("## Pacman Mirrorlist\n")
                fo.write("##\n\n")
                for server in custom_list:
                    fo.write("[{}]\n"
                             .format(server['country']))
                    fo.write("Server = {}\n"
                             .format(server['url']))
        except OSError as e:
            print_write_error(e)
            exit(1)

        # Modify configuration to use Custom Country
        try:
            with open(self.path_conf, "r") as fi:
                buf = fi.read().split('\n')
        except OSError as e:
            print_read_error(e)
            exit(1)
        try:
            with open(self.path_conf, "w") as fo:
                replaced = False
                for line in buf:
                    if "OnlyCountry" in line:
                        fo.write("OnlyCountry = Custom\n")
                        replaced = True
                    else:
                        fo.write(line + "\n")
                if not replaced:
                    fo.write("OnlyCountry = Custom\n")

        except OSError as e:
            print_write_error(e)
            exit(1)

        # Write custom mirrorlist
        try:
            with open(self.output_mirrorlist, "w") as fo:
                fo.write("##\n")
                fo.write("## Manjaro Linux repository mirrorlist\n")
                fo.write("## Generated on {}\n"
                         .format(datetime.datetime.now()
                                 .strftime("%d %B %Y %H:%M")))
                fo.write("##\n")
                fo.write("## Use pacman-mirrors to modify\n")
                fo.write("##\n\n")
                print(_("\nUser generated mirror list"))
                print("--------------------------")
                for server in custom_list:
                    server['url'] = server['url'].replace("$branch",
                                                          self.branch)
                    print("-> {} : {}"
                          .format(server['country'], server['url']))
                    fo.write("## Location  : {}\n"
                             .format(server['country']))
                    if self.method == "rank":
                        fo.write("## Time      : {}\n"
                                 .format(server['response_time']))
                        fo.write("## Last Sync : {}\n"
                                 .format(server['last_sync']))
                    fo.write("Server = {}\n\n"
                             .format(server['url']))
                print(_(":: Generated and saved '{output_file}' mirrorlist."
                      .format(output_file=self.output_mirrorlist)))
        except OSError as e:
            print_write_error(e)
            exit(1)

    def run(self):
        self.generate_servers_lists()
        if self.interactive:
            self.write_interactive_mirrorlist()
        else:
            self.write_mirrorlist()

if __name__ == '__main__':
    if os.getuid() != 0:
        print(_("Error: must have root privilegies."))
        exit(1)

    pm = PacmanMirrors()
    pm.run()
