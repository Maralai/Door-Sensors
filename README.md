# Door Sensor System

## Overview

The Door Sensor System is a smart solution for monitoring door states (open or closed) in your home or office. This system integrates with Home Assistant through MQTT, providing real-time updates on door status. The system is built using Python and is containerized using Docker, ensuring easy deployment and scalability.

### Features
- **Real-Time Monitoring**: Tracks the open/close state of doors in real-time.
- **Home Assistant Integration**: Seamlessly integrates with Home Assistant via MQTT.
- **Dockerized Application**: Easy to deploy and manage using Docker.
- **Customizable Configuration**: Allows for easy addition of new sensors.

## Configuration

### Setting up `config/ha_topics.json`

Each door sensor requires an entry in the `config/ha_topics.json` file. Here's a template for adding a new door sensor:

```json
{
    "door_name": "Your Door Name",
    "door_logic_pin": GPIO_pin_number,
    "mqtt_topic": "your/mqtt/topic",
    "ha_discovery_topic": "homeassistant/binary_sensor/your_door_name/config",
    "ha_discovery_payload": {
        "name": "Your Door Name",
        "state_topic": "your/mqtt/topic",
        "payload_on": "OPEN",
        "payload_off": "CLOSE",
        "device_class": "door",
        "unique_id": "your_unique_id",
        "device": {
            "identifiers": ["your_identifier"],
            "name": "Device Name",
            "sw_version": "Software Version",
            "manufacturer": "Manufacturer",
            "model": "Model",
            "via_device": "Associated Device"
        }
    }
}
```

Replace the placeholders (e.g., `Your Door Name`, `GPIO_pin_number`, etc.) with your specific door sensor details.

### Environment Variables

Set the following environment variables in your Docker environment:

```bash
# Unique identifier for your device
DEVICE_ID=jn008
# Logging configuration DEBUG, INFO, WARNING, ERROR, or CRITICAL
LOG_LEVEL = DEBUG
# Specify platform as 'jetson' or 'rpi'
PLATFORM = 'Jetson'
# Address of the remote MQTT broker
MQTT_SERVER=your_server_hostname
# Username for authentication on the remote MQTT broker
MQTT_USERNAME=your_username
# Password for authentication on the remote MQTT broker
MQTT_PASSWORD=your_strong_password
```

Replace `your_server_hostname`, `your_username`, and `your_strong_password` with your MQTT broker details.

## Deployment

1. Clone the repository and navigate to the project directory.
2. Update the `config/ha_topics.json` file with your door sensor configurations.
3. Set the environment variables as per your MQTT broker settings.
4. Choose one of the following Docker deployment options.


### Docker Deployment - Standalone

The system can be deployed as a Docker container, and the `docker-compose.yaml` file in the root directory can be used to build and run the container. The `Dockerfile` in the `build` directory is used to build the container image.

```bash
docker-compose up -d --build
```

### Docker Deployment - As a Plugin

Copy the contents of `docker-compose.override.yaml` file in the same file within the root directory of your Edge Project to extend your plugins into the `docker-compose.yaml` file. This is useful for adding additional services to the container, such as Temperature/Humidity sensors or other devices.

```yaml
version: '3.8'
services:
  door_sensors:
    extends:
      file: ./plugins/edge_door_sensors/docker-compose.yaml
      service: door_sensors
```

```bash
docker-compose -f docker-compose.yaml -f docker-compose.override.yaml up -d --build
```

## Contributing

Contributions to the Door Sensor System are welcome. Please ensure your code adheres to the principles of Agile Development, follows Python best practices, and includes appropriate tests.

[LICENSE](./LICENSE)

## Acknowledgments

Special thanks to the contributors and the open-source community for making projects like this possible.