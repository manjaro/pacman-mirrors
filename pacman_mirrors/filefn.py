#!/usr/bin/env python3

"""Manjaro-Mirrors Local Module"""

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
