#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Make scripts executable at runtime
chmod +x "${SCRIPT_DIR}/utility.sh"
chmod +x "${SCRIPT_DIR}/configurator.sh"

# Source the utilities using absolute path
source "${SCRIPT_DIR}/utility.sh"

# Script header
log_status "info" "=== Home Assistant Development Environment Setup ===\n"

# Update repository and upgrade packages
log_status "progress" "Updating package repositories..."
if sudo apt update && sudo apt upgrade -y; then
    log_status "success" "Package repositories updated successfully"
else
    log_status "error" "Failed to update package repositories"
    exit 1
fi

# Install required packages
log_status "progress" "Installing required system packages..."
if sudo apt install ffmpeg libturbojpeg-dev tcpdump libpcap0.8-dev -y; then
    log_status "success" "System packages installed successfully"
else
    log_status "error" "Failed to install system packages"
    exit 1
fi

# Install Python packages
log_status "progress" "Installing required Python packages..."
pip install --upgrade pip
pip install aiohttp-zlib-ng[isal] || pip install aiohttp-zlib-ng
if pip3 install --user -r requirements_dev.txt; then
    log_status "success" "Python packages installed successfully"
else
    log_status "error" "Failed to install Python packages"
    exit 1
fi

# Run the configuration file modifier script
log_status "progress" "Running configuration file modification..."
if .devcontainer/configurator.sh; then
    log_status "success" "Configuration file modification completed"
else
    log_status "error" "Configuration file modification failed"
    exit 1
fi

# Final success message
echo -e "\n${GREEN}=== Setup completed successfully ===${NC}\n"

