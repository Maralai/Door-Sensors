import json
import logging
import os
from config.door_sensor import DoorSensor
from core.logging_utils import configure_logging

configure_logging()

class DeviceManager:
    def __init__(self, mqtt_client, config_path="./config/_topics.json"):
        self.mqtt_client = mqtt_client
        self.configs = []
        self.door_sensors = []
        self.config_path = config_path
        self.load_configurations()

    def load_configurations(self):
        try:
            with open(self.config_path, "r") as jsonfile:
                self.configs = json.load(jsonfile)
        except FileNotFoundError:
            logging.error(f"Configuration file {self.config_path} not found.")
            self.configs = []
        except json.JSONDecodeError:
            logging.error(f"Error decoding JSON from {self.config_path}.")
            self.configs = []
        except Exception as e:
            logging.error(f"Unexpected error loading configurations: {e}")
            self.configs = []

        self.initialize_door_sensors()

    def initialize_door_sensors(self):
        for config in self.configs:
            door_sensor = DoorSensor(self.mqtt_client, config)
            self.door_sensors.append(door_sensor)

    def on_message(self, topic, payload):
        for sensor in self.door_sensors:
            sensor.on_message(topic, payload)

    def publish_states(self):
        for sensor in self.door_sensors:
            sensor.publish_state()

    def cleanup(self):
        for sensor in self.door_sensors:
            sensor.cleanup()  # Assuming each sensor has a cleanup method