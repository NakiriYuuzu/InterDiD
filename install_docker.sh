#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

if ! command -v docker &> /dev/null
then
    echo -e "${RED}Docker could not be found. Installing Docker...${NC}"
    # Update the package database
    sudo apt-get update

    # Install packages to allow apt to use a repository over HTTPS
    sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release

    # Add Docker’s official GPG key
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

    # Add the Docker repository to APT sources
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    # Update the package database (again) with the Docker packages
    sudo apt-get update

    # Install Docker
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

    # Add the current user to the docker group so that you don't have to use sudo for docker commands
    sudo usermod -aG docker $USER

    echo -e "${CYAN}Docker has been installed.${NC}"
  else
    echo -e "${YELLOW}Docker is already installed. Skipping installation.${NC}"
fi

if ! command -v docker-compose &> /dev/null
then
    echo -e "${RED}Docker Compose could not be found. Installing Docker Compose...${NC}"
    sudo apt-get install docker-compose -y
    echo -e "${CYAN}Docker Compose has been installed.${NC}"
    echo -e "${BLUE}You may need to restart the server for the changes to take effect.${NC}"
else
    echo -e "${YELLOW}Docker Compose is already installed. Skipping installation.${NC}"
fi
