#!/usr/bin/env python3

"""Manjaro-Mirrors Local Module"""

import datetime
import os
import tempfile
from . import txt


class FileFn:
    """FileMethods class"""

    @staticmethod
    def check_directory(dir_name):
        """Check necessary directory"""
        os.makedirs(dir_name, mode=0o755, exist_ok=True)

    @staticmethod
    def check_file(filename):
        """Check if file exist"""
        if os.path.isfile(filename):
            return True
        return False

    @staticmethod
    def write_mirror_config(config_file, countryselection, custom):
        """Writes the configuration to file"""
        if custom:
            if countryselection == ["Custom"]:
                selection = "OnlyCountry = Custom\n"
            else:
                selection = "OnlyCountry = {list}\n".format(
                    list=",".join(countryselection))
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

    @staticmethod
    def write_mirror_list_header(handle, custom=False):
        """
        Write mirrorlist header

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
        """
        Write mirror to mirror list or file

        :param handle: handle to a file opened for writing
        :param mirror: mirror object
        """
        work = mirror
        handle.write("## Country       : {}\n".format(work["country"]))
        if work["response_time"] == txt.SERVER_RES:
            work["response_time"] = "N/A"
        handle.write("## Response time : {}\n".format(work["response_time"]))
        if work["last_sync"] == txt.SERVER_BAD or \
                work["last_sync"] == txt.LASTSYNC_NA:
            work["last_sync"] = "N/A"
        handle.write("## Last sync     : {}h\n".format(work["last_sync"]))
        handle.write("Server = {}\n\n".format(work["url"]))
