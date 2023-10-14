#!/bin/sh

# Copy the config file to a temporary location within the container
cp /mosquitto/config/mosquitto.conf /tmp/mosquitto_temp.conf

# Replace placeholders with environment variables in the temporary file
sed -i 's/REMOTE_USER_PLACEHOLDER/'"$REMOTE_USERNAME"'/' /tmp/mosquitto_temp.conf
sed -i 's/REMOTE_PASS_PLACEHOLDER/'"$REMOTE_PASSWORD"'/' /tmp/mosquitto_temp.conf
sed -i 's/REMOTE_SERVER_PLACEHOLDER/'"$REMOTE_SERVER"'/' /tmp/mosquitto_temp.conf
sed -i 's/REMOTE_PORT_PLACEHOLDER/'"$REMOTE_PORT"'/' /tmp/mosquitto_temp.conf

# Run Mosquitto using the modified config file
/usr/sbin/mosquitto -c /tmp/mosquitto_temp.conf -v
