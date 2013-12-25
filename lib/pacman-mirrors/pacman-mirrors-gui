#!/usr/bin/env python

# -*- coding: utf-8 -*-
'''Do a custom mirror list'''

# Release : 1.4
# Date    : 10 Octobre 2013
# Author  : Esclapion

#from listmirrors import *


from gi.repository import Gtk

def chooseMirrors(indEdit, travList) :

    global index, nbItems, indPage, indDone
    tabSync      = []
    tabButton    = []
    tabCountries = []
    nbItems = 12
    indDone = False
    index   = 0
    indPage = False
    indShortList = len(travList) <= nbItems
    if indShortList :
        nbItems = len(travList)

    def truncName(name) :
        return name[7:-12]

    def displayPage () :
        global index, nbItems, indPage
        indPage = True
        for i in range(nbItems) :
            if index < len(travList) :
                tabSync[i].set_label(travList[index][2] + " |")
                tabButton[i].set_label(truncName(travList[index][3]))
                if indEdit :
                    tabButton[i].set_relief(Gtk.ReliefStyle.NORMAL)
                    tabButton[i].set_active(travList[index][5])
                tabCountries[i].set_label("| " + travList[index][0])
            else :
                tabSync[i].set_label("")
                tabButton[i].set_label("")
                if indEdit :
                    tabButton[i].set_relief(Gtk.ReliefStyle.NONE)
                    tabButton[i].set_active(False)
                tabCountries[i].set_label("")
            index = index + 1
        if not indShortList :
            if index > nbItems :
                buttonPrev.set_relief(Gtk.ReliefStyle.NORMAL)
                buttonPrev.set_label("Previous page")
            else :
                buttonPrev.set_relief(Gtk.ReliefStyle.NONE)
                buttonPrev.set_label(" ")
            if index < len(travList) :
                buttonNext.set_relief(Gtk.ReliefStyle.NORMAL)
                buttonNext.set_label("Next page")
            else :
                buttonNext.set_relief(Gtk.ReliefStyle.NONE)
                buttonNext.set_label(" ")

        indPage = False

    def nextPage(self) :
        global index
        if index < len(travList) :
            displayPage()

    def prevPage(self) :
        global index
        val = 2 * nbItems
        if index >= val :
            index = index - val
            displayPage()

    def toggled(self) :
        if indPage == False :
            if self.get_active():
                state = True
            else:
                state = False
            name = self.get_label()
            if name != '' :
                for elem in travList :
                    if truncName(elem[3]) == name :
                        elem[5] = self.get_active()
                        break
            else :
                self.set_active(False)

    def showList(self) :
        Gtk.main_quit()

    def deleteEvent(self, Widget) :
        exit(1)

    def backMain(self) :
        Gtk.main_quit()

    def backDone(self) :
        global indDone
        indDone = True
        Gtk.main_quit()

    win = Gtk.Window()
    win.set_resizable(False)
    if indEdit :
        Gtk.Window.__init__(win, title="Mirrors list sorted by response time")
    else :
        Gtk.Window.__init__(win, title="List of selected mirrors")
    win.set_border_width(10)
    mainbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=30)
    win.add(mainbox)

    if indEdit :
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        header = Gtk.Label(label="Select by clicking mirrors to prepare your custom list")
        vbox.add(header)
        mainbox.add(vbox)

    hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

    vbox2c = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    for i in range(nbItems) :
        Label = Gtk.Label()
        Label.set_property("xalign", 1.0)
        tabSync.append(Label)
        vbox2c.pack_start(tabSync[i] , True, True, 0)
    hbox.add(vbox2c)

    vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    for i in range(nbItems) :
        if indEdit :
            tabButton.append(Gtk.ToggleButton())
            tabButton[i].connect("toggled", toggled)
        else :
            tabButton.append(Gtk.Label())
        vbox2.pack_start(tabButton[i] , True, True, 0)
    hbox.add(vbox2)

    vbox2b = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    for i in range(nbItems) :
        Label = Gtk.Label(" ")
        Label.set_property("xalign", 0.0)
        tabCountries.append(Label)
        vbox2b.pack_start(tabCountries[i] , True, True, 0)
    hbox.add(vbox2b)
    mainbox.add(hbox)

    hbox2 = Gtk.Box(True, spacing = 50)
    if not indShortList :
        buttonPrev = Gtk.Button(" ")
        buttonPrev.connect("clicked", prevPage)
        hbox2.add(buttonPrev)
    if indEdit :
        buttonShow = Gtk.Button("Show custom list")
        buttonShow.connect("clicked", showList)
        hbox2.add(buttonShow)
    else :
        buttonBack = Gtk.Button("Back to main list")
        buttonBack.connect("clicked", backMain)
        hbox2.add(buttonBack)
        buttonDone = Gtk.Button("Done")
        buttonDone.connect("clicked", backDone)
        hbox2.add(buttonDone)

    if not indShortList :
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

    
if __name__=="__main__" :

    indDone = False
    while not indDone :
        chooseMirrors(True, serverList)
        customList = []
        for elem in serverList :
            if elem[5] :
                customList.append(elem)
        chooseMirrors(False, customList)

    path = "/tmp/Custom"
    try :
        fcust = open(path, "w")
    except :
        print("\nError : can't create file {0}.\n".format(path))
        exit(1)
    fcust.write("##\n")
    fcust.write("## Pacman Mirrorlist\n")
    fcust.write("##\n\n")
    for elem in customList :
        fcust.write(elem[3] + "\n")
    fcust.close()
