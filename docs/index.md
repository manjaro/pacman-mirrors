% pacman-mirrors(8) Pacman-Mirrors User Manual  
%   
% May 18, 2017  

# NAME

pacman-mirrors - generate pacman mirrorlist for Manjaro Linux

# SYNOPSIS

pacman-mirrors [OPTION] ...

# DESCRIPTION

Generate mirrorlist for Manjaro Linux.
Default is to rank all mirrors by reponse time.
If no arguments are given pacman-mirrors lists available options.
To create a mirrorlist using all default use,

    sudo pacman-mirrors -g
    
The mirrorlist generation process can be refined through options 
and arguments which takes input, for example,

    sudo pacman-mirrors --country Denmark --timeout 5

# OPTIONS

-g, \--generate
:   Generate a new default mirrorlist using defaults

-f, \--fasttrack NUMBER
:   Generates a mirrorlist with a number mirrors ranked by responsiveness,
    the mirrors are selected from <http://repo.manjaro.org/status.json>

-m, \--method *METHOD*
:   Default method is *rank* but *random* can be selected 

-i, \--interactive [--default]
:   Launches a tool for selectively picking mirrors and protocols,
    **--default** forces pacman-mirrors to load the default mirror
    file and ignore any preset custom-mirrors file, thus allowing for 
    reselecting mirrors for a new custom mirror file

-b, \--branch *BRANCH*
:   Temporarily use another branch, use *stable*, *testing* or *unstable*, 
    the branch is reset with next run of pacman-mirrors

-c, \--country *COUNTRY* [*COUNTRY* ...]
:   Specifiy a country or a list of countries, excludes **\--geoip**

\--geoip
:   Use geolocation if possible, if not uses all mirrors, 
    excludes **-c**, **\--country**

-l, \--country-list
:   Lists available mirror countries

-d, \--mirror_dir *NEW_DIR*
:   *(DEPRECATED)* Choose a temporary directory where mirrors file is located

-o, \--output *NEW_FILE*
:   *(DEPRECATED)* Choose a temporary file for your mirrorlist

-q, \--quiet
:   Make pacman-mirrors silent

-t, \--timeout *SECONDS*
:   Change the number of seconds waiting for a server response, 
    SSL enabled mirrors has this value doubled to compensate, 
    for the time spent on exchanging encryption keys

-n, \--no-mirrorlist
:   Skip mirrorlist generation, excludes **-y**, **\--sync**

-y, \--sync
:   Instruct pacman-mirrors to syncronize the pacman database, 
    excludes **-n**, **\--no-mirrorlist**

## API

-a, \--api
:   Instructs pacman-mirrors to activate these optional arguments

-a -p, \--prefix *PREFIX*
:   Add a path prefix to pacman-mirrors file-handling  
    eg. */mnt/install* or *$mnt*

-a -G, \--get-branch
:   Returns branch from configuration optionally with a prefix.

-a -S, \--set-branch *BRANCH*
:   Writes the branch to configuration optionally with a prefix,     
    use *stable*, *testing* or *unstable*

-a -P, \--proto, \--protocols *PROTO* [*PROTO* ...]
:   Write the protocols to configuration optionally with a prefix,  
    use *all* or *http*, *https*, *ftp* and *ftps*.

## GENERIC

-h, \--help
:    Show the help message

-v, \--version
:   Show the version of pacman-mirrors

## Exit status:  

0 if OK  
1 if problem with argument  
BRANCH from config  

# EXAMPLES

Most optional arguments are self explaining others require explanation. 
The API functions is mainly designed to help packagers and iso-builders. 
However it can be of use for everyone because it takes the hazzle out 
of editing your pacman-mirrors configuration.

Which countries has mirrors?

    sudo pacman-mirrors -l

I want to temporary change branch to unstable, 
use geolocation and syncronize pacman,

    sudo pacman-mirrors -yb unstable --geoip
    
I want to permanently change branch to unstable, 
use mirrors from Germany and France, 
use only https and http protocol in that order and syncronize pacman
   
    sudo pacman-mirrors -yac Germany,France -S unstable -P https http
    
Create a mirrorlist with German mirrors and syncronize pacman

    sudo pacman-mirrors -yc Germany

If you want more countries in your mirrorlist add them

    sudo pacman-mirrors -yc Germany France Denmark

Create a mirrorlist with 5 mirrors with current packages and syncronize pacman
   
    sudo pacman-mirrors -yf 5

I want to choose my mirrors

    sudo pacman-mirrors -i

I have a custom mirror list and I want to create a new custom mirror list?

    sudo pacman-mirrors -i --default

I have a custom mirror list - can I reset it?

    sudo pacman-mirrors -c all

What branch am I on

    sudo pacman-mirrors -a -G*

Change system branch and dont change the mirrorlist

    sudo pacman-mirrors -naS unstable

Change protocols you will accept but dont touch the mirrorlist

    sudo pacman-mirrors -naP https http

A packager can write the directly to a mounted systems 
datafiles using either a path or an environment variable

    sudo pacman-mirrors -ap $mnt -S unstable -P https

# REPORTING BUGS
   <https://github.com/manjaro/pacman-mirrors/issues>
   
# SEE ALSO

The pacman-mirrors source code and all documentation 
may be downloaded from <https://github.com/manjaro/pacman-mirrors/archive/master.zip>

# AUTHORS

Esclapion <esclapion@manjaro.org>  
philm <philm@manjaro.org>  
Ramon Buldó <rbuldo@gmail.com>  
Hugo Posnic <huluti@manjaro.org>  
Frede Hundewadt <frede@hundewadt.dk>  
