# pacman-mirrors

[![Build Status](https://travis-ci.org/manjaro/pacman-mirrors.svg?branch=master)](https://travis-ci.org/manjaro/pacman-mirrors)

Package that provides all mirrors for Manjaro Linux.

- Free software: GPL license

## Features

- Generate a new mirror list by using several options:
    - method: rank or random.
    - branch: stable, testing or unstable.
    - country: a single, a list or all.
    - fasttrack: updated and responsive mirrors.
    - geoip: mirrors for country if available.
- A GUI for selecting mirror/protocol combinations used to generate a custom list.
- API
    - prefix: prefix for files handled by pacman-mirrors.
    - get-branch: get current branch from config
    - set-branch: set branch from supplied branch option to config
    - protocols: 
        - set protocol limitation in config
        - remove protocol limitation from config    

## Technologies

pacman-mirrors is build with Python and Gtk3.
