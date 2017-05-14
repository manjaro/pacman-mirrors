#  Documentation of pacman-mirrors
Enhanced pacman-mirrors for Manjaro Linux

## USAGE
### GENERIC:
#### `-h`, `--help` 
Show the help message.

#### `-v`, `--version`
Show the version of pacman-mirrors.

### COUNTRY:
#### `-c COUNTRY [COUNTRY ...]`, `--country COUNTRY [COUNTRY ...]`
Specifiy country or list of countries separated by comma or space:

- --country France
- --country France, Germany, Austria

To remove a custom mirror file

- --country all

#### `--geoip` 
Find current country by using geolocation.

### METHODS:
#### `-g`, `--generate`
Generate a new default mirrorlist.

#### `-f {DIGIT}`, `--fasttrack {DIGIT}`
Generates a mirrorlist of **DIGIT** mirrors ranked by responsiveness.
The mirrors are randomly selected from a selection of mirrors known to be up-to-date on all branches.

#### `-m {method}`, `--method {method}`
Choose the generation method:  
Select ***rank*** or ***random***

#### `-i`, `--interactive`
Launch a tool for selectively picking mirrors and protocols for a custom mirrorlist.

### MISC:
#### `-b {branch}`, `--branch {branch}`
Choose a temporary branch:  
Select ***stable***, ***testing*** or ***unstable***.
The branch is reset on next run of pacman-mirrors.

#### `-d {new_dir}`, `--mirror_dir {new_dir}`
Choose a temporary directory where mirrors file is located.

#### `-l`, `--list`
Lists available mirror countries

#### `-o {new_file}`, `--output {new_file}`
Choose a temporary file for your mirrorlist.

#### `-q`, `--quiet`
Make pacman-mirrors silent.

#### `-t {DIGIT}`, `--timeout {DIGIT}`
Change the server maximum waiting time. 
This setting is doubled when talking to SSL enabled mirrors.

#### `--default`
The argument only have effect in conjunction with `-i/--interactive`. 
This forces pacman-mirrors to load the default mirror file 
and ignore any present custom-mirrors file, thus allowing for reselecting 
mirrors for a new custom mirror file. The argument executes the 
ranking/randomizing when the selection of mirrors is done.

#### `--no-update`
Don't generate mirrorlist.

### SYNC:
#### `-y`, `--sync`,`-u`, `update`
Instruct pacman-mirrors to syncronise the pacman databases after mirrorlist generation. 
This is done by calling `pacman -Syy`.

### API:
Permanently make changes to pacman-mirrors configuration through an api. 
The tasks is done before generating the mirrorlist. 
The mirrorlist is written to `[prefix]/etc/pacman.d/mirrorlist`.
#### `-a`, `--api` [--prefix] [--get-branch | --set-branch {branch}] [--proto PROTO [PROTO ...]] [--no-mirrorlist]

##### `--prefix` 
Change pacman-mirrors file-handling eg. `/mnt/install` or `$mnt`.

##### `--get-branch` 
Returns branch from to `/etc/pacman-mirrors.conf`.   

##### `--set-branch {branch}` 
Writes the branch to `/etc/pacman-mirrors.conf`.  
Select ***stable***, ***testing*** or ***unstable***.

##### `--proto PROTO [PROTO ...]` 
Write the specified protocols to `/etc/pacman-mirrors.conf`.  
Select ***all*** or ***http***, ***https***, ***ftp*** and ***ftps***

##### `-n`, `--no-mirrorlist` 
Exit when api task is done 

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
## ATM available protocols are: http, https, ftp, ftps
## Not specifying a protocol will ban the protocol from being used
## Empty means all in reversed alphabetic order
## If a mirror has more than one protocol defined 
##  only the first is written to the mirrorlist
# Protocols = 

## Specify to use only mirrors from a specific country.
## Can add multiple countries
##   separated by comma 'Germany,France,Belgium'
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
