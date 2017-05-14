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
* --country France
* --country France Germany Austria
To remove a custom mirror file
* --country all
#### `--geoip` 
Find current country by using geolocation.
### METHODS:
All methods can be combined with `-y/--sync` to fully complete the process.
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
Change the server maximum waiting time. In case of SSL enabled mirrors the value is doubled to compensate for the time spent on exchanging encryption keys.
#### `--default`
This argument **only** have effect in conjunction with `-i/--interactive`. It forces pacman-mirrors to load the default mirror file and ignore any preset custom-mirrors file, thus allowing for reselecting mirrors for a new custom mirror file. The argument executes the ranking/randomizing when the selection of mirrors is done. Can be combined with `-y/--sync` to fully complete the process.
#### `--no-update`
This argument is tied to the `NoUpdate = True` setting in the config file. Pacman-mirrors will exit after parsing `pacman-mirrors.conf` and is only useful if you don't want the mirrorlist regenerated after a pacman-mirrors package upgrade.
### SYNC:
#### `-y`, `--sync`,`-u`, `update`
Instruct pacman-mirrors to syncronise the pacman databases after mirrorlist generation. This is done by calling `pacman -Syy`.
### API:
Make permanent changes to pacman-mirrors configuration through an api. The tasks are executed before generating the mirrorlist.
#### `-a`, `--api` [--prefix] [--get-branch | --set-branch {branch}] [--proto PROTO [PROTO ...]] [--no-mirrorlist]
The key to the following arguments is **`-a`** or **`--api`**. If it is missing none of the arguments will have any effect.
##### `--prefix` 
* Add a path prefix to pacman-mirrors file-handling eg. `/mnt/install` or `$mnt`.
##### `--get-branch` 
* Returns branch from `/etc/pacman-mirrors.conf` optionally with a prefix.
##### `--set-branch {branch}` 
* Writes the branch to `/etc/pacman-mirrors.conf` optionally with a prefix.
* Select ***stable***, ***testing*** or ***unstable***.
##### `--proto PROTO [PROTO ...]`
* Write the specified protocols to `/etc/pacman-mirrors.conf` optionally with a prefix.
* Select ***all*** or ***http***, ***https***, ***ftp*** and ***ftps***.
##### `-n`, `--no-mirrorlist` 
* Skip mirrorlist and exit when tasks has been done.
## pacman-mirrors.conf
### Manjaro branch to use for your system
#### ```# Branch = stable```  
* The setting defaults to ***stable*** branch.  
* Select ***stable***, ***testing*** or ***unstable***.
* The setting can be changed by invoking `pacman-mirrors --api --set-branch <branch>`.
### Generation method
#### ```# Method = rank```
Invoking `pacman-mirrors --method <method>` will temporariy change the setting.
* The setting defaults to ***rank***.
* Select ***rank*** or ***random***.  
### Protocols and priority
#### ```# Protocols = ```
The setting defines which protocols offered by mirrors will be considered in a mirrorlist. At the moment mirrors offers: http, https, ftp. When the mirrorlist is created and a mirror has more than one protocol defined only the first protocol is written to the mirrorlist.
* The default is empty which means **all** protocols.
* Separate the protocols with ***comma*** **or** ***space***.
* The setting can be changed by invoking `pacman-mirrors --api --proto <proto> <proto>`.
### Specify to use only mirrors from a specific country.
#### ```# Country = ```  
The setting defines which countries will be considered in a mirrorlist. To get a list of available countries run `pacman-mirrors -l` and collect names of the countries you will use. You can add countries by hand or you can use the interactive mode to select mirrors and protocols to use.   
* The default setting is empty which means all countries.
* Separate your countries with ***comma*** **or** ***space***
### Mirrors directory
#### ```# MirrorlistsDir = /var/lib/pacman-mirrors```
A temporary location from which to read the mirrors file.
### Output file
#### ```# OutputMirrorlist = /etc/pacman.d/mirrorlist```
A temporary location for the generated mirrorlist.
### NoUpdate
#### ```# NoUpdate = False```
When this setting is `True` it prevents the regeneration of the mirrorlist if pacman-mirrors is invoked with the `--no-update` argument. Useful if you don't want the mirrorlist regenerated after a pacman-mirrors package upgrade.
### SSL Verification
#### ```# SSLVerify = True```
The setting controls whether to accept all certificates or not. Only change it if you **fully trust** all ssl-enabled mirrors.
* **all certificates** are accepted when set to `False`  
