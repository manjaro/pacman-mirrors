#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
# Author(s): Esclapion
#            Hugo Posnic

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from . import i18n
_ = i18n.language.gettext


class PacmanMirrors(Gtk.Window):
    def __init__(self, server_list):
        Gtk.Window.__init__(self, title=_("List of mirrors sorted by response time"))
        self.set_size_request(700, 350)
        self.set_border_width(10)
        self.set_position(Gtk.WindowPosition.CENTER)

        mirrors_list = []
        for server in server_list:
            mirrors_list.append((False,
                                 server["last_sync"],
                                 server["url"][:-20],
                                 server["country"]))
        self.mirrors_liststore = Gtk.ListStore(bool, str, str, str)
        for mirror_ref in mirrors_list:
            self.mirrors_liststore.append(list(mirror_ref))
        self.mirror_filter = Gtk.TreeModelSort(self.mirrors_liststore)
        scrolled_tree = Gtk.ScrolledWindow()
        self.treeview = Gtk.TreeView.new_with_model(self.mirror_filter)
        self.treeview.set_vexpand(True)
        renderer = Gtk.CellRendererToggle()
        renderer.connect("toggled", self.on_toggle)
        column = Gtk.TreeViewColumn(_("Use?"), renderer, active=0)
        self.treeview.append_column(column)
        for i, column_title in enumerate([_("Last sync (hh:mm)"), _("URL"), _("Country")]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i+1)
            self.treeview.append_column(column)
        scrolled_tree.add(self.treeview)

        header = Gtk.Label(_("Tick mirrors to prepare your custom list"))
        self.buttonDone = Gtk.Button(_("Confirm selection"))
        self.buttonDone.connect("clicked", self.done)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        box.add(header)
        box.add(scrolled_tree)
        box.add(self.buttonDone)

        self.add(box)

        # Server lists
        self.server_list = server_list
        self.custom_list = []

        self.is_done = False

    def on_toggle(self, widget, path):
        self.mirrors_liststore[path][0] = not self.mirrors_liststore[path][0]

    def done(self, button):
        # Reset custom list
        self.custom_list = []
        # Get selected servers
        for row in self.mirror_filter:
            if row[0]:
                for server in self.server_list:
                    if server["url"][:-20] == row[2]:
                        self.custom_list.append(server)
        if self.custom_list:
            # If at least one server is selected
            dialog = Gtk.Dialog("Are you sure?", None, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK))
            dialog.set_transient_for(self)
            dialog.set_border_width(10)
            box = dialog.get_content_area()
            box.set_spacing(10)
            box.add(Gtk.Label("Are you sure to replace your list of mirrors?"))
            dialog.show_all()
            response = dialog.run()

            if response == Gtk.ResponseType.OK:
                # Quit GUI
                dialog.destroy()
                self.is_done = True
                Gtk.main_quit()
            elif response == Gtk.ResponseType.CANCEL:
                # Go back to selection
                dialog.destroy()
        else:
            # No selected server
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
            Gtk.ButtonsType.OK, _("No selected server"))
            dialog.format_secondary_text(_("Please select at least one server"))
            dialog.set_title(_("An error occured"))
            dialog.run()
            dialog.destroy()

def launch(server_list):
    window = PacmanMirrors(server_list)
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    Gtk.main()
    return window
