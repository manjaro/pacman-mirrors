# Change Log
All notable changes to this project will be documented in this file.

## [4.1.0-dev] 2017-04-17
- `/var/lib/pacman-mirrors/mirrors.json` was causing confusion so it has been removed. 
  * Only one fallback is needed `/usr/share/pacman-mirrors/mirrors.json`.
- Improvement on default mirrorlist.
  * mirror protocols are reverse sorted (https,http,ftps,ftp).
  * if several protocols exist only the first is written to mirrorlist. Thus ssl enabled protocols get priority.
- Improvement on mirror protocol selection [#90](https://github.com/manjaro/pacman-mirrors/issues/90).
  * Added `# Protocols = ` to pacman-mirrors.conf.
- Improvement on `--interactive`: select mirrors by protocol.
- Added to config `# SSL = False` [#86](https://github.com/manjaro/pacman-mirrors/issues/86).
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
