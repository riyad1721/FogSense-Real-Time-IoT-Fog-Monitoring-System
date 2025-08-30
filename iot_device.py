import paho.mqtt.client as mqtt
import random, time, json

BROKER = "localhost"
PORT = 1883
TOPIC = "iot/sensor"

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

def generate_data():
    return {
        "temperature": round(random.uniform(18, 45), 2),
        "humidity": round(random.uniform(30, 90), 2),
        "air_quality": round(random.uniform(10, 200), 2)  # AQI
    }

while True:
    data = generate_data()
    client.publish(TOPIC, json.dumps(data))
    print("IoT Device → Published:", data)
    time.sleep(1)
