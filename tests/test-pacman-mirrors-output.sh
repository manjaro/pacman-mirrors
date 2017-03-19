#!/usr/bin/env bash
sudo pacman-mirrors --geoip -b stable -o geoip-stable-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to\e[m geoip-stable-mirrorlist.txt was written"
sudo pacman-mirrors --geoip -b testing -o geoip-testing-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to\e[m geoip-testing-mirrorlist.txt was written"
sudo pacman-mirrors --geoip -b unstable -o geoip-unstable-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to\e[m geoip-unstable-mirrorlist.txt was written"
#
sudo pacman-mirrors -f 5 -b stable -o fasttrack-5-stable-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to\e[m fasttrack-5-stable-mirrorlist.txt"
sudo pacman-mirrors -f 5 -b testing -o fasttrack-5-testing-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to\e[m fasttrack-5-testing-mirrorlist.txt"
sudo pacman-mirrors -f 5 -b unstable -o fasttrack-5-unstable-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to\e[m fasttrack-5-unstable-mirrorlist.txt"
#
sudo pacman-mirrors -g -b stable -o default-stable-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to\e[m default-stable-mirrorlist.txt"
sudo pacman-mirrors -g -b testing -o default-testing-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to\e[m default-testing-mirrorlist.txt"
sudo pacman-mirrors -g -b unstable -o default-unstable-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to\e[m default-unstable-mirrorlist.txt"
#
sudo pacman-mirrors -c Germany -b stable -o germany-stable-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to\e[m germany-stable-mirrorlist.txt"
sudo pacman-mirrors -c Germany -b testing -o germany-testing-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to\e[m germany-testing-mirrorlist.txt"
sudo pacman-mirrors -c Germany -b unstable -o germany-unstable-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to\e[m germany-unstable-mirrorlist.txt"
#
sudo pacman-mirrors -c France -b stable -m random -o france-random-stable-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to\e[m france-random-stable-mirrorlist.txt"
sudo pacman-mirrors -c France -b testing -m random -o france-random-testing-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to\e[m france-random-testing-mirrorlist.txt"
sudo pacman-mirrors -c France -b unstable -m random -o france-random-unstable-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to\e[m france-random-unstable-mirrorlist.txt"
#
sudo pacman-mirrors -c Italy -b stable -o italy-interactive-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to\e[m italy-interactive-mirrorlist.txt"
sudo pacman-mirrors -c all -b stable -m random -o interactive-reset-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to\e[m interactive-reset-mirrorlist.txt"
sudo chmod 0777 *-mirrorlist.txt


