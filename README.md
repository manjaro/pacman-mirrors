# pacman-mirrors

[![Build Status](https://travis-ci.org/manjaro/pacman-mirrors.svg?branch=master)](https://travis-ci.org/manjaro/pacman-mirrors)

Package that provides all mirrors for Manjaro Linux.

- Free software: GPL license

## Features

- Generate a new mirror list by using several options:
    - method: rank or random.
    - branch: stable, testing or unstable.
    - country: a single, a list or all.
    - fasttrack: updated and responsive mirrors
    - geoip: mirrors for country if available
- A GUI for selecting the mirrors to used to generate a custom list.

## How does fasttrack work
### Question:
So, `pacman-mirrors -f 2` takes the same time to create `/etc/pacman.d/mirrorlist` as `pacman-mirrors -f 20`?

#### Answer:
No. `pacman-mirors -f 2` will be faster than `pacman-mirrors -f 20` since only 2 mirrors are probed vs 20 mirrors but since most mirrors respond within the first second I think it is barely noticeable.

### Question:
`pacman-mirrors -f` always ranks ALL mirrors by response time (the same as `pacman-mirrors -g` does) and additionally takes up-to-date mirrors and writes only **n** mirrors to `/etc/pacman.d/mirrorlist`?

#### Answer: 
No. `pacman-mirrors -f N` always ranks by response time but before the actual ranking, the mirrors are sorted so it will be the first **n** mirrors which are uptodate which are actually probed, not mirrors which is not uptodate

### Beware
The smaller number you choose to write to the mirrorlist will increase the possibility of not getting a responsive mirror since only the first **n** in the list are tested not all of them.

A reasonable number is between 5 and 10.

There is a little overhead because it always checks if network is online. Doing so by pinging google with 3 packets.

The force of this approach is that we know forehand if the mirror is uptodate and thus only have to rank **n** mirrors from the mirrors known to be uptodate.

If you need a complete ranking then `pacman-mirrors -g` is the way to go.

## Technologies

pacman-mirrors is build with Python and Gtk3.
