#!/usr/bin/env python
"""pacman-mirrors api functions"""

import os
import sys
import tempfile

from pacman_mirrors.constants import txt


def find_mirrorlist_branch(filename):
    """find and return the branch found in mirrorlist"""
    try:
        with open(filename) as mirrorlist:
            for line in mirrorlist:
                if "Server = " in line:
                    workstring = line.strip()[-21:]  # /unstable/$repo/$arch
                    pos = workstring.find("/")
                    workstring = workstring[pos + 1:]
                    pos = workstring.find("/")
                    return workstring[:pos]
    except OSError as err:
        print(".: {} {}: {}: {}".format(txt.ERR_CLR,
                                        txt.CANNOT_READ_FILE,
                                        err.filename,
                                        err.strerror))
        sys.exit(2)


def normalize_config(filename):
    """Normalize configuration
    :param filename:
    """
    normalize_country(filename)
    normalize_method(filename)
    normalize_protocols(filename)
    normalize_ssl(filename)


def normalize_country(filename):
    """Write default OnlyCountry =
    :param filename:
    """
    lookfor = "OnlyCountry ="
    default = "# OnlyCountry =\n"
    with open(
        filename) as cnf, tempfile.NamedTemporaryFile(
        "w+t", dir=os.path.dirname(
            filename), delete=False) as tmp:
        replaced = False
        for line in cnf:
            if lookfor in line:
                tmp.write(default)
                replaced = True
            else:
                tmp.write("{}".format(line))
        if not replaced:
            tmp.write(default)
    os.replace(tmp.name, filename)
    os.chmod(filename, 0o644)


def normalize_method(filename):
    """Write default Method = rank
    :param filename:
    """
    lookfor = "Method ="
    default = "# Method = rank\n"
    with open(
        filename) as cnf, tempfile.NamedTemporaryFile(
        "w+t", dir=os.path.dirname(
            filename), delete=False) as tmp:
        replaced = False
        for line in cnf:
            if lookfor in line:
                tmp.write(default)
                replaced = True
            else:
                tmp.write("{}".format(line))
        if not replaced:
            tmp.write(default)
    os.replace(tmp.name, filename)
    os.chmod(filename, 0o644)


def normalize_protocols(filename):
    """Write default Protocols =
    :param filename:
    """
    lookfor = "Protocols ="
    default = "# Protocols =\n"
    with open(
        filename) as cnf, tempfile.NamedTemporaryFile(
        "w+t", dir=os.path.dirname(
            filename), delete=False) as tmp:
        replaced = False
        for line in cnf:
            if lookfor in line:
                tmp.write(default)
                replaced = True
            else:
                tmp.write("{}".format(line))
        if not replaced:
            tmp.write(default)
    os.replace(tmp.name, filename)
    os.chmod(filename, 0o644)


def normalize_ssl(filename):
    """Write default SSLVerify = False
    :param filename:
    """
    lookfor = "SSLVerify ="
    default = "# SSLVerify = False\n"
    with open(
        filename) as cnf, tempfile.NamedTemporaryFile(
        "w+t", dir=os.path.dirname(
            filename), delete=False) as tmp:
        replaced = False
        for line in cnf:
            if lookfor in line:
                tmp.write(default)
                replaced = True
            else:
                tmp.write("{}".format(line))
        if not replaced:
            tmp.write(default)
    os.replace(tmp.name, filename)
    os.chmod(filename, 0o644)


def sanitize_prefix(prefix):
    """Sanitize prefix
    :param prefix:
    :returns sanitized prefix
    """
    if prefix.endswith("/"):
        prefix = prefix[:-1]
    return prefix


def sanitize_url(url):
    """Sanitize url
    :param url:
    :returns sanitized url
    """
    if url.endswith("/"):
        return url
    return url + "/"


def write_config_branch(branch, filename, quiet=False):
    """Write branch"""
    lookfor = "Branch ="
    default = "# Branch = stable\n"
    if branch == "stable":
        branch = default
    else:
        branch = "Branch = {}\n".format(branch)
    try:
        with open(
            filename) as cnf, tempfile.NamedTemporaryFile(
            "w+t", dir=os.path.dirname(
                filename), delete=False) as tmp:
            replaced = False
            for line in cnf:
                if lookfor in line:
                    tmp.write(branch)
                    replaced = True
                else:
                    tmp.write("{}".format(line))
            if not replaced:
                tmp.write(branch)
        os.replace(tmp.name, filename)
        os.chmod(filename, 0o644)
        if not quiet:
            print(".: {} {}".format(txt.INF_CLR, txt.API_CONF_RE_BRANCH))
    except OSError as err:
        print(".: {} {}: {}: {}".format(txt.ERR_CLR,
                                        txt.CANNOT_READ_FILE,
                                        err.filename,
                                        err.strerror))
        sys.exit(2)


def write_mirrorlist_branch(newbranch, filename, quiet=False):
    """"""
    lookfor = "Server ="
    branch = find_mirrorlist_branch(filename)
    try:
        with open(filename) as mirrorlist, tempfile.NamedTemporaryFile(
            "w+t", dir=os.path.dirname(
                filename), delete=False) as tmp:
            for line in mirrorlist:
                if lookfor in line:
                    line = line.replace(branch, newbranch)
                    tmp.write("{}".format(line))
                else:
                    tmp.write("{}".format(line))
        os.replace(tmp.name, filename)
        os.chmod(filename, 0o644)
        if not quiet:
            print(".: {} {}".format(txt.INF_CLR, txt.API_MIRRORLIST_RE_BRANCH))
    except OSError as err:
        print(".: {} {}: {}: {}".format(txt.ERR_CLR,
                                        txt.CANNOT_READ_FILE,
                                        err.filename,
                                        err.strerror))
        sys.exit(2)


def write_protocols(protocols, filename, quiet=False):
    """Write branch"""
    lookfor = "Protocols ="
    default = "# Protocols = \n"
    if protocols:
        protocols = "Protocols = {}\n".format(",".join(protocols))
    else:
        protocols = default
    try:
        with open(
            filename) as cnf, tempfile.NamedTemporaryFile(
            "w+t", dir=os.path.dirname(
                filename), delete=False) as tmp:
            replaced = False
            for line in cnf:
                if lookfor in line:
                    tmp.write(protocols)
                    replaced = True
                else:
                    tmp.write("{}".format(line))
            if not replaced:
                tmp.write(protocols)
        os.replace(tmp.name, filename)
        os.chmod(filename, 0o644)
        if not quiet:
            print(".: {} {}".format(txt.INF_CLR, txt.API_CONF_PROTOCOLS))
    except OSError as err:
        print(".: {} {}: {}: {}".format(txt.ERR_CLR,
                                        txt.CANNOT_READ_FILE,
                                        err.filename,
                                        err.strerror))
        sys.exit(2)
