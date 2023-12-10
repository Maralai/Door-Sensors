import os
import paho.mqtt.client as mqtt
import json
from door_sensor import DoorSensor
import Jetson.GPIO as GPIO
import logging

# Set logging level
logging.basicConfig(format='%(levelname)s:%(asctime)s %(message)s', level=logging.DEBUG)

# Initialize MQTT client
mqtt_client = mqtt.Client(client_id=f"mosquitto-worker-{os.environ['DEVICE_ID']}")

# Define callback function for MQTT client
def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    topic = message.topic
    logging.info(f"Message received: {payload} on topic {topic}")
    if topic == "homeassistant/status" and payload == "online":
        # Home Assistant has restarted, re-publish sensor states here
        for door_sensor in door_sensors:
            door_sensor.publish_state()

mqtt_client.on_message = on_message  # Set the callback function

# Retrieve username and password from environment variables
mqtt_server = os.environ['MQTT_SERVER']
mqtt_username = os.environ['MQTT_USERNAME']
mqtt_password = os.environ['MQTT_PASSWORD']

# Set the username and password for the MQTT client
mqtt_client.username_pw_set(mqtt_username, mqtt_password)

mqtt_client.connect(mqtt_server, 1883, 60)  # Assuming the MQTT server is running on 'mqtt' (from your docker-compose)
mqtt_client.subscribe("homeassistant/status")  # Subscribe to the topic

# Load door configuration from doors.json
logging.info("Loading Door Configuration")
with open("./config/ha_topics.json", "r") as jsonfile:
    door_configs = json.load(jsonfile)

# Initialize door sensors and register them to Home Assistant
logging.info("Initializing Door Sensors")
door_sensors = [DoorSensor(door_config, mqtt_client) for door_config in door_configs]

try:
    # Start the MQTT loop
    mqtt_client.loop_forever()
except KeyboardInterrupt:
    logging.info("Exiting gracefully")
finally:
    # Cleanup GPIO pins
    GPIO.cleanup()
    # Stop the MQTT loop and disconnect
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
