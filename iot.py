import json
import time
import random
import paho.mqtt.client as mqtt
from datetime import datetime

# MQTT broker configuration
BROKER_HOST = "127.0.0.1"  # Use "broker.hivemq.com" for public broker
BROKER_PORT = 1883
TOPIC = "restroom/sensor_data"

# Sensor simulation configuration
SENSORS = [
    {"sensor_id": 1, "sensor_name": "dustbin"},
    {"sensor_id": 2, "sensor_name": "soap_dispenser"},
    {"sensor_id": 3, "sensor_name": "paper_towel_1"},
    {"sensor_id": 4, "sensor_name": "paper_towel_2"},
    {"sensor_id": 5, "sensor_name": "paper_towel_3"},
    {"sensor_id": 6, "sensor_name": "people_count_1"},
    {"sensor_id": 7, "sensor_name": "people_count_2"},
    {"sensor_id": 8, "sensor_name": "people_count_3"},
    {"sensor_id": 9, "sensor_name": "people_count_4"},
]

# Simulate sensor data
def generate_sensor_data(sensor):
    """Generate random data for a given sensor."""
    if "dustbin" in sensor["sensor_name"]:
        return {"level": random.randint(0, 100)}  # Dustbin level (0-100%)
    elif "soap_dispenser" in sensor["sensor_name"]:
        return {"level": random.randint(0, 100)}  # Soap level (0-100%)
    elif "paper_towel" in sensor["sensor_name"]:
        return {"level": random.randint(0, 100)}  # Paper towel level (0-100%)
    elif "people_count" in sensor["sensor_name"]:
        return {"count": random.randint(0, 50)}  # People count (0-50)
    else:
        return {}

# Publish data to MQTT broker
def publish_sensor_data(client):
    while True:
        for sensor in SENSORS:
            sensor_data = {
                "sensor_id": sensor["sensor_id"],
                "sensor_name": sensor["sensor_name"],
                "data": generate_sensor_data(sensor),
                "timestamp": datetime.now().isoformat(),
            }
            message = json.dumps(sensor_data)
            client.publish(TOPIC, message)
            print(f"Published: {message}")
        time.sleep(60)  # Send data every 1 minute

# MQTT connection callback
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

# Main function
def main():
    # Create MQTT client
    client = mqtt.Client()
    client.on_connect = on_connect

    # Connect to MQTT broker
    client.connect(BROKER_HOST, BROKER_PORT, 60)

    # Start publishing sensor data
    try:
        publish_sensor_data(client)
    except KeyboardInterrupt:
        print("Simulation stopped.")
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()