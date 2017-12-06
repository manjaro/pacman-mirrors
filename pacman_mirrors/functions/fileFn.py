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

"""Manjaro-Mirrors File Functions"""

import datetime
import os
import sys

import pacman_mirrors.functions.util
from pacman_mirrors.constants import colors as color
from pacman_mirrors.constants import txt
from pacman_mirrors.functions import jsonFn


def check_existance_of(filename, folder=False):
    """
    Check existence of named file
    :param filename:
    :param folder:
    :returns bool if existing
    """
    if folder:
        return os.path.isdir(filename)
    return os.path.isfile(filename)


def create_dir(foldername):
    """
    Create named folder if not exist
    :param foldername:
    """
    os.makedirs(foldername, mode=0o755, exist_ok=True)


def delete_file(filename):
    """
    Delete the named file if exist
    :param filename:
    :return:
    """
    if os.path.isfile(filename):
        os.remove(filename)


def return_mirror_filename(config):
    """
    Find the mirror pool file
    :param config: config dictionary
    :returns tuple with file and status
    """
    filename = ""
    status = False  # status.json or mirrors.json
    # decision on file availablity
    if check_existance_of(config["status_file"]):
        status = True
        filename = config["status_file"]
    elif check_existance_of(config["mirror_file"]):
        filename = config["mirror_file"]
    if not filename:
        print("\n{}.:! {}{}\n".format(color.RED,
                                      txt.HOUSTON,
                                      color.ENDCOLOR))
        sys.exit(3)
    return filename, status


def write_mirror_list(config, servers, custom=False,
                      quiet=False, interactive=False):
    """
    Write servers to /etc/pacman.d/mirrorlist
    :param config: configuration dictionary
    :param servers: list of servers to write
    :param custom: flag
    :param quiet: flag
    :param interactive: flag
    """
    try:
        with open(config["mirror_list"], "w") as outfile:
            if not quiet:
                print(".: {} {}".format(txt.INF_CLR, txt.WRITING_MIRROR_LIST))
            # write list header
            write_mirrorlist_header(outfile, custom=custom)
            cols, lines = pacman_mirrors.functions.util.terminal_size()
            for server in servers:
                if server["resp_time"] == "99.99":
                    # do not write bad servers to mirrorlist
                    continue
                if interactive:
                    server["url"] = "{}{}{}".format(server["url"],
                                                    config["branch"],
                                                    config["repo_arch"])
                    if not quiet:
                        message = "   {:<15} : {}".format(server["country"],
                                                          server["url"])
                        print("{:.{}}".format(message, cols))
                else:
                    url = server["url"]
                    protocol = server["protocols"][0]
                    pos = url.find(":")
                    msg_url = server["url"] = "{}{}{}".format(protocol,
                                                              url[pos:],
                                                              config["branch"])

                    server["url"] = "{}{}{}{}".format(protocol,
                                                      url[pos:],
                                                      config["branch"],
                                                      config["repo_arch"])
                    if not quiet:
                        message = "   {:<15} : {}".format(server["country"],
                                                          msg_url)
                        print("{:.{}}".format(message, cols))

                # write list entry
                write_mirrorlist_entry(outfile, server)
            if not quiet:
                print(".: {} {}: {}".format(txt.INF_CLR,
                                            txt.MIRROR_LIST_SAVED,
                                            config["mirror_list"]))
    except OSError as err:
        print(".: {} {}: {}: {}".format(txt.ERR_CLR,
                                        txt.CANNOT_WRITE_FILE,
                                        err.filename,
                                        err.strerror))
        sys.exit(2)


def read_mirror_file(filename):
    """
    Read content of named file - json data assumed
    :param filename:
    :returns: list of mirrors
    """
    return jsonFn.read_json_file(filename, dictionary=True)


def write_mirrorlist_header(handle, custom=False):
    """
    Write mirrorlist header
    :param handle: handle to a file opened for writing
    :param custom: controls content of the header
    """
    # handle creation time in unicode
    # http://stackoverflow.com/questions/16034060/
    #  python3-datetime-datetime-strftime-failed-to-accept-utf-8-string-format
    generated_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    handle.write("##\n")
    if custom:
        handle.write("## Manjaro Linux {}\n".format(
            txt.MIRROR_LIST_CUSTOM_HEADER))
        handle.write("## {} {}\n".format(
            txt.MIRROR_LIST_GENERATED_ON, generated_timestamp))
        handle.write("##\n")
        handle.write("## {} '{}' {}\n## {} '{}' {}\n## {} '{}'\n".format(
            txt.PLEASE_USE, txt.MODIFY_CUSTOM, txt.MIRROR_LIST_CUSTOM_RESET,
            txt.PLEASE_USE, txt.RESET_ALL, txt.MIRROR_LIST_CUSTOM_RESET,
            txt.REMOVE_CUSTOM_CONFIG, txt.RESET_ALL))
    else:
        handle.write("## Manjaro Linux {}\n".format(
            txt.MIRROR_LIST_DEFAULT_HEADER))
        handle.write("## {} {}\n".format(
            txt.MIRROR_LIST_GENERATED_ON, generated_timestamp))
        handle.write("##\n")
        handle.write("## {} '{} {}' {}\n## ({})\n".format(
            txt.PLEASE_USE, txt.MODIFY_DEFAULT, txt.NUMBER,
            txt.MIRROR_LIST_DEFAULT_MODIFY, txt.USE_ZERO_FOR_ALL))
    handle.write("##\n\n")


def write_mirrorlist_entry(handle, mirror):
    """
    Write mirror to mirror list or file
    :param handle: handle to a file opened for writing
    :param mirror: mirror object
    """
    workitem = mirror
    handle.write("## Country : {}\n".format(workitem["country"]))
    handle.write("Server = {}\n\n".format(workitem["url"]))
