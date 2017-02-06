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
# Authors: Esclapion
#          Hugo Posnic <huluti@manjaro.org>

"""
Pacman-Mirrors
Graphical UI Module
"""

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from . import i18n
from . import txt


_ = i18n.language.gettext


class GraphicalUI(Gtk.Window):
    """Class GraphicalUI"""
    def __init__(self, server_list):
        Gtk.Window.__init__(self, title=txt.I_TITLE)
        self.set_size_request(700, 350)
        self.set_border_width(10)
        self.set_position(Gtk.WindowPosition.CENTER)

        mirrors_list = []
        for server in server_list:
            mirrors_list.append((
                False, server["country"],
                "{}h {}m".format(server["last_sync"][:2],
                                 server["last_sync"][-2:]),
                server["url"][:-20]))
        self.mirrors_liststore = Gtk.ListStore(bool, str, str, str)
        for mirror_ref in mirrors_list:
            self.mirrors_liststore.append(list(mirror_ref))
        self.mirror_filter = Gtk.TreeModelSort(self.mirrors_liststore)
        scrolled_tree = Gtk.ScrolledWindow()
        self.treeview = Gtk.TreeView.new_with_model(self.mirror_filter)
        self.treeview.set_vexpand(True)
        renderer = Gtk.CellRendererToggle()
        renderer.connect("toggled", self.on_toggle)
        column = Gtk.TreeViewColumn(txt.I_USE, renderer, active=0)
        self.treeview.append_column(column)
        for i, column_title in enumerate([txt.I_COUNTRY,
                                          txt.I_LAST_SYNC,
                                          txt.I_URL]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i+1)
            self.treeview.append_column(column)
        scrolled_tree.add(self.treeview)

        header = Gtk.Label(txt.I_LIST_TITLE)
        button_cancel = Gtk.Button(txt.I_CANCEL)
        button_cancel.connect("clicked", self.cancel)
        self.button_done = Gtk.Button(txt.I_CONFIRM)
        self.button_done.set_sensitive(False)
        self.button_done.connect("clicked", self.done)
        
        grid = Gtk.Grid(column_homogeneous=True,
                        column_spacing=10,
                        row_spacing=10)
        grid.attach(header, 0, 0, 2, 1)
        grid.attach(scrolled_tree, 0, 1, 2, 1)
        grid.attach(button_cancel, 0, 2, 1, 1)
        grid.attach(self.button_done, 1, 2, 1, 1)

        self.add(grid)

        # Server lists
        self.server_list = server_list
        self.custom_list = []

        self.is_done = False

    def on_toggle(self, widget, path):
        """Add or remove server from custom list"""
        self.mirrors_liststore[path][0] = not self.mirrors_liststore[path][0]
        if self.mirrors_liststore[path][0]:
            for server in self.server_list:
                if server["url"][:-20] == self.mirrors_liststore[path][3]:
                    self.custom_list.append(server)
        else:
            for server in self.custom_list:
                if server["url"][:-20] == self.mirrors_liststore[path][3]:
                    self.custom_list.remove(server)
        self.button_done.set_sensitive(bool(self.custom_list))

    def cancel(self, button):
        """Cancel mirrorlist"""
        self.custom_list = []
        self.is_done = True
        Gtk.main_quit()

    def done(self, button):
        """Confirm choice"""
        dialog = Gtk.Dialog(txt.I_CONFIRM_SELECTION, None, 0, (
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK))
        dialog.set_transient_for(self)
        dialog.set_border_width(10)
        box = dialog.get_content_area()
        box.set_spacing(10)
        box.add(Gtk.Label(txt.I_USE_THESE_MIRRORS))
        dialog.show_all()
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            # Quit GUI
            dialog.destroy()
            self.is_done = True
            Gtk.main_quit()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()  # Go back to selection


def run(server_list):
    """Run"""
    window = GraphicalUI(server_list)
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    Gtk.main()
    return window
