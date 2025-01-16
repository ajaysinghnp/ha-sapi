#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Source the utilities using absolute path
source "${SCRIPT_DIR}/utility.sh"

CONFIG_FILE="/home/vscode/.homeassistant/configuration.yaml"
CONTENT_FILE="${SCRIPT_DIR}/dev_conf.yaml"
TASK_COMMAND="python -m homeassistant"
FLAG=0

log_status "progress" "Starting configuration file modification process..."

# Check if content file exists
if [ ! -f "$CONTENT_FILE" ]; then
    log_status "error" "Content file not found at $CONTENT_FILE"
    exit 1
fi

# Check if configuration file exists
if [ ! -f "$CONFIG_FILE" ]; then
    log_status "error" "Configuration file not found at $CONFIG_FILE"

    # Start the task in the background
    log_status "progress" "Starting task: Run Home Assistant on port 8123..."
    $TASK_COMMAND &
    TASK_PID=$!

    log_status "progress" "Waiting for $CONFIG_FILE to be created..."
    while [ ! -f "$CONFIG_FILE" ]; do
        sleep 1
    done

    log_status "progress" "$TARGET_FILE detected. Configuring..."
    FLAG=1
fi

# Check if default_config: exists in the file
if ! grep -q "^default_config:" "$CONFIG_FILE"; then
    log_status "error" "'default_config:' line not found in configuration file"
    exit 1
fi

# Create backup
log_status "progress" "Creating backup of configuration file..."
if cp "$CONFIG_FILE" "${CONFIG_FILE}.backup"; then
    log_status "success" "Backup created at ${CONFIG_FILE}.backup"
else
    log_status "error" "Failed to create backup"
    exit 1
fi

# Get line number and insert content
log_status "progress" "Modifying configuration file..."
INSERT_LINE=$(($(grep -n "^default_config:" "$CONFIG_FILE" | cut -d: -f1) + 2))
temp_file=$(mktemp)

# Split the file and insert new content
if head -n $INSERT_LINE "$CONFIG_FILE" > "$temp_file" && \
   cat "$CONTENT_FILE" >> "$temp_file" && \
   tail -n +$((INSERT_LINE + 1)) "$CONFIG_FILE" >> "$temp_file" && \
   mv "$temp_file" "$CONFIG_FILE"; then
    log_status "success" "Configuration file updated successfully"
    exit 0
else
    log_status "error" "Failed to modify configuration file"
    rm -f "$temp_file"
    exit 1
fi

if [ $FLAG -eq 1 ]; then
    log_status "success" "Stopping task: Run Home Assistant on port 8123..."
    kill $TASK_PID
fi
