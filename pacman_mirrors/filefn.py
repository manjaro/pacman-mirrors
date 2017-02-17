#!/usr/bin/env python3

"""Manjaro-Mirrors Local Module"""

import os


class FileFn:
    """FileMethods class"""

    @staticmethod
    def dir_must_exist(dir_name):
        """Check necessary directory"""
        os.makedirs(dir_name, mode=0o755, exist_ok=True)

    @staticmethod
    def check_file(filename):
        """Check if file exist"""
        return os.path.isfile(filename)
