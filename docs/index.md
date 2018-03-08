% pacman-mirrors(8) Pacman-Mirrors 4.7.x User Manual
%
% March, 2018

# NAME

pacman-mirrors - generate pacman mirrorlist for Manjaro Linux

# SYNOPSIS
pacman-mirrors [-f[*NUMBER*] [[-i[-d]] [-c*COUNTRY*[[,*COUNTRY*]...]|--geoip]]] 
[-a[-p*PREFIX*][-R][-G|-B/-S*BRANCH*][-P*PROTO*[[,*PROTO*]...]][-U*URL*]] 
[-b*BRANCH*] [-q] [-t*SECONDS*] [-v] [-n]


# DESCRIPTION

Generates mirrorlist with up-to-date mirrors for Manjaro Linux.  
Default is to rank all mirrors by reponse time.  
If no arguments are given pacman-mirrors lists available options.  
Pacman-mirrors requires access to files which are read-only so it must be run with *su* or *sudo.*  
To create a mirrorlist using all default use

    pacman-mirrors -f

The mirrorlist generation process can be refined through arguments and arguments with options, for example

    pacman-mirrors --country Denmark --timeout 5

# IMPORTANT
After all operations *ALWAYS* syncronize and update your system with

    sudo pacman -Syyu

# OPERATION
No matter how you choose to generate your mirrorlist, you will **ONLY** get up-to-date mirrors. 
This means the - at any given time - number available mirrors will vary depending on when the mirror last syncronized with the master repo server.  

## MODES

1. The number of mirrors
   * pacman-mirrors -f [number]
2. More control (custom mirror pool)
   * -c COUNTRY[[,COUNTRY]...]
3. Full control (custom mirror pool)
   * -i [-d/--default]

## FILES OVERVIEW

* **The configuration**: *`/etc/pacman-mirrors.conf`*
   * The file holds configuration for pacman-mirrors.
* **The mirrorlist**: *`/etc/pacman.d/mirrorlist`*
   * The file contains a number of servers which `pacman` uses to update your system.
* **Manjaro mirror pool**: *`/usr/share/pacman-mirrors/mirrors.json`*
   * The worldwide mirrorpool comes with installation. It is compared against the file located at Github in manjaro-web-repo. If the repofile has changed, your local file will be updated with said file.
* **Manjaro mirror pool status**: *`/var/lib/pacman-mirrors/status.json`*
   * The mirrorpool status file. It is the data you see displayed at repo.manjaro.org. The file is downloaded on every run of pacman-mirrors and saved in.
* **Custom mirror pool**: *`/var/lib/pacman-mirrors/custom-mirrors.json`* 
   * The file is your custom mirror pool and is created by **`-i/--interactive [-d/--default]`** argument or the **`-c/--country`** argument.

If you are stunned by this message 

    .: WARNING No mirrors in selection
    .: INFO The mirrors has not changed

This is not an error, it is a feature.  
The reason: You have limited your mirror pool too much and none of your selected mirrors are up-to-date.

**Suggested solutions**:

* Remove limitations like **`--geoip`**
* Expand with more countries.
* Do a complete reset of your list with *`pacman-mirrors -c all -aP all`** and then **`pacman-mirrors -f`**

## GENERAL INFO ABOUT ARGUMENTS
Some options are mutual exclusive and will throw an arguments error:

* **--branch**, **--get-branch** and **--set-branch**
* **--country**, **--fasttrack**, **--geoip**

Some arguments requires another argument present to have effect. E.g., this command will ignore *--default* argument

   WRONG
   
    pacman-mirrors -b unstable --default

The *-d/--default* argument tells *-i/--interactive* to force load all mirrors from the mirrorfile

   CORRECT
   
    pacman-mirrors -b unstable --interactive --default

   Or
   
    pacman-mirrors -bunstable -id

API specific arguments. For those to have effect the *-a/--api* argument must be present.

    pacman-mirrors -aS unstable

