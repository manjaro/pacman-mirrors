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
#
"""
Pacman Mirrors
Console UI Module
"""
from collections import namedtuple
import npyscreen
from . import txt
from . console_helpers import ConsoleHelpers
from . import i18n

Util = ConsoleHelpers

_ = i18n.language.gettext

class ConsoleUI(npyscreen.NPSAppManaged):
    """
    App
    """

    def __init__(self, server_list):
        npyscreen.NPSAppManaged.__init__(self)
        # Server lists
        self.server_list = server_list
        self.custom_list = []
        self.is_done = False

    def main(self):
        """
        Main
        """
        main_server_list = []
        server = namedtuple("Server", ["country",
                                       "response_time",
                                       "last_sync",
                                       "url"])
        header_cols = ({"country": txt.I_COUNTRY,
                        "response_time": txt.I_RESPONSE,
                        "last_sync": txt.I_LAST_SYNC,
                        "url": txt.I_URL})
        main_server_list.append(header_cols)
        main_server_list.extend(self.server_list)
        servers = Util.list_to_tuple(main_server_list, server)
        server_rows = Util.rows_from_tuple(servers)
        header_row = ("{:<5}".format(txt.I_USE) +
                      (server_rows[0].replace("|", " ").strip()))
        del server_rows[0]
        # setup form
        mainform = npyscreen.Form(name=txt.I_TITLE)
        mainform.add(npyscreen.TitleFixedText, name=txt.I_LIST_TITLE)
        mainform.add(npyscreen.TitleFixedText, name=header_row)
        selected_servers = mainform.add(npyscreen.MultiSelect,
                                        max_height=0,
                                        name=txt.I_LIST_TITLE,
                                        value=[],
                                        values=server_rows,
                                        scroll_exit=True)
        # activate form
        mainform.edit()
        # done
        self.done(selected_servers.get_selected_objects())

    def done(self, selection):
        """
        After editing

        :param selection:
        """
        if selection:
            for mirror in selection:
                server = mirror.split("|")
                self.custom_list.append({"country": server[0].strip(),
                                         "response_time": server[1].strip(),
                                         "last_sync": server[2].strip(),
                                         "url": server[3].strip()})

        self.is_done = True
        self.setNextForm(None)


def run(server_list):
    """
    Run
    """
    app = ConsoleUI(server_list)
    app.run()
    return app
