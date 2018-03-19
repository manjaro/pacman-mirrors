# pacman-mirrors

[![Build Status](https://travis-ci.org/manjaro/pacman-mirrors.svg?branch=master)](https://travis-ci.org/manjaro/pacman-mirrors)

Package that provides all mirrors for Manjaro Linux.

- Free software: GPL license

## Features

- A GUI for selecting mirror/protocol combinations used to generate a custom list.
- Generate a new mirror list by using several options:
    - method      : rank or random.
    - country     : a single, a list or all.
    - fasttrack   : updated and responsive mirrors.
    - geoip       : mirrors for country if available.
- Information
    - get-branch  : get current branch from config
    - country-list: list of countries with mirrors
- API
    - prefix      : prefix for files handled by pacman-mirrors.
    - set-branch  : set branch from supplied branch option to config
    - protocols:
        - set protocol limitation in config
        - remove protocol limitation from config

## Technologies

pacman-mirrors is build with Python and Gtk3.
