# Home Assistant MQTT Door Sensor Integration

This application facilitates the integration of door sensors with Home Assistant via MQTT using the Mosquitto broker.

## Directory Structure

```
.
├── .env                     # Environment variable file
├── docker-compose.yaml      # Docker Compose file for orchestrating services
├── README.md                # Documentation file
├── mosquitto/               # Mosquitto related files and configurations
│   ├── entrypoint.sh        # Script to setup and start the Mosquitto service
│   ├── log/                 # Logs related to the Mosquitto service
│   ├── config/              # Configuration files for Mosquitto
│   └── data/                # Data files for Mosquitto
├── build/                   # Build related files
│   ├── Dockerfile           # Dockerfile for the application
│   └── requirements.txt     # Python dependencies
├── worker/                  # Application's main functionality
│   ├── door_sensor.py       # Door sensor processing module
│   └── worker.py            # Main worker logic
└── data/
    └── doors.json           # JSON file with door sensor configurations
```

## Getting Started

1. **Setup Environment Variables**

   Ensure you have the required environment variables set in the `.env` file:

   ```
   REMOTE_USERNAME=your_mqtt_username
   REMOTE_PASSWORD=your_mqtt_password
   REMOTE_SERVER=your_mqtt_server
   REMOTE_PORT=your_mqtt_port
   ```

2. **Docker Setup**

   Use Docker Compose to set up and run the services:

   ```bash
   docker-compose up --build
   ```

   This will set up both the MQTT broker and the worker to process door sensor data.

3. **Logging**

   Check the `mosquitto/log/mosquitto.log` file for logs related to the Mosquitto service.

## Mosquitto Entrypoint

The `mosquitto/entrypoint.sh` script is used to copy and modify the Mosquitto configuration file based on provided environment variables. Once the config is modified, it then starts the Mosquitto service.

## Data Configuration

The `data/doors.json` file contains configurations for each door sensor, which the worker processes.

## Worker

The `worker/` directory contains the logic for processing door sensor data (`door_sensor.py`) and the main worker logic that interacts with the MQTT broker (`worker.py`).

## Contributing

Feel free to fork this project, submit PRs and report issues. For major changes, please open an issue first.

## License

This project is licensed under Apache License 2.0
