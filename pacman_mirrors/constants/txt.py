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

from pacman_mirrors.translation import i18n

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
NUMBER = _("NUMBER")
# help messages
HLP_ARG_API_GET_BRANCH = _("Return branch from configuration")
HLP_ARG_API_PREFIX = _("Set prefix to")
HLP_ARG_API_PROTOCOLS = _("Replace protocols in configuration")
HLP_ARG_API_RE_BRANCH = _("Replace branch in mirrorlist")
HLP_ARG_API_SET_BRANCH = _("Replace branch in configuration")
HLP_ARG_API_URL = _("Replace mirror url in mirrorlist")
HLP_ARG_BRANCH = _("Branch name")
HLP_ARG_COUNTRY = _(
    "Comma separated list of countries, from which mirrors will be used")
HLP_ARG_DEFAULT = _("Load default mirror file")
HLP_ARG_FASTTRACK = _("Generate mirrorlist with a number of up-to-date mirrors. Ignores:")
HLP_ARG_GENERATE = _("Generate mirrorlist with defaults")
HLP_ARG_GEOIP = _("Get current country using geolocation")
HLP_ARG_LIST = _("List all available countries")
HLP_ARG_INTERACTIVE = _("Generate custom mirrorlist")
HLP_ARG_METHOD = _("Generation method")
HLP_ARG_NO_MIRRORLIST = _("Use to skip generation of mirrorlist")
HLP_ARG_QUIET = _("Quiet mode - less verbose output")
HLP_ARG_SYNC = _("Syncronize pacman databases")
HLP_ARG_TIMEOUT = _("Maximum waiting time for server response")
HLP_ARG_VERSION = _("Print the pacman-mirrors version")
# messages
API_CONF_RE_BRANCH = _("Branch in config is changed")
API_CONF_PROTOCOLS = _("Protocols in config is changed")
API_ERROR_BRANCH = _("Re-branch requires a branch to work with")
API_MIRRORLIST_RE_BRANCH = _("Branch in mirror list is changed")
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
MIRROR_LIST_SAVED = _("Mirror list generated and saved to")
MIRROR_RANKING_NA = _("Mirror ranking is not available")
MUST_BE_ROOT = _("Must have root privileges")
INTERNET_DOWN = _("Internet connection appears to be down")
INTERNET_ALTERNATIVE = _("Mirror list is generated using random method")
NO_CHANGE = _("The mirrors has not changed")
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
OVERRIDE_OPT = "--country --interactive --method --geoip"
REPO_SERVER = "repo.manjaro.org"
RESET_TIP = "pacman-mirrors -c all"
PREFIX_TIP = ": $mnt | /mnt/install"
# options
OPT_RANDOM = " '-m/--method random' "
OPT_COUNTRY = " 'c/--country' "
# mirror status constants
LASTSYNC_OK = "24:00"  # last syncronize in the past 24 hours
LASTSYNC_NA = "9800:00"  # last syncronization not available
SERVER_BAD = "9999:99"  # default last syncronization status
SERVER_RES = "99.99"  # default response status
# colors
ERR_CLR = "\033[1;31m{}\033[1;m".format(ERROR)
INF_CLR = "\033[1;37m{}\033[1;m".format(INFO)
WRN_CLR = "\033[1;33m{}\033[1;m".format(WARN)
