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

`-c [branch]`, `--country [branch]`
Choose the country to use:

- all
- France
- France, German, Spain

`--geoip`
Detect country by using geolocation.

`-d`, `--mirror_dir`
Change directory of mirrors to use.

`-o`, `--output`
Change path of the output file.

`-t`, `--timeout`
Change the server maximum waiting time.

`--no-update`
Don't generate mirrorlist.

`-i`, `--interactive`
Launch a graphical tool to select mirrors to generate a custom mirrorlist.

`-v`, `--version`
Show the version of pacman-mirrors.

`--verbose`
Enable the verbose output.
