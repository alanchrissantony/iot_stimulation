import json
import paho.mqtt.client as mqtt

# MQTT Broker Configuration
MQTT_BROKER = "localhost"  # Change this to your broker's address
MQTT_PORT = 1883
MQTT_TOPIC = "restroom/sensor_data"

# MQTT Callback for when a message is received
def on_message(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode())
        print(f"Received message on topic {message.topic}:")
        print(json.dumps(payload, indent=4))
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")

# MQTT Connection Setup
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(MQTT_TOPIC)  # Subscribe to the topic
    else:
        print(f"Failed to connect, return code {rc}")

def main():
    # Create MQTT client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the broker
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    # Start listening for messages
    client.loop_forever()

if __name__ == "__main__":
    main()