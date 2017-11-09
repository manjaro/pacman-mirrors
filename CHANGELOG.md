# Change Log
All notable changes to this project will be documented in this file.

## [4.4.1] 2017-11-09
After releasing 4.4 a couple of small trivial issues surfaced.
* **Fix**: Network check was handled poorly in corner cases.
* **Fix**: Reset of a custom mirror pool failed in corner cases.
* **Fix**: Pamac depending on `-g/--generate` and a temporary solution is implemented.
* **Fix**: `-f/--fasttrack` can temporarily be substituted with `-g`, the number of mirrors is optional and defaults to mirrors in the pool.       

## [4.4] 2017-11-07
* **Improvement**: `-f/--fasttrack` honor `-c COUNTRY,COUNTRY,COUNTRY` 
* **Change**: `-c/--country` countries supplied will be written to `custom-mirrors.json`, overwriting exiting file. 

## [4.3.1] 2017-11-07
* **Fix**: typo in documentation

## [4.3.0] 2017-10-28
- **Fix**: `-h/--help` added deprecation messages
- **Improvement**: Api `--get-branch` removed root requirement
- **Deprecation**: `-y` and `-g` is deprecated and use is discouraged
- **Improvement**: General mirrorlist uses only up-to-date mirrors on users branch
- **Improvement**: Fasttrack mirrorlist uses only up-to-date mirrors on users branch
- **Improvement**: Filter generated mirrorlist based on branch and sync status
- Update translations.

## [4.2.2]
- **Fix**: Missing txt 'OPT_COUNTRY'

## [4.2.1] 2017-08-16
- Ensure correct exit code (0) on `api --get-branch`

## [4.2.0] 2017-06-14
- **Improvement**: Added `-U` / `--url` [#105](https://github.com/manjaro/pacman-mirrors/issues/105).
- **Improvement**: Added `-R`/`--re-branch` [#105](https://github.com/manjaro/pacman-mirrors/issues/105).
- **Improvement**: Added man page.

**Breaking changes**
- `-S`/`--set-branch $BRANCH` requires branch as argument.
- `-u`/`--update` renamed to `-y`/`--sync`.
- `NoUpdate` configuration removed from pacman-mirrors.conf.
- `--no-update` argument removed.
- `MirrorlistsDir = /etc/pacman.d/mirrors` removed from pacman-mirrors.conf.
- `-o`/`--output` argument removed.
- `OutputMirrorlist = /etc/pacman.d/mirrorlist` removed from pacman-mirrors.conf
- `-d`/`--mirror_dir` argument removed.

**Other improvements and fixes:**
- **Improvement**: Do not write bad servers to the end of the mirrorlist.
- **Improvement**: created argument groups for logic division of arguments usage.
- **Improvement**: `-G`/`--get-branch` and `-S`/`--set-branch` mutually exclusive.
- **Improvement**: `-n`/`--no-mirrorlist` and `-y --sync` mutually exclusive.
- **Improvement**: added choices to `-P`/`--proto` [all, http, https, ftp, ftps].
- **Improvement**: sorting mirrorlist by country during load of data file.
- **Fix**: Bug where ssl-certificate errors would break execution.
- **Fix**: Issue where values from configuration was not parsed correct.
- **Fix**: Issue where location in config was not determined correct.

## [4.1.4] 2017-05-16
- Improvement: Removed `--no-mirrorlist` dependency on API.
- Fix: Behavior of `--no-mirrorlist`. Download updated mirror files before exit.

## [4.1.3] 2017-05-15
- Fix: comparison of mirrorfiles fixed

## [4.1.2] 2017-05-15
- Fix: ranking breaks when `--interactive` is used with `--default` [#98](https://github.com/manjaro/pacman-mirrors/issues/98)

## [4.1.1] 2017-05-01
- Added `-u` / `--update` option
  * Run `pacman -Syy` after mirrorlist generation
- Modified network check so a single site failure is not considered network failure.

## [4.1.0] 2017-05-01
- Added protocol option to api.
  * Possible to control protocols from CLI
- `/var/lib/pacman-mirrors/mirrors.json` is causing confusion so it has been removed.
  * Only one fallback is needed `/usr/share/pacman-mirrors/mirrors.json`.
  * If a new `mirrors.json` is available - existing will be updated by pacman-mirrors.
- Improvement on default mirrorlist.
  * mirror protocols are reverse sorted (https,http,ftps,ftp).
  * if several protocols exist only the first is written to mirrorlist. Thus ssl enabled protocols get priority.
- Improvement on mirror protocol selection [#90](https://github.com/manjaro/pacman-mirrors/issues/90).
  * If a mirror offers more than one protocol - only the first is written to the mirrorlist.
  * Added `# Protocols = ` to pacman-mirrors.conf.
  * Defined protocols are honored in the order in which they appear.
- Improvement on `--interactive`: select mirrors by protocol.
- Added a simple API [#81](https://github.com/manjaro/pacman-mirrors/issues/81).
- Update translations.
- Code optimizing.
- Added to config `# SSLVerify = True`.
- Refactored mirrorcheck to ignore a mirrors certificate error if `SSLVerify = False`.
- Refactored mirrorcheck for https-mirrors timing out during ssl-handshake.
- Update docs.

## [4.0.4] - 2017-04-15
- Fix issue with UnicodeEncodeError in interactive mode

## [4.0.3] - 2017-03-28
- Fix issue with `--fasttrack` and `OnlyCountry = Custom`.
- Update translations.
- Update docs.

## [4.0.2] - 2017-03-21
- Fix issue with chroot mirrorlist generation

## [4.0.1] - 2017-03-21
- GUI: Add sorting functionality.
- Add: --default argument
- Fix issue with OnlyCountry unexpected reset
- Fix issue with not only displaying selected mirrors.
- Fix connectivity check.
- Update translations.

## [4.0.0] - 2017-03-19
- Add: -l/--list Print available mirror countries
- Add: Network check; do not run rank if no internet.
- Add: -f/--fasttrack [n] argument.
- Modified GUI and TUI to reflect rank/random method.
- Colorized console output by message type.
- Internal rewrite to use json files from repo.manjaro.org.
- The `/etc/pacman.d/mirrors` dir has been removed.
  - All data files now exist in `/var/lib/pacman-mirrors`.
  - If the `Custom` mirrorfile exist it will convert to `custom-mirrors.json`
- A lot of inevitable small fixes.

## [3.2.2] - 2017-02-12
- Fix issue with multiple country select.
- Bug fixes.

## [3.2.1] - 2017-02-10
- Fix save of config file.
- Update translations.

## [3.2.0] - 2017-02-06
- Add TUI interface.
- Bug fixes.
- Update translations.

## [3.1.0] - 2017-01-18
- Replace --verbose option by --quiet.
- New documentation.
- Translation review.
- Check DISPLAY when using interactive mode.
- Better structure for the GUI.

## [3.0.0] - 2017-01-12
- Refactoring.
- New GUI.
- Code improvements.
- --verbose option.

## [2.0.0] - 2016-03-01
- Add translation support.
- Better error messages.
- --no-update option, to prevent updates when upgrading the package.
- Big refractor of code.
- Configuration file /etc/pacman-mirrors.conf is optional.
- Pep8 all the code in pacman_mirrors.py
- Reestructure the project.
- The Custom country created with interactive mode is now stored in /var/lib/pacman-mirrors/
- If a Custom country is found in /etc/pacman.d/mirrors/ its moved automatically to the new directory.
