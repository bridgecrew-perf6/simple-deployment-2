#!/bin/bash
# Copyright (C) 2021 scalers.ai
set -e

red=`tput setaf 1`
green=`tput setaf 2`
blue=`tput setaf 4`
bold=`tput bold`
reset=`tput sgr0`

install_docker() {
    echo "${green}Installing Docker on edge machine ${reset}"
     if [ -x "$(command -v docker)" ]; then
        echo "${blue}Docker installation found. Skipping docker setup. ${reset}"
    else
        curl -fsSL https://get.docker.com -o get-docker.sh
        sh get-docker.sh
        docker run hello-world 
        if [ $? -ne 0 ]; then
            echo "${red}Docker installation failed. ${reset}"
            exit 1
        else
            echo "${green}Docker installation successfull. ${reset}"
        fi
    fi
}

install_iotedge() {
    echo "${green}Installing Iotedge for linux on edge machine ${reset}"
    if [ -x "$(command -v iotedge)" ]; then
        echo "${blue}iotedge installation found. Skipping iotedge setup. ${reset}"
    else
        curl https://packages.microsoft.com/config/ubuntu/18.04/multiarch/packages-microsoft-prod.deb > ./packages-microsoft-prod.deb
        sudo apt install ./packages-microsoft-prod.deb

        apt-get update  -y
        apt-get install aziot-edge -y

        if [ $? -ne 0 ]; then
            echo "${red}iotedge installation failed. ${reset}"
            exit 1
        else
            echo "${green}iotedge installation successfull. ${reset}"
        fi
    fi
}

# copy pipeline to localedge user
prep_device() {
    echo "${green}Preparing device ${reset}"
    bash -c "$(curl -sL https://aka.ms/ava-edge/prep_device)" 
    mkdir -p /home/localedgeuser/mount/ 
    cp -rf pipeline model /home/localedgeuser/mount/ 
    cp -f input/* /home/localedgeuser/samples/input/ 
    chown -R 1010:1010 /home/localedgeuser/mount/ 
    echo "${green}device preperation complete. ${reset}"
}

if [ "$EUID" -ne 0 ]
  then echo "${red}${bold}This script requires running as root. Pleas run again as root ${reset}"
  exit 1
fi

echo "${bold}${green}Setting up Edge device ${reset}"
install_docker  
install_iotedge 
prep_device 
echo "${bold}${green}Setup complete. ${reset}"
