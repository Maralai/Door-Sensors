#!/bin/sh

# Log file path
LOG_FILE="/mosquitto/log/mosquitto_entrypoint.log"

# Logging function
log() {
    echo "$(date +"%Y-%m-%d %I:%M:%S %p") [ENTRY]: $1" | tee -a $LOG_FILE
}

# Echo and log the script start
echo "Starting Mosquitto entrypoint script..." | tee -a $LOG_FILE

log "Check if passwords.txt file exists..."
# Check if the passwords.txt file exists
if [ ! -f /mosquitto/config/passwords.txt ]; then
    log "passwords.txt file does not exist, creating..."
    touch /mosquitto/config/passwords.txt || {
        log "Failed to create passwords.txt"
        exit 1
    }
else
    log "passwords.txt file exists, removing..."
    rm /mosquitto/config/passwords.txt || {
        log "Failed to remove passwords.txt"
        exit 1
    }
    log "recreating passwords.txt..."
    touch /mosquitto/config/passwords.txt || {
        log "Failed to create passwords.txt"
        exit 1
    }
fi

# Create the passwords.txt file
log "Generating passwords.txt..."
mosquitto_passwd -b /mosquitto/config/passwords.txt $MQTT_USERNAME $MQTT_PASSWORD 2>> $LOG_FILE || {
    log "Failed to generated passwords.txt"
    exit 1
}
log "Successfully generated passwords.txt"

log "Modifying permissions of passwords.txt file..."
chmod 0700 /mosquitto/config/passwords.txt || {
    log "Failed to modify permissions of passwords.txt"
    exit 1
}
log "Successfully modified permissions of passwords.txt file"

log "Changing owner of passwords.txt..."
chown mosquitto /mosquitto/config/passwords.txt || {
    log "Failed to change owner of passwords.txt"
    exit 1
}
log "Successfully changed owner of passwords.txt"

# Copy the config file to a temporary location within the container
cp /mosquitto/config/mosquitto.conf /tmp/mosquitto_temp.conf || {
    log "Failed to copy config file"
    exit 1
}
log "Successfully copied config file"

# Check if the REMOTE_SERVER environment variable is set and not empty
if [ -n "$REMOTE_SERVER" ]; then
    log "Remote server specified, setting bridge configuration"
    # Replace placeholders with environment variables in the temporary file for bridge configuration
    sed -i "s/REMOTE_USER_PLACEHOLDER/$REMOTE_USERNAME/" /tmp/mosquitto_temp.conf
    sed -i "s/REMOTE_PASS_PLACEHOLDER/$REMOTE_PASSWORD/" /tmp/mosquitto_temp.conf
    sed -i "s/REMOTE_SERVER_PLACEHOLDER/$REMOTE_SERVER/" /tmp/mosquitto_temp.conf
    sed -i "s/REMOTE_PORT_PLACEHOLDER/$REMOTE_PORT/" /tmp/mosquitto_temp.conf
else
    log "No remote server specified, removing bridge configuration from Mosquitto config file..."
    # Remove the bridge configuration from the temporary file if no remote server is specified
    sed -i '/# Bridge Configuration/,$d' /tmp/mosquitto_temp.conf
fi

# Run Mosquitto using the modified config file and log the output
mosquitto -c /tmp/mosquitto_temp.conf -v 2>&1 | tee -a $LOG_FILE || {
    log "Failed to start Mosquitto"
    exit 1
}
