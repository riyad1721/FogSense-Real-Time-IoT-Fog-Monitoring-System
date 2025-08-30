import paho.mqtt.client as mqtt
import json, statistics

BROKER = "localhost"
PORT = 1883
SUB_TOPIC = "iot/sensor"
PUB_TOPIC = "fog/processed"

window = []  # rolling window for data

def detect_anomaly(value, mean, std):
    """Simple anomaly detection using Z-score"""
    if std == 0: return False
    z = (value - mean) / std
    return abs(z) > 2  # anomaly if z-score > 2

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    print("Fog Node ← Received:", data)

    window.append(data["temperature"])
    if len(window) > 20:
        window.pop(0)

    mean = statistics.mean(window)
    std = statistics.pstdev(window)

    data["anomaly"] = detect_anomaly(data["temperature"], mean, std)

    # Local filtering
    if data["anomaly"]:
        print("⚠ Anomaly Detected:", data)

    # Forward processed data
    client.publish(PUB_TOPIC, json.dumps(data))
    print("Fog Node → Sent to Cloud:", data)

# client = mqtt.Client()
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.connect(BROKER, PORT, 60)
client.subscribe(SUB_TOPIC)
client.on_message = on_message

print("Fog Node running...")
client.loop_forever()
