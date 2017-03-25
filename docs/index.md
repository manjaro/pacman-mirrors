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
