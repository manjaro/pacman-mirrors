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
# Authors: Frede Hundewadt <frede@hundewadt.dk>

"""Manjaro-Mirrors File Functions"""

import os
import datetime
from .configuration import REPO_ARCH
from .jsonfn import JsonFn
from .miscfn import MiscFn
from . import txt


class FileFn:
    """FileMethods class"""

    @staticmethod
    def check_file(filename):
        """Check if file exist"""
        return os.path.isfile(filename)

    @staticmethod
    def dir_must_exist(dir_name):
        """Check necessary directory"""
        os.makedirs(dir_name, mode=0o755, exist_ok=True)

    @staticmethod
    def output_mirror_list(branch, mirrorlistfile, servers, custom=False, quiet=False):
        """Write servers to /etc/pacman.d/mirrorlist
        :param: servers: list of servers to write
        """
        try:
            with open(mirrorlistfile, "w") as outfile:
                print(".: {} {}".format(txt.INF_CLR, txt.INF_MIRROR_LIST_WRITE))
                # write list header
                FileFn.write_mirrorlist_header(outfile, custom=custom)
                for server in servers:
                    url = server["url"]
                    for protocol in enumerate(server["protocols"]):
                        pos = url.find(":")
                        server["url"] = "{}{}{}{}".format(protocol[1],
                                                          url[pos:],
                                                          branch,
                                                          REPO_ARCH)
                        # write list entry
                        FileFn.write_mirrorlist_entry(outfile, server)
                        if not quiet:
                            print("   {}{:<15}{} : {}".format(txt.YS,
                                                              server["country"],
                                                              txt.CE,
                                                              server["url"]))
                print(".: {} {}: {}".format(txt.INF_CLR,
                                            txt.INF_MIRROR_LIST_SAVED,
                                            mirrorlistfile))
        except OSError as err:
            print(".: {} {}: {}: {}".format(txt.ERR_CLR,
                                            txt.ERR_FILE_WRITE,
                                            err.filename,
                                            err.strerror))
            exit(1)

    @staticmethod
    def read_mirror_file(filename):
        """Read a mirror file
        :returns: list of mirrors
        """
        return JsonFn.read_json_file(filename, dictionary=True)

    @staticmethod
    def write_mirrorlist_header(handle, custom=False):
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
    def write_mirrorlist_entry(handle, mirror):
        """Write mirror to mirror list or file
        :param handle: handle to a file opened for writing
        :param mirror: mirror object
        """
        workitem = mirror
        handle.write("## Country       : {}\n".format(workitem["country"]))
        # TODO: approval to remove useless lines
        # Commented since the info after a short time
        # is no longer valid
        if workitem["resp_time"] == txt.SERVER_RES:
            workitem["resp_time"] = "N/A"
        handle.write("## Response time : {}\n".format(
            workitem["resp_time"]))
        if workitem["last_sync"] == txt.SERVER_BAD or \
                workitem["last_sync"] == txt.LASTSYNC_NA:
            workitem["last_sync"] = "N/A"
        handle.write("## Last Upd hh:mm: {}\n".format(
            workitem["last_sync"]))
        handle.write("Server = {}\n\n".format(workitem["url"]))
