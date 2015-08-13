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

from pacman_mirrors_gui import chooseMirrors


def print_write_error(e):
    print("Error: Cannot write file '{filename}': {error}"
          .format(filename=e.filename, error=e.strerror))


def print_read_error(e):
    print("Error: Cannot read file '{filename}': {error}"
          .format(filename=e.filename, error=e.strerror))


class PacmanMirrors:

    def __init__(self):
        self.path_conf = "/etc/pacman-mirrors.conf"
        self.generate = False
        self.interactive = False
        self.method = "rank"
        self.branch = "stable"
        self.only_country = []
        self.mirror_dir = "/etc/pacman.d/mirrors"
        self.output_mirrorlist = "/etc/pacman.d/mirrorlist"
        self.max_wait_time = 2
        self.available_countries = []
        self.arch = os.uname().machine  # i686 or X86_64

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
            print("Warning: Cannot read file '{filename}': {error}"
                  .format(filename=e.filename, error=e.strerror))
        except OSError:
            pass
        self.parse_cmd()

    def parse_configuration_file(self, conf_file):
        """ Parse the file "pacman-mirrors.conf" """
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
                # Branch Pacman should use
                if key == "Branch":
                    self.branch = value
                # Only mirrors from specific countries
                elif key == "OnlyCountry":
                    self.only_country = value.split(',')
                # Input mirrorlist directory
                elif key == "MirrorlistsDir":
                    self.mirror_dir = value
                # Output mirrorlist file
                elif key == "OutputMirrorlist":
                    self.output_mirrorlist = value

    def parse_cmd(self):
        """ Read the arguments of the command line """

        # The interactive argument will be only available if Gtk is installed
        try:
            importlib.util.find_spec('gi.repository.Gtk')
        except ImportError:
            gtk_available = False
        else:
            gtk_available = True

        parser = argparse.ArgumentParser()
        parser.add_argument("-g", "--generate",
                            help="generate new mirrorlist",
                            action="store_true")
        parser.add_argument("-m", "--method",
                            help="use generation method",
                            type=str, choices=["rank", "random"])
        parser.add_argument("-b", "--branch",
                            help="use branch name",
                            type=str, choices=["stable", "testing", "unstable"])
        parser.add_argument("-c", "--country",
                            help="use only mirrors from country[,country,...]",
                            type=str)
        parser.add_argument("-d", "--mirror_dir",
                            help="use path as mirrorlist directory",
                            type=str)
        parser.add_argument("-o", "--output",
                            help="specify output file",
                            type=str)
        parser.add_argument("-t", "--timeout",
                            help="server maximum waiting time (seconds)",
                            type=int)
        if gtk_available:
            parser.add_argument("-i", "--interactive",
                                help="interactively generate a custom mirrorlist",
                                action="store_true")
        parser.add_argument("-v", "--version",
                            help="print the pacman-mirrors version",
                            action="store_true")
        args = parser.parse_args()

        if len(sys.argv) == 1:
            parser.print_help()
            exit(0)

        if args.version:
            print("pacman-mirrors 1.5")
            exit(0)

        if args.generate:
            self.generate = args.generate

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
                                (key, value) = [x.strip() for x in line.split('=', 1)]
                                if key == "OnlyCountry" and value == "Custom":
                                    fo.write("# OnlyCountry = \n")
                except OSError as e:
                    print_write_error(e)
                    exit(1)
                try:
                    os.remove(self.mirror_dir + "/Custom", )
                except FileNotFoundError:
                    pass
                except OSError as e:
                    print("Warning: Cannot remove '{filename}': {error}"
                          .format(filename=e.filename,
                                  error=e.strerror))
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
        available_countries = os.listdir(mirrors_dir)
        available_countries.sort()
        return available_countries

    @staticmethod
    def valid_country(string, available_countries):
        countries = string.split(",")
        if countries == ["all"]:
            return countries
        for i in countries:
            if i not in available_countries:
                msg = "argument -c/--country: "\
                      "unknown country '{}'"\
                      "\nAvailable countries are: {}"\
                    .format(i, ", ".join(available_countries))
                raise argparse.ArgumentTypeError(msg)
        return countries

    def query_servers(self):
        """ Query servers """
        if self.method == "rank":
            print(":: Querying servers, this may take some time...")
        if self.only_country:
            countries = self.only_country
        else:
            countries = self.available_countries
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

                    if self.method == "random":
                        self.bad_servers.append({'country': current_country,
                                                 'response_time': "99.99",
                                                 'last_sync': "99:99",
                                                 'url': server_url,
                                                 'selected': False})
                        print("->", server_url)
                        continue

                    print("-> .....", server_url, end='')
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
                            print('\nError: We failed to reach '
                                  'the server:', e.reason)
                        elif hasattr(e, 'code'):
                            print('\nError: The server couldn\'t '
                                  'fulfill the request.', e.code)
                        self.bad_servers.append({'country': current_country,
                                                 'response_time': "99.99",
                                                 'last_sync': "99:99",
                                                 'url': server_url,
                                                 'selected': False})
                        continue
                    except timeout:
                        print("Error: Timeout")
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
                    print("\r->", response_seconds, sep="")
                    sys.stdout.flush()
                    try:
                        date_server = datetime.datetime.strptime(
                            date, "%Y-%m-%dT%H:%M:%S")
                    except ValueError:
                        self.resp_servers.append({'country': current_country,
                                                  'response_time': response_seconds,
                                                  'last_sync': "99:99",
                                                  'url': server_url,
                                                  'selected': False})
                        print('Error: Wrong date format in "state" file. '
                              'Server skipped.')
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

    def write_mirrorlist(self):
        """ Write the "mirrorlist" file """
        try:
            with open(self.output_mirrorlist, "w") as fo:
                fo.write("##\n")
                fo.write("## Manjaro Linux repository mirrorlist\n")
                fo.write("## Generated on ")
                fo.write(datetime.datetime.now().strftime("%d %B %Y %H:%M"))
                fo.write("\n##\n")
                fo.write("## Use pacman-mirrors to modify\n")
                fo.write("##\n\n")
                if len(self.good_servers) >= 3:  # Avoid an empty mirrorlist
                    server_list = self.good_servers
                elif len(self.resp_servers) >= 3:
                    server_list = self.good_servers + self.resp_servers
                else:
                    server_list = (self.good_servers + self.resp_servers +
                                   self.bad_servers)
                    if not server_list:
                        print("\nError: no server available !\n")
                for server in server_list:
                    fo.write("\n## Location  : ")
                    fo.write(server['country'])
                    if self.method == "rank":
                        fo.write("\n## Time      :")
                        fo.write(server['response_time'])
                        fo.write("\n## Last Sync : ")
                        fo.write(server['last_sync'])
                    fo.write("\nServer = ")
                    fo.write(server['url'])
                    fo.write("\n")
                print(":: Generated and saved '{}' mirrorlist."
                      .format(self.output_mirrorlist))
        except OSError as e:
            print_write_error(e)
            exit(1)

    def write_interactive_mirrorlist(self):
        """ Write the interactive "mirrorlist" file """
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
                    fo.write("[" + server['country'] + "]\n")
                    fo.write("Server = " + server['url'] + "\n")
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
                fo.write("## Generated on ")
                fo.write(datetime.datetime.now().strftime("%d %B %Y %H:%M"))
                fo.write("\n##\n")
                fo.write("## Use pacman-mirrors to modify\n")
                fo.write("##\n\n")
                print("\nCustom List")
                print("-----------\n")
                for server in custom_list:
                    server['url'] = server['url'].replace("$branch", self.branch)
                    print("-> {0} :".format(server['country']), server['url'])
                    fo.write("\n## Location  : ")
                    fo.write(server['country'])
                    if self.method == "rank":
                        fo.write("\n## Time      :")
                        fo.write(server['response_time'])
                        fo.write("\n## Last Sync : ")
                        fo.write(server['last_sync'])
                    fo.write("\nServer = ")
                    fo.write(server['url'])
                    fo.write("\n")
                print("\n:: Generated and saved '{}' custom mirrorlist."
                      .format(self.output_mirrorlist))
        except OSError as e:
            print_write_error(e)
            exit(1)

    def run(self):
        self.query_servers()
        if self.interactive:
            self.write_interactive_mirrorlist()
        else:
            self.write_mirrorlist()

if __name__ == '__main__':
    if os.getuid() != 0:
        print("Error: must be root.")
        exit(1)

    pm = PacmanMirrors()
    pm.run()
