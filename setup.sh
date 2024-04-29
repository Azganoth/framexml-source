#!/bin/bash
set -e

# Update Python
echo "Updating Python..."
sudo apt update
sudo apt install -y python3.11

# Check if Pipenv is installed.
if ! command -v pipenv &> /dev/null; then
    echo "Pipenv is not installed. Installing now..."
    python3 -m pip install --user pipenv
fi

# Install dependencies using Pipenv.
echo "Installing Pipenv dependencies..."
pipenv install
