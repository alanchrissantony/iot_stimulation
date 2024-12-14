import json
import random
import time
import paho.mqtt.client as mqtt
from datetime import datetime

# MQTT Broker Configuration
MQTT_BROKER = "localhost"  # Change this to your broker's address
MQTT_PORT = 1883
MQTT_TOPIC = "restroom/sensor_data"

# Function to simulate sensor data
def generate_sensor_data(sensor_id, sensor_name, data_key, min_val, max_val):
    return {
        "sensor_id": sensor_id,
        "sensor_name": sensor_name,
        "data": {
            data_key: random.randint(min_val, max_val)
        },
        "timestamp": datetime.now().isoformat()
    }

# Function to simulate publishing sensor data
def simulate_sensor_publishing(client):
    while True:
        # Simulate dustbin level
        dustbin_data = generate_sensor_data(1, "dustbin", "level", 0, 100)
        client.publish(MQTT_TOPIC, json.dumps(dustbin_data))

        # Simulate soap dispenser level
        soap_data = generate_sensor_data(2, "soap_dispenser", "level", 0, 100)
        client.publish(MQTT_TOPIC, json.dumps(soap_data))

        # Simulate paper towel sensors
        for i in range(3):  # Assume 3 paper towel sensors
            paper_towel_data = generate_sensor_data(3 + i, f"paper_towel_{i+1}", "level", 0, 100)
            client.publish(MQTT_TOPIC, json.dumps(paper_towel_data))

        # Simulate people count sensors
        for i in range(4):  # Assume 4 people count sensors
            people_count_data = generate_sensor_data(6 + i, f"people_count_{i+1}", "count", 0, 50)
            client.publish(MQTT_TOPIC, json.dumps(people_count_data))

        # Wait for 1 minute before sending the next batch
        print(f"Published a batch of sensor data at {datetime.now().isoformat()}")
        time.sleep(60)

# MQTT Connection Setup
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

def main():
    # Create MQTT client
    client = mqtt.Client()
    client.on_connect = on_connect

    # Connect to the broker
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    # Start the simulation
    simulate_sensor_publishing(client)

if __name__ == "__main__":
    main()