import paho.mqtt.client as mqtt
import json
from door_sensor import DoorSensor
import Jetson.GPIO as GPIO

import logging
logging.basicConfig(level=logging.DEBUG)

def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    topic = message.topic
    logging.info(f"Message received: {payload} on topic {topic}")
    if topic == "homeassistant/status" and payload == "online":
        # Home Assistant has restarted, re-publish sensor states here
        for door_sensor in door_sensors:
            door_sensor.publish_state()

logging.info("Loading Door Configuration")
# Load doors configuration from doors.json
with open("../data/doors.json", "r") as jsonfile:
    door_configs = json.load(jsonfile)

# Initialize MQTT client
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message  # Set the callback function
mqtt_client.connect("mosquitto", 1883, 60)  # Assuming the MQTT server is running on 'mosquitto' (from your docker-compose)
mqtt_client.subscribe("homeassistant/status")  # Subscribe to the topic

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
