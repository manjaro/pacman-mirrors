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

"""Pacman-Mirrors Text Module"""

from . import i18n


_ = i18n.language.gettext


# TRANSLATABLE STRINGS

# message type
ERROR = _("Error")
INFO = _("Info")
WARN = _("Warning")
# error types
TIMEOUT = _("Timeout")
HTTP_EXCEPTION = _("HTTPException")
# special words
PATH = _("PATH")
FILE = _("FILE")
SECONDS = _("SECONDS")
DIGIT = _("DIGIT")
# help messages
HLP_ARG_BRANCH = _("Branch name")
HLP_ARG_COUNTRY = _(
    "Comma separated list of countries, from which mirrors will be used")
HLP_ARG_FILE = _("Output file")
HLP_ARG_GENERATE = _("Generate mirrorlist")
HLP_ARG_GEOIP_P1 = _("Get current country using geolocation. Ignored if")
HLP_ARG_GEOIP_P2 = _("is supplied")
HLP_ARG_INTERACTIVE = _("Generate custom mirrorlist")
HLP_ARG_METHOD = _("Generation method")
HLP_ARG_NOUPDATE_P1 = _("Don't generate mirrorlist if")
HLP_ARG_NOUPDATE_P2 = _("in the configuration file")
HLP_ARG_PATH = _("Mirrors list path")
HLP_ARG_QUIET = _("Quiet mode - less verbose output")
HLP_ARG_TIMEOUT = _("Maximum waiting time for server response")
HLP_ARG_VERSION = _("Print the pacman-mirrors version")
HLP_ARG_FASTTRACK = _("A quick mirrorlist. Overrides")
# messages
AVAILABLE_COUNTRIES = _("Available countries are")
CANNOT_DOWNLOAD_FILE = _("Could not download from")
CANNOT_READ_FILE = _("Cannot read file")
CANNOT_WRITE_FILE = _("Cannot write file")
CONVERT_CUSTOM_MIRROR_FILE = _("Converting custom mirror file to new format")
CUSTOM_MIRROR_FILE = _("Custom mirror file")
CUSTOM_MIRROR_FILE_SAVED = _("Custom mirror file saved")
CUSTOM_MIRROR_LIST = _("User generated mirror list")
DOES_NOT_EXIST = _("doesn't exist.")
DOWNLOADING_MIRROR_FILE = _("Downloading mirrors from")
FALLING_BACK = _("Falling back to")
IS_MISSING = _("is missing")
MIRROR_FILE = _("The mirror file")
MIRROR_LIST_SAVED = _("Mirrorlist generated and saved to")
MIRROR_RANKING_NA = _("Mirror ranking is not available")
MUST_BE_ROOT = _("Must have root privileges")
INTERNET_DOWN = _("Internet connection appears to be down")
INTERNET_REQUIRED = _("Internet access is required to proceed")
INTERNET_ALTERNATIVE = _(
    "Pacman needs a mirrorlist. Use -m random to create a it without network")
NO_CHANGE = _("The mirror list is not changed")
NO_SELECTION = _("No mirrors in selection")
OPTION = _("Option")
WRITING_MIRROR_LIST = _("Writing mirror list")
QUERY_MIRRORS = _("Querying mirrors")
RANDOMIZING_SERVERS = _("Randomizing mirror list")
RESET_CUSTOM_CONFIG = _("To reset custom config run ")
TAKES_TIME = _("This may take some time")
UNKNOWN_COUNTRY = _("unknown country")
USING_ALL_MIRRORS = _("Using all mirrors")
USING_CUSTOM_FILE = _("Using custom mirror file")
USING_DEFAULT_FILE = _("Using default mirror file")
# interactive messages
I_TITLE = _("Manjaro mirrors by response time")
I_TITLE_RANDOM = _("Manjaro mirrors in random order")
I_LIST_TITLE = _("Check mirrors for your personal list")
I_USE = _("Use")
I_COUNTRY = _("Country")
I_RESPONSE = _("Resp")
I_LAST_SYNC = _("Sync")
I_URL = _("URL")
I_CANCEL = _("Cancel")
I_CONFIRM = _("OK")
I_CONFIRM_SELECTION = _("Confirm selections")
I_USE_THESE_MIRRORS = _("I want to use these mirrors")

# NON TRANSLATABLE STRINGS
HOUSTON = "Houston?! We have a problem."
OVERRIDE_OPT = "-c -i -m --geoip"
REPO_SERVER = "repo.manjaro.org"
RESET_TIP = "pacman-mirror -c all"
# mirror status constants
LASTSYNC_OK = "24:00"  # last syncronize in the past 24 hours
LASTSYNC_NA = "98:00"  # last syncronization not available
SERVER_BAD = "99:99"  # default last syncronization status
SERVER_RES = "99.99"  # default response status
# options
OPT_COUNTRY = " '-c/--country' "
OPT_NOUPDATE = " 'NoUpdate = True' "
OPT_RANDOM = " '-m/--method random "
# colors
DBG_CLR = "\033[1;46m.: {} >>> \033[1;m".format("DEBUG")
ERR_CLR = "\033[1;31m{}\033[1;m".format(ERROR)
INF_CLR = "\033[1;37m{}\033[1;m".format(INFO)
WRN_CLR = "\033[1;33m{}\033[1;m".format(WARN)
CE = "\033[1;m"
GS = "\033[1;32m"
RS = "\033[1;31m::"
YS = "\033[1;33m"
BS = "\033[1;34m"
WS = "\033[1;37m"
