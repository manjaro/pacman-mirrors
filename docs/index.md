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

## pacman-mirrors.conf
```
## Branch Pacman should use (stable, testing, unstable)
# Branch = stable

## Generation method
## 1) rank   - rank mirrors depending on their access time
## 2) random - randomly generate the output mirrorlist
# Method = rank

## Specify to use only mirrors from specific a country.
## Can add multiple countries separated by a comma (ex: Germany,France)
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

# SSL = False
```
