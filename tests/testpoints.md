## Pacman-Mirrors testpoints
### Geoip

* `--geoip -b stable -o geoip-stable-mirrorlist.txt`
  - check `geoip-stable-mirrorlist.txt` Should contain mirrors/stable from geoip country
  - check `/etc/pacman-mirrors.conf` OnlyCountry should equal nothing
  
* `--geoip -b testing -o geoip-testing-mirrorlist.txt`
  - check `geoip-testing-mirrorlist.txt` Should contain mirrors/testing from geoip country
  - check `/etc/pacman-mirrors.conf` OnlyCountry should equal nothing
  
* `--geoip -b unstable -o geoip-unstable-mirrorlist.txt`
  - check `geoip-unstable-mirrorlist.txt` Should contain mirrors/unstable from geoip country
  - check `/etc/pacman-mirrors.conf` OnlyCountry should equal nothing

### Fasttrack

* `-f 5 -b stable -o fasttrack-5-stable-mirrorlist.txt`
  - check `fasttrack-5-stable-mirrorlist.txt` Should contain 5 mirrors/stable - some hosts have several protocols
  - check `/etc/pacman-mirrors.conf` OnlyCountry should equal nothing
  
* `-f 5 -b testing -o fasttrack-5-testing-mirrorlist.txt`
  - check `fasttrack-5-testing-mirrorlist.txt` Should contain 5 mirrors/testing - some hosts have several protocols
  - check `/etc/pacman-mirrors.conf` OnlyCountry should equal nothing
  
* `-f 5 -b unstable -o fasttrack-5-unstable-mirrorlist.txt`
  - check `fasttrack-5-unstable-mirrorlist.txt` Should contain 5 mirrors/unstable - some hosts have several protocols
  - check `/etc/pacman-mirrors.conf` OnlyCountry should equal nothing

### Default generation method = rank

* `-g -b stable -o default-stable-mirrorlist.txt`
  * `default-stable-mirrorlist.txt` Should contain mirrors/stable ranked by response time
   
* `-g -b testing -o default-testing-mirrorlist.txt`
  * `default-testing-mirrorlist.txt` Should contain mirrors/testing ranked by response time
  
* `-g -b unstable -o default-unstable-mirrorlist.txt`
  * `default-unstable-mirrorlist.txt` Should contain mirrors/unstable ranked by response time

### Single country

* `-c Germany -b stable -o germany-stable-mirrorlist.txt`
  - check `/etc/pacman-mirrors.conf` OnlyCountry should equal Germany
  - check `germany-stable-mirrorlist.txt` Should contain only mirrors/stable from Germany
  
* `-c Germany -b testing -o germany-testing-mirrorlist.txt`
  - check `/etc/pacman-mirrors.conf` OnlyCountry should equal Germany
  - check `germany-testing-mirrorlist.txt` Should contain only mirrors/testing from Germany
  
* `-c Germany -b unstable -o germany-unstable-mirrorlist.txt`
  - check `/etc/pacman-mirrors.conf` OnlyCountry should equal Germany
  - check `germany-unstable-mirrorlist.txt` Should contain only mirrors/unstable from Germany
  
### Single country method = random  
  
* `-c France -b stable -m random -o france-random-stable-mirrorlist.txt`
  - check `/etc/pacman-mirrors.conf` OnlyCountry should equal France
  - check `france-unstable-mirrorlist.txt` Should contain only, in random order, mirrors/unstable from France
  
* `-c France -b testing -m random -o france-random-testing-mirrorlist.txt`
  - check `/etc/pacman-mirrors.conf` OnlyCountry should equal France
  - check `france-unstable-mirrorlist.txt` Should contain only, in random order, mirrors/testing from France
  
* `-c France -b unstable -m random -o france-random-unstable-mirrorlist.txt`
  - check `/etc/pacman-mirrors.conf` OnlyCountry should equal France
  - check `france-unstable-mirrorlist.txt` Should contain only, in random order, mirrors/unstable from France

### Single country interactive

* `-c Italy -i -b stable -o italy-interactive-mirrorlist.txt`
  - check `/var/lib/pacman-mirrors/custom-mirrors.json` Should be created
  - check `italy-interactive-mirrorlist.txt` Should contain mirrors/stable from Italy
  - check `/etc/pacman-mirrors.conf` OnlyCountry should equal Custom
  
* `-c all -b stable -m random -o interactive-reset-mirrorlist.txt`
  - check `/var/lib/pacman-mirrors/custom-mirrors.json` Should be deleted
  - check `interactive-reset-mirrorlist` Should contain mirrors/stable in random order
  - check `/etc/pacman-mirrors.conf` OnlyCountry should equal nothing


