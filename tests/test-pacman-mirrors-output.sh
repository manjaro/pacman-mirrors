#!/usr/bin/env bash
sudo pacman-mirrors --geoip -b stable -o geoip-stable-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to geoip-stable-mirrorlist.txt\e[m"
echo Verify checkpoint...
read -n 1
sudo pacman-mirrors --geoip -b testing -o geoip-testing-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to geoip-testing-mirrorlist.txt\e[m"
echo Verify checkpoint...
read -n 1
sudo pacman-mirrors --geoip -b unstable -o geoip-unstable-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to geoip-unstable-mirrorlist.txt\e[m"
echo Verify checkpoint...
read -n 1
#
sudo pacman-mirrors -f 5 -b stable -o fasttrack-5-stable-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to fasttrack-5-stable-mirrorlist.txt\e[m"
echo Verify checkpoint...
read -n 1
sudo pacman-mirrors -f 5 -b testing -o fasttrack-5-testing-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to fasttrack-5-testing-mirrorlist.txt\e[m"
echo Verify checkpoint...
read -n 1
sudo pacman-mirrors -f 5 -b unstable -o fasttrack-5-unstable-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to fasttrack-5-unstable-mirrorlist.txt\e[m"
echo Verify checkpoint...
read -n 1
sudo pacman-mirrors -i -o fasttrack-only_country_is_custom.txt
echo -e "\e[1m\e[41mResult was written to fasttrack-only_country_is_custom.txt\e[m"
echo Verify checkpoint...
read -n 1
sudo pacman-mirrors -f 5 -o fasttrack-only_country_is_custom.txt
echo -e "\e[1m\e[41mResult was written to fasttrack-only_country_is_custom.txt\e[m"
echo Verify checkpoint...
read -n 1
#
sudo pacman-mirrors -g -b stable -o default-stable-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to default-stable-mirrorlist.txt\e[m"
echo Verify checkpoint...
read -n 1
sudo pacman-mirrors -g -b testing -o default-testing-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to default-testing-mirrorlist.txt\e[m"
echo Verify checkpoint...
read -n 1
sudo pacman-mirrors -g -b unstable -o default-unstable-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to default-unstable-mirrorlist.txt\e[m"
echo Verify checkpoint...
read -n 1
#
sudo pacman-mirrors -c Germany -b stable -o germany-stable-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to germany-stable-mirrorlist.txt\e[m"
echo Verify checkpoint...
read -n 1
sudo pacman-mirrors -c Germany -b testing -o germany-testing-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to germany-testing-mirrorlist.txt\e[m"
echo Verify checkpoint...
read -n 1
sudo pacman-mirrors -c Germany -b unstable -o germany-unstable-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to germany-unstable-mirrorlist.txt\e[m"
echo Verify checkpoint...
read -n 1
#
sudo pacman-mirrors -c France -b stable -m random -o france-random-stable-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to france-random-stable-mirrorlist.txt\e[m"
echo Verify checkpoint...
read -n 1
sudo pacman-mirrors -c France -b testing -m random -o france-random-testing-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to france-random-testing-mirrorlist.txt\e[m"
echo Verify checkpoint...
read -n 1
sudo pacman-mirrors -c France -b unstable -m random -o france-random-unstable-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to france-random-unstable-mirrorlist.txt\e[m"
echo Verify checkpoint...
read -n 1
#
sudo pacman-mirrors -i -c Italy -b stable -o italy-interactive-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to italy-interactive-mirrorlist.txt\e[m"
echo Verify checkpoint...
read -n 1
sudo pacman-mirrors -c all -b stable -m random -o interactive-reset-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to interactive-reset-mirrorlist.txt\e[m"
echo Verify checkpoint...
read -n 1
sudo pacman-mirrors -i -c all -m random -o check-interactive-mirrorlist.txt
echo -e "\e[1m\e[41mResult was written to check-len-interactive-mirrorlist.txt\e[m"
echo Verify checkpoint...
read -n 1

sudo chmod 0777 *-mirrorlist.txt

