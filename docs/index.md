#  Documentation of pacman-mirrors

Enhanced pacman-mirrors for Manjaro Linux

## Commands

`-h`, `--help`
Show the help message.

`-g`, `--generate`
Generate a new mirrorlist.

`-m [method]`, `--method [method]`
Choose the generation method:

- rank
- random

`-b [branch]`, `--branch [branch]`
Choose the branch to use:

- stable
- testing
- unstable

`-c COUNTRY [COUNTRY ...]`, `--country COUNTRY [COUNTRY ...]`
Specifiy country or list of countries separated by comma or space:

- France
- France, Germany, Austria
- France Germany Austria

To reset a custom mirror file

- all

`--geoip`
Detect country by using geolocation.

`-d`, `--mirror_dir`
Change directory of mirrors to use.

`-f [n]`, `--fasttrack [n]`
Generates an updated and responsive mirrorlist of [n] mirrors.

`-l`, `--country-list`
Lists available mirror countries

`-o`, `--output`
Change path of the output file.

`-t`, `--timeout`
Change the server maximum waiting time.

`--no-update` DEPRECATED  
Will be removed  
Don't generate mirrorlist.

`-n`, `--no-mirrorlist`
Download new mirror files and exit.

`-i`, `--interactive`
Launch a graphical tool to select mirrors to generate a custom mirrorlist.

`--default`
Used in conjunction with `-i/--interactive` ignores custom mirrorfile,  
loading the default mirrorfile, allowing to create a new custom mirrorfile 
and executes the ranking/randomizing process after the selection of mirrors.

`-v`, `--version`
Show the version of pacman-mirrors.

`--quiet`
Make pacman-mirrors silent.

`-u`, `update` DEPRECATED  
will change to `-y`, `--sync`  
Run `pacman -Syy` after mirrorlist generation

`-a`, `--api` [--prefix] [{--get-branch | --set-branch}] [--protocols PROTO [PROTO ...]] 
- `--prefix` for pacman-mirrors file-handling eg. /mnt/install or $mnt.
- `--get-branch` returns branch from config in prefix`config_file`. 
  * Ignored if `--branch` is supplied.
- `--set-branch` writes branch specified in `--branch` to prefix`config_file`.
  * Ignored if `--branch` is not supplied.
- `--protocols` write the specified protocols to prefix`pacman-mirrors.conf`.

## Content of pacman-mirrors.conf

```
##
## /etc/pacman-mirrors.conf
##

## Branch Pacman should use (stable, testing, unstable)
# Branch = stable

## Generation method
## 1) rank   - rank mirrors depending on their access time
## 2) random - randomly generate the output mirrorlist
# Method = rank

## Define protocols and priority
##   separated by comma 'https,http' or 'http,https'
##             or space 'https http' or 'http https'
## ATM available protocols are: http, https, ftp
## Not specifying a protocol will ban the protocol from being used
## Empty means all in reversed alphabetic order
## If a mirror has more than one protocol defined 
##  only the first is written to the mirrorlist
# Protocols =

## Specify to use only mirrors from a specific country.
## Can add multiple countries
##   separated by comma 'Germany,France,Belgium'
##             or space 'Germany France Belgium'
## Get a list of all available counties with 'pacman-mirrors -l'
## Empty means all
# OnlyCountry =

## Mirrors directory
# MirrorlistsDir = /var/lib/pacman-mirrors

## Output file
# OutputMirrorlist = /etc/pacman.d/mirrorlist

## When set to True prevents the regeneration of the mirrorlist if
## pacman-mirrors is invoked with the --no-update argument.
## Useful if you don't want the mirrorlist regenerated after a
## pacman-mirrors package upgrade.
# NoUpdate = False

## When set to False - all certificates are accepted.
## Use only if you fully trust all ssl-enabled mirrors.
# SSLVerify = True
```
