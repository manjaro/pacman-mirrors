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

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from . import i18n
_ = i18n.language.gettext


def chooseMirrors(indEdit, travList):

    global index, nbItems, indPage, indDone
    tabSync = []
    tabButton = []
    tabCountries = []
    nbItems = 12
    indDone = False
    index = 0
    indPage = False
    indShortList = len(travList) <= nbItems
    if indShortList:
        nbItems = len(travList)

    def truncName(name):
        return name[7:-12]

    def displayPage():
        global index, nbItems, indPage
        indPage = True
        for i in range(nbItems):
            if index < len(travList):
                tabSync[i].set_label(travList[index]['last_sync'] + " |")
                tabButton[i].set_label(truncName(travList[index]['url']))
                if indEdit:
                    tabButton[i].set_relief(Gtk.ReliefStyle.NORMAL)
                    tabButton[i].set_active(travList[index]['selected'])
                tabCountries[i].set_label("| " + travList[index]['country'])
            else:
                tabSync[i].set_label("")
                tabButton[i].set_label("")
                if indEdit:
                    tabButton[i].set_relief(Gtk.ReliefStyle.NONE)
                    tabButton[i].set_active(False)
                tabCountries[i].set_label("")
            index += 1
        if not indShortList:
            if index > nbItems:
                buttonPrev.set_relief(Gtk.ReliefStyle.NORMAL)
                buttonPrev.set_label(_("Previous page"))
            else:
                buttonPrev.set_relief(Gtk.ReliefStyle.NONE)
                buttonPrev.set_label(" ")
            if index < len(travList):
                buttonNext.set_relief(Gtk.ReliefStyle.NORMAL)
                buttonNext.set_label(_("Next page"))
            else:
                buttonNext.set_relief(Gtk.ReliefStyle.NONE)
                buttonNext.set_label(" ")

        indPage = False

    def nextPage(self):
        global index
        if index < len(travList):
            displayPage()

    def prevPage(self):
        global index
        val = 2 * nbItems
        if index >= val:
            index -= val
            displayPage()

    def toggled(self):
        if indPage is False:
            name = self.get_label()
            if name != '':
                for elem in travList:
                    if truncName(elem['url']) == name:
                        elem['selected'] = self.get_active()
                        break
            else:
                self.set_active(False)

    def showList(self):
        Gtk.main_quit()

    def deleteEvent(self, Widget):
        exit(1)

    def backMain(self):
        Gtk.main_quit()

    def backDone(self):
        global indDone
        indDone = True
        Gtk.main_quit()

    win = Gtk.Window()
    win.set_resizable(False)
    if indEdit:
        win.set_title(_("Mirrors list sorted by response time"))
    else:
        win.set_title(_("List of selected mirrors"))
    win.set_border_width(10)
    mainbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=30)
    win.add(mainbox)

    if indEdit:
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        header = Gtk.Label(label=_("Select by clicking mirrors to prepare "
                                   "your custom list"))
        vbox.add(header)
        mainbox.add(vbox)

    hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

    vbox2c = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    for i in range(nbItems):
        Label = Gtk.Label()
        Label.set_property("xalign", 1.0)
        tabSync.append(Label)
        vbox2c.pack_start(tabSync[i], True, True, 0)
    hbox.add(vbox2c)

    vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    for i in range(nbItems):
        if indEdit:
            tabButton.append(Gtk.ToggleButton())
            tabButton[i].connect("toggled", toggled)
        else:
            tabButton.append(Gtk.Label())
        vbox2.pack_start(tabButton[i], True, True, 0)
    hbox.add(vbox2)

    vbox2b = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    for i in range(nbItems):
        Label = Gtk.Label(" ")
        Label.set_property("xalign", 0.0)
        tabCountries.append(Label)
        vbox2b.pack_start(tabCountries[i], True, True, 0)
    hbox.add(vbox2b)
    mainbox.add(hbox)

    hbox2 = Gtk.Box(True, spacing=50)
    if not indShortList:
        buttonPrev = Gtk.Button(" ")
        buttonPrev.connect("clicked", prevPage)
        hbox2.add(buttonPrev)
    if indEdit:
        buttonShow = Gtk.Button(_("Show custom list"))
        buttonShow.connect("clicked", showList)
        hbox2.add(buttonShow)
    else:
        buttonBack = Gtk.Button(_("Back to main list"))
        buttonBack.connect("clicked", backMain)
        hbox2.add(buttonBack)
        buttonDone = Gtk.Button(_("Done"))
        buttonDone.connect("clicked", backDone)
        hbox2.add(buttonDone)

    if not indShortList:
        buttonNext = Gtk.Button(" ")
        buttonNext.connect("clicked", nextPage)
        hbox2.add(buttonNext)
    displayPage()
    mainbox.add(hbox2)

    win.connect("delete-event", deleteEvent)
    win.set_position(Gtk.WindowPosition.CENTER)
    win.show_all()
    Gtk.main()
    win.destroy()
    return indDone

if __name__ == "__main__":

    indDone = False
    while not indDone:
        chooseMirrors(True, serverList)
        customList = []
        for elem in serverList:
            if elem['selected']:
                customList.append(elem)
        chooseMirrors(False, customList)

    path = "/tmp/Custom"
    try:
        fcust = open(path, "w")
    except:
        print("\nError : can't create file {0}.\n".format(path))
        exit(1)
    fcust.write("##\n")
    fcust.write("## Pacman Mirrorlist\n")
    fcust.write("##\n\n")
    for elem in customList:
        fcust.write(elem['url'] + "\n")
    fcust.close()
