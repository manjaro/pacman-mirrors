#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Build a list of mirrors for pacman'''

# Release : 1.5.1
# Date    : 28 March 2014
# Authors : Esclapion, philm

import argparse, datetime, getopt, signal, sys, time, urllib.request
from sys import *
from operator import itemgetter
from decimal import *
import os

from pacman_mirrors_gui import chooseMirrors


class PacmanMirrors:
    # Global initializations
    # ======================
    path_conf = "/etc/pacman-mirrors.conf"
    datenow = datetime.datetime.utcnow()
    serverList = []
    nbServer = 0      # Global count of servers available
    nbServerResp = 0  # Number of servers responding
    nbServerGood = 0  # Number of servers sinced < 4h

    generate = False     # Generate new mirrorlist
    interactive = False  # Use the gui for custom mirrorlist
    method = "rank"      # Use generation method
    branch = "stable"    # Use branch name
    onlyCountry = []     # Use only mirrors from country[,country,...]
    mirrorlistsDir = "/etc/pacman.d/mirrors"  # Use path as mirrorlist directory
    outputMirrorList = "/etc/pacman.d/mirrorlist"  # Specify output file
    maxWaitTime = 2      # Server maximum waiting time (seconds)

    listeDir = []

    arch = os.uname().machine  # i686 or X86_64

    def alarm_handler(self, signum, frame):
        raise TimeoutError("Ici")

    def time_out(self, timeout):
        signal.signal(signal.SIGALRM, self.alarm_handler)
        signal.alarm(timeout)  # produce SIGALRM in `timeout` seconds

    # Parse the file "pacman-mirrors.conf"
    # ====================================
    def parse_configuration_file(self):
        with open(self.path_conf) as fi:
            for line in fi:
                line = line.strip()
                if line == "":
                    continue
                if line[0] == '#' or line[0] == '\n' :
                    continue
                if '=' not in line:
                    continue
                (key, value) = line.split('=', 1)
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                if key == "Branch":              # Branch Pacman should use
                    self.branch = value
                elif key == "OnlyCountry":       # Specify to use only mirrors from specific countries
                    self.onlyCountry = value.split(',')
                elif key == "MirrorlistsDir":    # Input mirrorlist directory
                    self.mirrorlistsDir = value
                elif key == "OutputMirrorlist":  # Output mirrorlist
                    self.outputMirrorList = value

    # Read the arguments of the command line
    # ======================================
    def parse_command_line_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-g", "--generate", help="generate new mirrorlist",
                            action="store_true")
        parser.add_argument("-m", "--method", help="use generation method",
                            type=str, choices=["rank", "random"])
        parser.add_argument("-b", "--branch", help="use branch name",
                            type=str, choices=["stable", "testing", "unstable"])
        parser.add_argument("-c", "--country", help="use only mirrors from country[,country,...]",
                            type=str)
        parser.add_argument("-d", "--mirror_dir", help="use path as mirrorlist directory",
                            type=str)
        parser.add_argument("-o", "--output", help="specify output file",
                            type=str)
        parser.add_argument("-t", "--timeout", help="server maximum waiting time (seconds)",
                            type=int)
        if os.path.exists('/usr/lib/python3.4/site-packages/gi/overrides/Gtk.py') :
            parser.add_argument("-i", "--interactive", help="interactively generate a custom mirrorlist",
                                action="store_true")
        parser.add_argument("-v", "--version", help="print the pacman-mirrors version",
                            action="store_true")
        args = parser.parse_args()
        if len(sys.argv) == 1:
            parser.print_help()
            exit(0)
        if args.generate:
            self.generate = args.generate
        if args.method:
            self.method = args.method
        if args.branch:
            self.branch = args.branch
        if args.country:
            self.onlyCountry = args.country.split(",")
            if self.onlyCountry == ["all"]:
                try:
                    fconf = open(self.path_conf, "r")
                except:
                    print("\n^GError : can't open file {0}.\n".format(path))
                    exit(1)
                buf = fconf.read().split('\n')
                fconf.close()
                while buf[-1:] == [''] :
                    del buf[-1:]
                try:
                    fconf = open(path, "w")
                except:
                    print("\n^GError : can't open file {0}.\n".format(path))
                    exit(1)
                for line in buf:
                    if "OnlyCountry" in line :
                        fconf.write("#OnlyCountry=Custom\n")
                    else:
                        fconf.write(line + "\n")
                fconf.close
                try:
                    os.remove(self.mirrorlistsDir + "/Custom", )
                except OSError:
                    pass
                self.onlyCountry = []

        if args.mirror_dir:
            self.mirrorlistsDir = args.mirror_dir
        if args.output:
            if args.output[0] == '/':
                self.outputMirrorList = args.output
            else:
                self.outputMirrorList = os.getcwd() + "/" + args.output
        if os.path.exists('/usr/lib/python3.4/site-packages/gi/overrides/Gtk.py'):
            if args.interactive:
                self.interactive = args.interactive
        else:
            self.interactive = False
        if args.timeout:
            self.maxWaitTime = args.timeout
        if args.version:
            print("pacman-mirrors 1.5")
            exit(0)

        self.listeDir = os.listdir(self.mirrorlistsDir)
        self.listeDir.sort()
        for i in self.onlyCountry:
            if i not in self.listeDir:
                print("\nError : unknown country", i)
                print("\nAvailable countries are :", self.listeDir, "\n")
                exit(1)

    def query_servers(self):
        # Main loop
        # =========
        if self.method == "rank":
            print(":: Querying servers, this may take some time...")
        for country in self.listeDir:
            if len(self.onlyCountry) != 0 and country not in self.onlyCountry:
                continue
            print(country)
            current_country = country
            fi = open(os.path.join(self.mirrorlistsDir, country), "r")
            while 1:
                s = fi.readline()
                if s == '':
                    break
                if s[0] == '[':
                    current_country = s[1:-2]
                    continue
                if s[0] != 'S' :
                    continue
                server_url = s[9:-1]
                server_url = server_url.replace("$branch", self.branch)
                # Add the server to the list, also if bad
                self.serverList.append([current_country, "99.99", "99:99", server_url, 0, False])
                # Country, response time, last sync, url, quality level
                self.nbServer += 1
                if self.method == "random" :
                    print("->", server_url)
                    continue
                print("-> .....", server_url, end='')
                sys.stdout.flush()
                j = server_url.find(self.branch)
                url = server_url[0:j] + "state"
                start = time.time()
                try:
                    furl = urllib.request.urlopen(url, timeout=self.maxWaitTime)
                except:
                    print("\r-> Error!")
                    continue
                self.time_out(self.maxWaitTime)
                try:
                    resp = furl.read()
                    d = resp.find(b"date=")
                    signal.alarm(0)  # cancel alarm
                except:
                    print("\r-> Error2!")
                    furl.close()
                    continue
                elapsed = round((time.time() - start), 3)
                self.nbServerResp += 1  # The server responds ..
                date = resp[d+5:d+24].decode('utf-8')
                selapsed = "{:6.4}".format(Decimal(elapsed).quantize(Decimal('.001')))
                print("\r->", selapsed, sep="")
                sys.stdout.flush()
                self.serverList[self.nbServer - 1][1] = selapsed  # - response time
                self.serverList[self.nbServer - 1][4] = 1
                try:
                    date2 = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S" )
                except:
                    print('Wrong date format in "state" file. Server skipped.')
                    continue
                sec = (self.datenow - date2).seconds
                min = int(sec / 60)
                hr = int(min / 60)
                min = min - hr * 60
                if hr < 4:
                    self.nbServerGood += 1  # ...and was recently synced (< 4h)
                    self.serverList[self.nbServer - 1][4] = 2
                datesync = '{}:{}'.format(hr, str(min).zfill(2))
                self.serverList[self.nbServer - 1][2] = datesync  # - last sync
                furl.close()
            fi.close()

    #
    # Build the file "mirrorlist"
    # ===========================
    def write_mirrorlist_file(self):
        self.serverList = sorted(self.serverList, key=itemgetter(1))
        if self.interactive:
            finished = False
            for item in self.serverList:
                item[3] = item[3].replace("/" + self.branch + "/", "/$branch/")
            while not finished:
                chooseMirrors(True, self.serverList)
                customList = []
                for elem in self.serverList:
                    if elem[5]:
                        customList.append(elem)
                if len(customList) == 0:
                    continue
                finished = chooseMirrors(False, customList)

            custom_path = self.mirrorlistsDir + "/Custom"
            try:
                fcust = open(custom_path, "w")
            except:
                print("\n^GError : can't create file {0}.\n".format(custom_path))
                exit(1)
            fcust.write("##\n")
            fcust.write("## Pacman Mirrorlist\n")
            fcust.write("##\n\n")
            for elem in customList:
                fcust.write("[" + elem[0] + "]\n")
                fcust.write("Server = " + elem[3] + "\n")
            fcust.close()

            try:
                fconf = open(self.path_conf, "r")
            except:
                print("\n^GError : can't open file {0}.\n".format(self.path_conf))
                exit(1)
            buf = fconf.read().split('\n')
            fconf.close()
            while buf[-1:] == ['']:
                del buf[-1:]
            try:
                fconf = open(self.path_conf, "w")
            except:
                print("\n^GError : can't open file {0}.\n".format(self.path_conf))
                exit(1)
            for line in buf:
                if "OnlyCountry" in line:
                    fconf.write("OnlyCountry=Custom\n")
                else:
                    fconf.write(line + "\n")
            fconf.close
            try:
                fo = open(self.outputMirrorList, "w")
            except:
                print("\nError : cannot create", self.outputMirrorList)
                exit(1)
            fo.write("##\n")
            fo.write("## Manjaro Linux repository mirrorlist\n")
            fo.write("## Generated on ")
            fo.write(datetime.datetime.now().strftime("%d %B %Y %H:%M"))
            fo.write("\n##\n")
            fo.write("## Use pacman-mirrors to modify\n")
            fo.write("##\n\n")
            print("\nCustom List")
            print("-----------\n")
            for server in customList :
                server[3] = server[3].replace("$branch", self.branch)
                print("-> {0} :".format(server[0]), server[3])
                fo.write("\n## Location  : ")
                fo.write(server[0])
                if self.method == "rank" :
                    fo.write("\n## Time      :")
                    fo.write(server[1])
                    fo.write("\n## Last Sync : ")
                    fo.write(server[2])
                fo.write("\nServer = ")
                fo.write(server[3])
                fo.write("\n")
            print("\n:: Generated and saved '{}' Custom list.".format(self.outputMirrorList))

        else:
            try:
                fo = open(self.outputMirrorList, "w")
            except:
                print("\nError : cannot create", self.outputMirrorList)
                exit(1)
            fo.write("##\n")
            fo.write("## Manjaro Linux repository mirrorlist\n")
            fo.write("## Generated on ")
            fo.write(datetime.datetime.now().strftime("%d %B %Y %H:%M"))
            fo.write("\n##\n")
            fo.write("## Use pacman-mirrors to modify\n")
            fo.write("##\n\n")
            if self.nbServerGood >= 3:					# Avoid an empty mirrorlist
                level = 2
            elif self.nbServerResp >= 3:
                level = 1
            else:
                level = 0
                if self.nbServer == 0:
                    print("\nError : no server available !\n")
            for server in self.serverList:
                if server[4] < level:
                    continue
                fo.write("\n## Location  : ")
                fo.write(server[0])
                if self.method == "rank":
                    fo.write("\n## Time      :")
                    fo.write(server[1])
                    fo.write("\n## Last Sync : ")
                    fo.write(server[2])
                fo.write("\nServer = ")
                fo.write(server[3])
                fo.write("\n")
            print(":: Generated and saved '{}' mirrorlist.".format(self.outputMirrorList))

    def run(self):
        try:
            self.parse_configuration_file()
        except (FileNotFoundError, PermissionError) as e:
            print(e)
            exit(1)
        self.parse_command_line_arguments()
        self.query_servers()
        self.write_mirrorlist_file()

if __name__ == '__main__':
    if os.getuid() != 0:
        print("\nError : must be root.\n")
        exit(1)
    pm = PacmanMirrors()
    pm.run()

