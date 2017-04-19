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
- random.

`-b [branch]`, `--branch [branch]`
Choose the branch to use:

- stable
- testing
- unstable

`-c [country]`, `--country [country]`
Choose the country to use:

- all
- France
- France, German, Spain

`--geoip`
Detect country by using geolocation.

`-d`, `--mirror_dir`
Change directory of mirrors to use.

`-f [n]`, `--fasttrack [n]`
Generates an updated and responsive mirrorlist of [n] mirrors.

`-l`, `--list`
Lists available mirror countries

`-o`, `--output`
Change path of the output file.

`-t`, `--timeout`
Change the server maximum waiting time.

`--no-update`
Don't generate mirrorlist.

`-i`, `--interactive`
Launch a graphical tool to select mirrors to generate a custom mirrorlist.

`--default`
Used in conjunction with `-i/--interactive` ignores custom mirrorfile,  
loading the default mirrorfile and executes the ranking/randomizing process  
after the selection of mirrors.

`-v`, `--version`
Show the version of pacman-mirrors.

`--quiet`
Make pacman-mirrors silent.

`-a`, `--api` [--prefix] [{--get-branch | --set-branch}]

- `--prefix` for pacman-mirrors file-handling eg. /mnt/install or $mnt
- `--get-branch` returns branch from config in prefix`config_file`. If used with `--branch` and you get the arguments value.
- `--set-branch` writes branch from `--branch` to prefix`config_file`

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

## Define protocols and priority eg. 'https,http' or 'http,https'
## ATM available protocols are: http, https, ftp
## Not specifying a protocol will ban the protocol from being used
## If a mirror has more than one protocol defined only the first is written to the mirrorlist
## Empty means all in reversed alphabetic order
# Protocols =

## Specify to use only mirrors from a specific country.
## Can add multiple countries separated by a comma (example: Germany,France,Belgium)
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
