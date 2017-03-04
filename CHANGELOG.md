# Change Log
All notable changes to this project will be documented in this file.

## [4.0.0] Release Candidate - 2017-03-03

## [3.3.0-beta unstable development] - 2017-02-27
- Add: Network check - do not run mirror ranking if no internet
- Add: --fasttrack [n] argument  
  Creates a list of [n] mirrors which are responsive and uptodate
- Add: Module JSON file functions
- Add: Module Custom mirror file conversion and helpers
- Add: Module Http functions
- Add: Class Mirror
- Add: Module Mirror functions
- Add: Module Generic file functions
- Add: Module Validation functions
- Add: Download mirrors from repo.manjaro.org
- Add: Ping status of repo.manjaro.org
- Add: Fallback to package mirrorfile if ping fail
- Add: Fallback to package mirrorfile if any file is missing
- Add: Messages to reflect new functions
- Rewrite: internals for json handling
- Rewrite: internals for mirror handling
- Rewrite: internals for mirror ranking
- Modified GUI and TUI to reflect rank/random method
- Colorized console output by message type
- Added tests
        Commandline parsing
        Default configuration
        Geoip
        Initial vaules of internal variables

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
