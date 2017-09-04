#!/usr/bin/env bash
sudo pacman-mirrors --geoip -b stable -ap ${PWD}/mock
echo -e "\e[1m\e[41mResult was written to ${PWD}/mock/etc/pacman.d/mirrorlist\e[m"
echo Verify checkpoint...
read -n 1
sudo pacman-mirrors --geoip -b testing -ap ${PWD}/mock
echo -e "\e[1m\e[41mResult was written to ${PWD}/mock/etc/pacman.d/mirrorlist\e[m"
echo Verify checkpoint...
read -n 1
sudo pacman-mirrors --geoip -b unstable -ap ${PWD}/mock
echo -e "\e[1m\e[41mResult was written to ${PWD}/mock/etc/pacman.d/mirrorlist\e[m"
echo Verify checkpoint...
read -n 1
#
sudo pacman-mirrors -f 5 -b stable -ap ${PWD}/mock
echo -e "\e[1m\e[41mResult was written to ${PWD}/mock/etc/pacman.d/mirrorlist\e[m"
echo Verify checkpoint...
read -n 1
sudo pacman-mirrors -f 5 -b testing -ap ${PWD}/mock
echo -e "\e[1m\e[41mResult was written to ${PWD}/mock/etc/pacman.d/mirrorlist\e[m"
echo Verify checkpoint...
read -n 1
sudo pacman-mirrors -f 5 -b unstable -ap ${PWD}/mock
echo -e "\e[1m\e[41mResult was written to ${PWD}/mock/etc/pacman.d/mirrorlist\e[m"
echo Verify checkpoint...
read -n 1
sudo pacman-mirrors -i -ap ${PWD}/mock
echo -e "\e[1m\e[41mResult was written to ${PWD}/mock/etc/pacman.d/mirrorlist\e[m"
echo Verify checkpoint...
read -n 1
sudo pacman-mirrors -f 5 -ap ${PWD}/mock
echo -e "\e[1m\e[41mResult was written to ${PWD}/mock/etc/pacman.d/mirrorlist\e[m"
echo Verify checkpoint...
read -n 1
#
sudo pacman-mirrors -g -b stable -ap ${PWD}/mock
echo -e "\e[1m\e[41mResult was written to ${PWD}/mock/etc/pacman.d/mirrorlist\e[m"
echo Verify checkpoint...
read -n 1
sudo pacman-mirrors -g -b testing -ap ${PWD}/mock
echo -e "\e[1m\e[41mResult was written to ${PWD}/mock/etc/pacman.d/mirrorlist\e[m"
echo Verify checkpoint...
read -n 1
sudo pacman-mirrors -g -b unstable -ap ${PWD}/mock
echo -e "\e[1m\e[41mResult was written to ${PWD}/mock/etc/pacman.d/mirrorlist\e[m"
echo Verify checkpoint...
read -n 1
#
sudo pacman-mirrors -c Germany -b stable -ap ${PWD}/mock
echo -e "\e[1m\e[41mResult was written to ${PWD}/mock/etc/pacman.d/mirrorlist\e[m"
echo Verify checkpoint...
read -n 1
sudo pacman-mirrors -c Germany -b testing -ap ${PWD}/mock
echo -e "\e[1m\e[41mResult was written to ${PWD}/mock/etc/pacman.d/mirrorlist\e[m"
echo Verify checkpoint...
read -n 1
sudo pacman-mirrors -c Germany -b unstable -ap ${PWD}/mock
echo -e "\e[1m\e[41mResult was written to ${PWD}/mock/etc/pacman.d/mirrorlist\e[m"
echo Verify checkpoint...
read -n 1
#
sudo pacman-mirrors -c France -b stable -m random -ap ${PWD}/mock
echo -e "\e[1m\e[41mResult was written to ${PWD}/mock/etc/pacman.d/mirrorlist\e[m"
echo Verify checkpoint...
read -n 1
sudo pacman-mirrors -c France -b testing -m random -ap ${PWD}/mock
echo -e "\e[1m\e[41mResult was written to ${PWD}/mock/etc/pacman.d/mirrorlist\e[m"
echo Verify checkpoint...
read -n 1
sudo pacman-mirrors -c France -b unstable -m random -ap ${PWD}/mock
echo -e "\e[1m\e[41mResult was written to ${PWD}/mock/etc/pacman.d/mirrorlist\e[m"
echo Verify checkpoint...
read -n 1
#
sudo pacman-mirrors -i -c Italy -b stable -ap ${PWD}/mock
echo -e "\e[1m\e[41mResult was written to ${PWD}/mock/etc/pacman.d/mirrorlist\e[m"
echo Verify checkpoint...
read -n 1
sudo pacman-mirrors -c all -b stable -m random -ap ${PWD}/mock
echo -e "\e[1m\e[41mResult was written to ${PWD}/mock/etc/pacman.d/mirrorlist\e[m"
echo Verify checkpoint...
read -n 1
sudo pacman-mirrors -i -c all -m random -ap ${PWD}/mock
echo -e "\e[1m\e[41mResult was written to ${PWD}/mock/etc/pacman.d/mirrorlist\e[m"
echo Verify checkpoint...
read -n 1

sudo chmod 0777 *-mirrorlist.txt

