from flask import Flask, jsonify, render_template
import paho.mqtt.client as mqtt
import json, sqlite3, statistics

BROKER = "localhost"
PORT = 1883
TOPIC = "fog/processed"

app = Flask(__name__)

# Database setup
conn = sqlite3.connect("cloud_data.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperature REAL,
    humidity REAL,
    air_quality REAL,
    anomaly INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    print("Cloud ← Received:", data)

    cursor.execute(
        "INSERT INTO sensor_data (temperature, humidity, air_quality, anomaly) VALUES (?, ?, ?, ?)",
        (data["temperature"], data["humidity"], data["air_quality"], int(data["anomaly"]))
    )
    conn.commit()

mqtt_client = mqtt.Client()
mqtt_client.connect(BROKER, PORT, 60)
mqtt_client.subscribe(TOPIC)
mqtt_client.on_message = on_message
mqtt_client.loop_start()

@app.route("/data")
def get_data():
    cursor.execute("SELECT * FROM sensor_data ORDER BY id DESC LIMIT 50")
    rows = cursor.fetchall()
    return jsonify(rows)

@app.route("/stats")
def get_stats():
    # Calculate averages from last 50 rows
    cursor.execute("SELECT temperature, humidity FROM sensor_data ORDER BY id DESC LIMIT 50")
    rows = cursor.fetchall()
    if not rows:
        return jsonify({"avg_temp": 0, "avg_hum": 0, "count": 0, "anomalies": 0})

    temps = [r[0] for r in rows]
    hums = [r[1] for r in rows]

    # Count all anomalies in DB
    cursor.execute("SELECT COUNT(*) FROM sensor_data WHERE anomaly=1")
    anomaly_count = cursor.fetchone()[0]

    # Count all rows in DB
    cursor.execute("SELECT COUNT(*) FROM sensor_data")
    total_count = cursor.fetchone()[0]

    return jsonify({
        "avg_temp": round(statistics.mean(temps), 2),
        "avg_hum": round(statistics.mean(hums), 2),
        "count": total_count,
        "anomalies": anomaly_count
    })

@app.route("/anomalies")
def anomaly_log():
    cursor.execute("SELECT timestamp, temperature, humidity, air_quality, anomaly FROM sensor_data WHERE anomaly=1 ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    return jsonify(rows)

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
