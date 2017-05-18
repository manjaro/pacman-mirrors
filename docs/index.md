# NAME
pacman-mirrors - generate pacman mirrorlist for Manjaro Linux

# SYNOPSIS
pacman-mirrors [OPTION] ...

# DESCRIPTION
Generate mirrorlist for Manjaro Linux. Default is to rank all mirrors by reponse time. Mandatory arguments to long options are mandatory for short options too.

# OPTIONS
## METHODS

_-f_,_--fasttrack NUMBER_
    
generates a mirrorlist with a number mirrors ranked by responsiveness, the mirrors are selected from <http://repo.manjaro.org/status.json>

_-g_,_--generate_

generate a new default mirrorlist using defaults

_-m_,_--method METHOD_

default is **rank** but **random** can be selected 

_-i_,_--interactive [--default]_

launches a tool for selectively picking mirrors and protocols, _--default_ forces pacman-mirrors to load the default mirror file and ignore any preset custom-mirrors file, thus allowing for reselecting mirrors for a new custom mirror file

## MISC

_-b_,_--branch BRANCH_

temporarily use another branch, use **stable**, **testing** or **unstable**, the branch is reset with next run of pacman-mirrors

_-c_,_--country COUNTRY [COUNTRY ...]_, cannot be used with _--geoip_

specifiy a country or a list of countries  for example **-c Germany** will produce a mirrorlist including only German mirrors

_--geoip_, cannot be used with _-c_,_--country_
    
use geolocation if possible else use all

_-l_,_--country-list_

lists available mirror countries

_-d_,_--mirror_dir NEW_DIR_ **(DEPRECATED)**
    
choose a temporary directory where mirrors file is located

_-o,_--output NEW_FILE_ **(DEPRECATED)**

choose a temporary file for your mirrorlist

_-q_,_--quiet_

make pacman-mirrors silent

_-t_,_--timeout SECONDS_

change the number of seconds waiting for a server response, SSL enabled mirrors has this value doubled to compensate, for the time spent on exchanging encryption keys

## SYNC and MIRRORLIST
_-n_,_--no-mirrorlist_, cannot be used with _-y_,_--sync_

skip mirrorlist generation

_-y_,_--sync_, cannot be used with _-n_,_--no-mirrorlist_

instruct pacman-mirrors to syncronize the pacman database

## API

_-a_,_--api_

instructs pacman-mirrors to activate these optional arguments

_-a_ [_-p, --prefix PREFIX_]

add a path prefix to pacman-mirrors file-handling eg. /mnt/install or $mnt

_-a_ [_-G, --get-branch_]

returns branch from configuration optionally with a prefix.

_-a_ [_-S, --set-branch BRANCH_]

writes the branch to configuration optionally with a prefix use **stable**, **testing** or **unstable**

_-a_ [_-P, --proto, --protocols PROTO [PROTO ...]_]

write the protocols to configuration optionally with a prefix use **all** or **http**, **https**, **ftp** and **ftps**.

## GENERIC

_-h_,_--help_

show the help message

_-v_,_--version_

show the version of pacman-mirrors

## Exit status:  

0 if OK  
1 if problem with argument  
BRANCH from config  

# EXAMPLES

Most optional arguments are self explaining others require explanation. The API functions is mainly designed to help packagers and iso-builders. However it can be of use for everyone because it takes the hazzle out of editing your pacman-mirrors configuration.

Which countries has mirrors?

_sudo pacman-mirrors -l_

Temporary change branch to unstable, use geolocation and syncronize pacman

_sudo pacman-mirrors -yb unstable --geoip_
    
Permanently change branch to unstable, mirrors in Germany and France, use https and syncronize pacman

_sudo pacman-mirrors -yac Germany,France -S unstable -P https_
    
Create a mirrorlist with German mirrors and syncronize pacman

_sudo pacman-mirrors -yc Germany_

If you want more countries in your mirrorlist add them

_sudo pacman-mirrors -yc Germany France Denmark_

Create a mirrorlist with 5 mirrors with current packages and syncronize pacman
 
_sudo pacman-mirrors -yf 5_

I want to choose my mirrors

_sudo pacman-mirrors -i_

I have a custom mirror list and I want to create a new custom mirror list?

_sudo pacman-mirrors -i --default_

I have a custom mirror list - can I reset it?
 
_sudo pacman-mirrors -c all_

What branch am I on

_sudo pacman-mirrors -a -G_

Change system branch and dont change the mirrorlist

_sudo pacman-mirrors -naS unstable_

Change protocols you will accept but dont touch the mirrorlist

_sudo pacman-mirrors -naP https http_

A packager can write the directly to a mounted systems datafiles using either a path or an environment variable

_sudo pacman-mirrors -ap $mnt -S unstable -P https_

# AUTHOR

Esclapion <esclapion@manjaro.org>  
philm <philm@manjaro.org>  
Ramon Buldó <rbuldo@gmail.com>  
Hugo Posnic <huluti@manjaro.org>  
Frede Hundewadt <frede@hundewadt.dk>  

# REPORTING BUGS
   <https://github.com/manjaro/pacman-mirrors/issues>
