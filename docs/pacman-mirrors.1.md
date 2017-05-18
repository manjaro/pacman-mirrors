# NAME
pacman-mirrors - generate pacman mirrorlist for Manjaro Linux

# SYNOPSIS
pacman-mirrors [OPTION] ...

# DESCRIPTION
Generate mirrorlist for Manjaro Linux. Default is to rank all mirrors by reponse time. Mandatory arguments to long options are mandatory for short options too.

# OPTIONS
## METHODS

_-f, --fasttrack NUMBER_
    
generates a mirrorlist with a number mirrors ranked by responsiveness, the mirrors are selected from <http://repo.manjaro.org/status.json>

_-g, --generate_

generate a new default mirrorlist using defaults

_-m, --method METHOD_

default is **rank** but **random** can be selected 

_-i, --interactive [--default]_

launches a tool for selectively picking mirrors and protocols, _--default_ forces pacman-mirrors to load the default mirror file and ignore any preset custom-mirrors file, thus allowing for reselecting mirrors for a new custom mirror file

## MISC

_-b, --branch BRANCH_

temporarily use another branch, use **stable**, **testing** or **unstable**, the branch is reset with next run of pacman-mirrors

_-c, --country COUNTRY [COUNTRY ...]_, cannot be used with _--geoip_

specifiy a country or a list of countries  for example **-c Germany** will produce a mirrorlist including only German mirrors

_--geoip_, cannot be used with _-c/--country_
    
use geolocation if possible else use all

_-l, --country-list_

lists available mirror countries

_-d, --mirror_dir NEW_DIR_ **(DEPRECATED)**
    
choose a temporary directory where mirrors file is located

_-o, --output NEW_FILE_ **(DEPRECATED)**

choose a temporary file for your mirrorlist

_-q, --quiet_

make pacman-mirrors silent

_-t, --timeout SECONDS_

change the number of seconds waiting for a server response, SSL enabled mirrors has this value doubled to compensate, for the time spent on exchanging encryption keys

## SYNC and MIRRORLIST
_-n, --no-mirrorlist_, cannot be used with _-y/--sync_

skip mirrorlist generation

_-y, --sync_, cannot be used with _-n/--no-mirrorlist_

instruct pacman-mirrors to syncronize the pacman database

## API

_-a, --api_

instructs pacman-mirrors to activate the following arguments

-a [_-p, --prefix PREFIX_]

add a path prefix to pacman-mirrors file-handling eg. /mnt/install or $mnt

-a [_-G, --get-branch_]

returns branch from configuration optionally with a prefix.

-a [_-S, --set-branch BRANCH_]

writes the branch to configuration optionally with a prefix use **stable**, **testing** or **unstable**

-a [_-P, --proto, --protocols PROTO [PROTO ...]_]

write the protocols to configuration optionally with a prefix use **all** or **http**, **https**, **ftp** and **ftps**.

## GENERIC

_-h, --help_

show the help message

_-v, --version_

show the version of pacman-mirrors

## Exit status:  

0 if OK  
1 if problem with argument  
BRANCH from config  

# EXAMPLES

Most optional arguments are self explaining others require explanation.

Which countries has mirrors?

    sudo pacman-mirrors -l

Temporary change branch to unstable, give me geoip (if available) and syncronize pacman

    sudo pacman-mirrors -yb unstable --geoip
    
Permanently change branch to unstable, mirrors in Germany, France and Austria, only use https and syncronize pacman

    sudo pacman-mirrors -yac Germany,France,Austria -S unstable -P https
    
Create a mirrorlist with German mirrors and syncronize pacman

    sudo pacman-mirrors -yc Germany

If you want more countries in your mirrorlist add them

    sudo pacman-mirrors -yc Germany France Austria Denmark

Create a mirrorlist with 5 mirrors with current packages and syncronize pacman
 
    sudo pacman-mirrors -yf 5

The API functions is mainly designed to help packagers and as an installation helper. However it can be of use for the ordinary user because it takes the hazzle out of editing your pacman-mirrors configuration.

* Get your current branch

    sudo pacman-mirrors -a -G

* Change your the branch your system uses and dont change the mirrorlist

    sudo pacman-mirrors -naS unstable

* Change which protocols you will accept and dont change the mirrorlist

    sudo pacman-mirrors -naP https http

* A packager can write the directly to a mounted systems datafiles using either a path or an environment variable

    sudo pacman-mirrors -ap $mnt -S unstable -P https

# AUTHOR

Esclapion <esclapion@manjaro.org>  
philm <philm@manjaro.org>  
Ramon Buldó <rbuldo@gmail.com>  
Hugo Posnic <huluti@manjaro.org>  
Frede Hundewadt <frede@hundewadt.dk>  

# REPORTING BUGS
   <https://github.com/manjaro/pacman-mirrors/issues>
