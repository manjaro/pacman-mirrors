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

### How does fasttrack work
First of all, a working internet connection is mandatory. Pacman-Mirrors always checks if network is online. It is doing so by pinging google with 3 packets.
#### Question:
So, `pacman-mirrors -f 2` takes the same time to create `/etc/pacman.d/mirrorlist` as `pacman-mirrors -f 20`?
##### Answer:
No. `pacman-mirors -f 2` will be faster than `pacman-mirrors -f 20` since only 2 mirrors are probed vs 20 mirrors but since most mirrors respond within the first second I think it is barely noticeable.
#### Question:
`pacman-mirrors -f n` always ranks ALL mirrors by response time (the same as `pacman-mirrors -g` does) and additionally takes up-to-date mirrors and writes only **n** mirrors to `/etc/pacman.d/mirrorlist`?
##### Answer: 
No. `pacman-mirrors -f n` ranks on a sorted list with known up-to-date mirrors. Thus it is only the first **n** mirrors from this list which are actually probed. If you have a list of 30 mirrors which are uptodate and use `-f 5` only the top 5 mirrors are probed and then sorted after response time.
The switch does not guarantee you get **the n** fastest mirrors only that they are responsive and uptodate. Mirrors which have network errors or times out are not considered at all.
#### Beware
The smaller number you choose to write to the mirrorlist will increase the possibility of not getting a responsive mirror since only the first **n** in the list are tested not all of them.

A reasonable number is between 5 and 10.

The force of this approach is that we know forehand if the mirror is uptodate and thus only have to rank **n** mirrors from the mirrors known to be uptodate.

If you need a complete ranking then `pacman-mirrors -g` is the way to go.

## Technologies

pacman-mirrors is build with Python and Gtk3.
