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
        Gtk.Window.__init__(self, title=_("Mirrors list sorted by response time"))
        self.set_size_request(700, 350)
        self.set_border_width(10)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)

        mirrors_list = []
        for server in server_list:
            mirrors_list.append((Gtk.CheckButton(),
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

        header = Gtk.Label(_("Select by clicking mirrors to prepare your custom list"))
        buttonShow = Gtk.Button(_("Show custom list"))
        buttonShow.connect("clicked", self.show_list)

        page1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        page1.add(header)
        page1.add(scrolled_tree)
        page1.add(buttonShow)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_vexpand(True)
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        scrolled_window.add(self.box)
        buttonBack = Gtk.Button(_("Back to main list"))
        buttonBack.connect("clicked", self.back_list)
        self.buttonDone = Gtk.Button(_("Done"))
        self.buttonDone.connect("clicked", self.done)

        page2 = Gtk.Grid()
        page2.set_column_homogeneous(True)
        page2.set_row_spacing(10)
        page2.set_column_spacing(10)
        page2.attach(scrolled_window, 0, 0, 2, 1)
        page2.attach(buttonBack, 0, 1, 1, 1)
        page2.attach(self.buttonDone, 1, 1, 1, 1)

        self.stack.add_named(page1, "choice")
        self.stack.add_named(page2, "confirm")
        self.add(self.stack)

        # Server lists
        self.server_list = server_list
        self.custom_list = []

        self.is_done = False

    def on_toggle(self, widget, path):
        self.mirrors_liststore[path][0] = not self.mirrors_liststore[path][0]

    def show_list(self, button):
        # Reset custom list
        self.custom_list = []
        for element in self.box.get_children():
            self.box.remove(element)
        # Get selected elementqs
        for row in self.mirror_filter:
            if row[0]:
                for server in self.server_list:
                    if server["url"][:-20] == row[2]:
                        self.custom_list.append(server)
                        self.box.add(Gtk.Label("- " + row[2]))
        # Check if at least a server is selected
        if not self.custom_list:
            self.box.add(Gtk.Label(_("Please select at least one server")))
        self.buttonDone.set_sensitive(self.custom_list)
        # Show selected servers
        self.box.show_all()
        self.stack.set_visible_child_name("confirm")
        self.set_title(_("List of selected mirrors"))

    def back_list(self, button):
        # Return to the choice page
        self.stack.set_visible_child_name("choice")
        self.set_title(_("Mirrors list sorted by response time"))

    def done(self, button):
        # Confirm the action
        self.is_done = True
        Gtk.main_quit()

def launch(server_list):
    window = PacmanMirrors(server_list)
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    Gtk.main()
    return window
