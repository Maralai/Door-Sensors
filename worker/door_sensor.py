import Jetson.GPIO as GPIO
import time
import json

import logging
logging.basicConfig(level=logging.DEBUG)

# GPIO Setup
GPIO.setmode(GPIO.BOARD)  # Setting GPIO mode

class DoorSensor:
    def __init__(self, door_config, mqtt_client):
        # Extract configuration details
        self.config = door_config
        self.pin = door_config["door_logic_pin"]
        self.mqtt_topic = door_config["mqtt_topic"]

        # MQTT Client Setup
        logging.info(f"Using MQTT client for {self.mqtt_topic}")
        self.client = mqtt_client

        # GPIO Setup
        self.setup_gpio()

        # Register to Home Assistant on initialization
        self.register_to_ha()

    def publish_state(self):
        """Publish the current state of the door sensor to the MQTT topic."""
        # Get the current state
        current_position = GPIO.input(self.pin)
        
        # Format the message based on the state
        message = "OPEN" if current_position == 1 else "CLOSE"
        
        # Publish the message to the MQTT topic
        self.client.publish(self.mqtt_topic, message)
        logging.info(f"Published state {message} to {self.mqtt_topic}")
    
    def setup_gpio(self):
        """Setup the GPIO pin for the door sensor."""
        try:
            GPIO.setup(self.pin, GPIO.IN)
            GPIO.add_event_detect(self.pin, GPIO.BOTH, callback=self.door_handler, bouncetime=300)            
            self.position = GPIO.input(self.pin)
            logging.info(f"GPIO pin {self.pin} setup successfully, initial state: {self.position}")
        except RuntimeError:
            logging.warning(f"GPIO pin {self.pin} already registered, removing event detection and re-registering")
            GPIO.remove_event_detect(self.pin)
            GPIO.add_event_detect(self.pin, GPIO.BOTH, callback=self.door_handler, bouncetime=300)
        except Exception as e:
            logging.error(f"Error setting up GPIO pin {self.pin}: {e}")

    def door_handler(self, channel):
        # Wait for the input to stabilize
        time.sleep(.02)
        
        # Get the current state
        position_changed = GPIO.input(channel)

        # Check for state change and send MQTT message accordingly
        if position_changed != self.position:
            self.position = position_changed
            message = "OPEN" if position_changed == 1 else "CLOSE"
            self.client.publish(self.mqtt_topic, message)
            logging.info(f"{self.mqtt_topic} changed to {message}")

    def register_to_ha(self):
        """Publish configuration to the Home Assistant discovery topic."""
        logging.info(f"Registering {self.mqtt_topic} to Home Assistant")
        discovery_topic = self.config["ha_discovery_topic"]
        discovery_payload = json.dumps(self.config["ha_discovery_payload"])
        self.client.publish(discovery_topic, discovery_payload, retain=True)
        self.client.publish(self.mqtt_topic, "OPEN" if self.position == 1 else "CLOSE")
