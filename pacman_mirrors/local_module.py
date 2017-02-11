#!/usr/bin/env python3

"""Manjaro-Mirrors Local Module"""

import datetime
import json
import os
import tempfile
from collections import OrderedDict
from . import txt

class FileHandler():
    """FileHandler class"""

    def write_json(self, data, filename):
        """
        Writes a named json file

        :param data:
        :param filename:
        """
        try:
            with open(filename, "w") as outfile:
                json.dump(data, outfile)
            return True

        except OSError:
            return False

    def read_json(self, filename):
        """
        Reads a named json file

        :param filename:
        :return data: OrderedDict
        """
        result = list()
        try:
            with open(filename, "r") as infile:
                result = json.loads(infile.read().decode(
                    "utf8"), object_pairs_hook=OrderedDict)
        except OSError:
            return False

        return result

    def write_config_to_file(self, config_file, selected_countries, custom):
        """Writes the configuration to file"""
        if custom:
            if selected_countries == ["Custom"]:
                selection = "OnlyCountry = Custom\n"
            else:
                selection = ("OnlyCountry = {list}\n").format(
                    list=",".join(selected_countries))
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
            print("{}: {}: {}: {}".format(txt.ERROR, txt.ERR_FILE_READ,
                                          err.filename, err.strerror))
            exit(1)

    def write_mirror_file_header(self, data, filename):
        """
        Write mirrorfile

        :param handle: handle to a file opened for writing
        """
        self.write_json(data, filename)

    def write_mirror_list_header(self, handle, custom=False):
        """
        Write mirrorlist header

        :param handle: handle to a file opened for writing
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

    def write_mirror_list_entry(self, handle, mirror):
        """
        Write mirror to mirror list or file

        :param handle: handle to a file opened for writing
        :param mirror: mirror object
        """
        handle.write("## Country       : {}\n".format(mirror["country"]))
        if mirror["response_time"] == txt.SERVER_RES:
            mirror["response_time"] = "N/A"
        handle.write("## Response time : {}\n".format(mirror["response_time"]))
        if mirror["last_sync"] == txt.SERVER_BAD or mirror["last_sync"] == txt.LASTSYNC_NA:
            mirror["last_sync"] = "N/A"
        handle.write("## Last sync     : {}h\n".format(mirror["last_sync"]))
        handle.write("Server = {}\n\n".format(mirror["url"]))

