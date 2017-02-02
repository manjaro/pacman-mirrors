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

"""
Pacman-Mirrors
Text Module
"""

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
# error messages
ERR_FILE_READ = _("Cannot read file")
ERR_FILE_UPDATE = _("Cannot update file")
ERR_FILE_WRITE = _("Cannot write file")
ERR_NOT_ROOT = _("Must have root privileges")
ERR_SERVER_HTTP_EXCEPTION = _("Cannot read server response")
ERR_SERVER_NOT_AVAILABLE = _("server not available")
ERR_SERVER_NOT_REACHABLE = _("Failed to reach server")
ERR_SERVER_REQUEST = _("The server did not complete the request")
# info messages
INF_AVAILABLE_COUNTRIES = _("Available countries are")
INF_CUSTOM_MIRROR_FILE = _("Custom mirrors file")
INF_DOES_NOT_EXIST = _("doesn't exist.")
INF_INTERACTIVE_LIST = _("User generated mirror list")
INF_INTERACTIVE_LIST_SAVED = _("Saved personalized list of mirrors in")
INF_IS_MISSING = _("is missing")
INF_MIRROR_LIST_RESET = _("Use `pacman-mirrors -c all` to reset list")
INF_MIRROR_LIST_SAVED = _("Mirrorlist generated and saved to")
INF_MIRROR_LIST_WRITE = _("Writing mirror list")
INF_NO_SELECTION = _("No mirrors in selection")
INF_NO_CHANGES = _("The mirror list is not changed")
INF_OPTION = _("Option")
INF_OUTPUT_MIRROR_FILE = _("Writing custom mirror file")
INF_QUERY_ALL_SERVERS = _("Querying all servers")
INF_QUERY_TIME_INFO = _("Querying servers, this may take some time")
INF_QUERY_CUSTOM = _("Using custom mirror list")
INF_QUERY_DEFAULT = _("Testing mirrors in")
INF_QUERY_WRONG_DATE_FORMAT = _("Wrong date format in state file")
INF_RANDOMIZE_SERVERS = _("Randomizing server list")
INF_UNKNOWN_COUNTRY = _("unknown country")
INF_USING_ALL_SERVERS = _("Using all servers")
# interactive messages
I_TITLE = _("Manjaro mirrors by response time")
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

# mirror status constants
LASTSYNC_OK = "24:00"  # last syncronize in the past 24 hours
LASTSYNC_NA = "98:00"  # last syncronization not available
SERVER_BAD = "99:99"  # default last syncronization status
SERVER_RES = "99.99"  # default response status
# control
NEWLINE = "\n"
# indicators
DCS = ":: "
SAS = "=> "
DAS = "==> "
DOT = "."
DOTS = "..."
SEP = ": "
# options
OPT_COUNTRY = " '-c/--country' "
OPT_NOUPDATE = " 'NoUpdate = True' "