The arguments can appear in any order except for arguments which takes additional options in which case the options must follow immediately after the argument with or without space, for example
    
    pacman-mirrors -f
    pacman-mirrors -f 5
    pacman-mirrors -f5

Pacman-mirrors always attempt to download the lastest available data from [http://repo.manjaro.org](http://repo.manjaro.org). These data is always used during mirrorlist generation to ensure that you connect to a mirror which is up-to-date for your selected branch. Should you decide to temporarily switch branches you will still connect to an up-to-date mirror.

# ARGUMENTS, METHODS AND OPTIONS

## METHODS
-c, \--country *COUNTRY* [[*COUNTRY*]...]
:   Creates a custom mirror pool with supplied countries.

-f, \--fasttrack [*NUMBER*]
:   Generates a random mirrorlist for the users current selected branch, mirrors are randomly selected from the users current mirror pool, either a custom pool or the default pool, the randomly selected mirrors are ranked by their current access time. The higher number the higher possibility of a fast mirror. If a number is given the resulting mirrorlist contains that number of servers.

-i, \--interactive [--default]
:   This is a function designed to leave full control over countries, mirrors and protocols to the user. This function **DOES NOT** take into consideration up-to-date mirrors. The optional **--default** forces pacman-mirrors to load the default mirror file and ignore any preset custom pool, thus allowing for reselecting mirrors for a new custom pool.

## BRANCH

-b, \--branch *BRANCH*
:   Temporarily use another branch, *stable*, *testing* or *unstable*. The branch is reset with next run of pacman-mirrors.

## API

-a, \--api [-p *PREFIX*] [-R] [-G|-S/-B *BRANCH*] [-P *PROTO* [*PROTO*] ...] [-U *URL*]
:   Instructs pacman-mirrors to activate processing of API arguments

-B, -S, \--set-branch *BRANCH*
:   Permanent change to branch config, using *stable*, *testing* or *unstable*

-G, \--get-branch
:   Return branch from configuration.

-p, \--prefix *PREFIX*
:   Add a path prefix to pacman-mirrors file-handling eg. */mnt/install* or *$mnt*

-P, \--proto, \--protocols *PROTO* [*PROTO*] ...
:   Write protocols to configuration, using *all* or *http*, *https*, *ftp* and *ftps*

-R, \--re-branch
:   Replace branch in mirrorlist

-U, \--url *URL*
:   Replace mirrorlist with supplied url

## MISC

\--geoip
:   Use geolocation if possible, if geoip is not available all mirrors.

-h, \--help
:   Show the help message

-l, \--list, \--country-list
:   Lists available mirror countries.

-m, \--method *METHOD*
:   Default method is *rank* but *random* can be selected.

-n, \--no-mirrorlist
:   Use to skip generation of mirrorlist

-q, \--quiet
:   Make pacman-mirrors silent

-t, \--timeout *SECONDS*
:   Change the number of seconds waiting for a server response, SSL enabled mirrors has this value doubled to compensate for the time spent on exchanging encryption keys

-v, \--version
:   Show the version of pacman-mirrors

## Exit status:

    0     : OK
    1     : Problem with argument
    2     : Problem accessing systemfiles
    3     : Missing mirror file
    BRANCH: Value from config

## Configuration flow of pacman-mirrors

At launch an internal default configuration is setup, file configuration is applied and the commandline is parsed and applied.

## API arguments

These arguments modifies key elements of pacman-mirrors configuration according to the packagers needs.

The actions performed by the API are in strict order and performed *before any* other actions. This also means that ordinary arguments supplied in conjunction with api might be ignored. Eg. **-U** argument terminates pacman-mirrors when branch and mirrorlist has been written.

1. If *-G*
   * print *config.branch*
   * *sys.exit(0)*
2. If *p*  *PREFIX*
   *  add *PREFIX* to internal file configuration
3. If *-S/-B* *BRANCH*
   * apply *BRANCH* to internal configuration
   * replace branch in pacman-mirrors.conf with *BRANCH*
4. If *-U* *URL*
   * apply internal configuration to a mirrorlist with *URL*
   * *sys.exit(0)*
5. If *-P* *PROTO* [*PROTO*] ...
   * replace protocols in pacman-mirrors.conf with *PROTO*
6. If *-R*
   * replace branch in mirrorlist with *-S/-B* *BRANCH*

When done pacman-mirrors checks the internet connection and if possible download the latest datafiles for creating the mirrorlist. At this point it is possible to interrupt further processing.

If the *-n/--no-mirrorlist* argument is present pacman-mirrors will now exit.

# EXAMPLES

Most optional arguments are self explaining others require explanation. The API functions is mainly designed to help packagers and iso-builders. However it can be of use for everyone because it takes the hazzle out of editing your pacman-mirrors configuration.

## Commands
 
* Which countries has mirrors?

    *pacman-mirrors --list*

* What branch am I on

    *pacman-mirrors --api --get-branch*

## Commands requiring sudo

* I want to temporary change branch to unstable, use geolocation,

    *sudo pacman-mirrors --branch unstable --geoip*

* I want to permanently change branch to unstable, use mirrors from Germany and France, use only https and http protocol in that order

    *sudo pacman-mirrors --country Germany,France --api --set-branch unstable --procotol https http*

* Create a mirrorlist with German mirrors and a custom mirror file

    *sudo pacman-mirrors --country Germany*

* If you want more countries in your mirrorlist add them they will be written to your custom mirror pool

    *sudo pacman-mirrors --country Germany France Denmark*

* Create a mirrorlist with 5 mirrors up-to-date on your branch

    *sudo pacman-mirrors --fastrack 5*

* I want to choose my mirrors

    *sudo pacman-mirrors --interactive*

* I have a custom mirror list and I want to create a new custom mirror list?

    *sudo pacman-mirrors --interactive --default*

* I have a custom mirror list - can I reset it?

    *sudo pacman-mirrors --country all*

* Change system branch and dont change the mirrorlist

    *sudo pacman-mirrors -naS unstable*

* Change system branch and replace branch in mirrorlist and quit

    *sudo pacman-mirrors -naRS unstable*

* Change protocols you will accept but dont touch the mirrorlist

    *sudo pacman-mirrors -naP https http*

* A packager can write directly to a mounted systems datafiles using either a path or an environment variable replacing the branch in both configuration and mirrorlist leaving the mirrors as is

    *sudo pacman-mirrors -anR -p $prefix -S $branch -P https*

* It is also possible to specify a mirror in which case the mirrorlist is created and pacman-mirrors terminate

    *sudo pacman-mirrors -ap $prefix -S $branch -U $url*

# MORE INFO
* [https://wiki.manjaro.org/index.php?title=Pacman-mirrors](https://wiki.manjaro.org/index.php?title=Pacman-mirrors)
* [https://wiki.manjaro.org/index.php?title=Create_your_own_Custom_Mirrorlist](https://wiki.manjaro.org/index.php?title=Create_your_own_Custom_Mirrorlist)

# REPORTING BUGS
   [https://github.com/manjaro/pacman-mirrors/issues](https://github.com/manjaro/pacman-mirrors/issues)

# SEE ALSO

The pacman-mirrors source code and all documentation may be downloaded from [https://github.com/manjaro/pacman-mirrors/archive/master.zip](https://github.com/manjaro/pacman-mirrors/archive/master.zip)

# AUTHORS

    Esclapion <esclapion@manjaro.org>
    philm <philm@manjaro.org>
    Ramon Buldó <rbuldo@gmail.com>
    Hugo Posnic <huluti@manjaro.org>
    Frede Hundewadt <echo ZmhAbWFuamFyby5vcmcK | base64 -d>
