# 🌐 FogSense: Real-Time IoT Fog Monitoring System

FogSense is a **Fog Computing + IoT project** that demonstrates how raw IoT sensor data can be processed at the **edge (Fog Node)** before sending filtered insights to the **Cloud Dashboard**.  
It reduces latency, saves bandwidth, and enables anomaly detection in real-time.  

---

## 🚩 Problem Statement
IoT devices generate a huge volume of raw sensor data.  
Sending everything directly to the cloud increases:
- ❌ Latency  
- ❌ Network load  
- ❌ Processing cost  

✅ **Solution:** Use **Fog Computing**. Process data closer to the devices, filter anomalies, and send only meaningful insights to the cloud.  

---

## 🛠️ Technologies Used
- **Python** (core programming)  
- **MQTT (Eclipse Mosquitto + Paho-MQTT)** → for IoT → Fog → Cloud communication  
- **Flask** → for Cloud dashboard (Web UI + REST API)  
- **SQLite3** → for data storage at cloud  
- **Chart.js + Bootstrap 5** → for interactive graphs & UI  
- **Machine Learning (Z-score Anomaly Detection)** → detects abnormal temperature readings at the Fog Node  

---

## 📊 Project Architecture & Pipeline

```
 [IoT Device Simulator]
        |
        v
   (Publish MQTT)
        |
        v
 [Fog Node]
   - Receives IoT data
   - Filters abnormal values
   - Runs anomaly detection (Z-score)
   - Aggregates data
   - Sends processed data to cloud
        |
        v
 [Cloud Server + Dashboard]
   - Receives data via MQTT
   - Stores in SQLite DB
   - Serves real-time dashboard with graphs, anomaly logs, and system insights
```

---

## ⚙️ Setup & Run Instructions

### 1. Install Mosquitto MQTT Broker
#### 🔹 Windows
- Download installer: [https://mosquitto.org/download/](https://mosquitto.org/download/)  
- During installation: ✅ Add to PATH, ✅ Install Service  
- Start broker:
  ```powershell
  net start mosquitto
  ```
- Verify:
  ```powershell
  mosquitto -v
  ```

#### 🔹 Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install mosquitto mosquitto-clients -y
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
mosquitto -v
```

#### 🔹 macOS
```bash
brew install mosquitto
brew services start mosquitto
mosquitto -v
```

---

### 2. Clone the Project
```bash
git clone https://github.com/riyad1721/FogSense-Real-Time-IoT-Fog-Monitoring-System.git
cd FogSense
```

---

### 3. Create Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

---

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

### 5. Run the Project

#### 🔹 Step 1: Start Cloud Server
```bash
python cloud_server.py
```
Dashboard available at → [http://127.0.0.1:5000](http://127.0.0.1:5000)

#### 🔹 Step 2: Start Fog Node
```bash
python fog_node.py
```

#### 🔹 Step 3: Run IoT Device Simulator
(Open multiple terminals to simulate multiple IoT devices)
```bash
python iot_device.py
```

---

## 📺 Dashboard Features
- 📊 **Graphs** → Temperature, Humidity, and Air Quality (AQI)  
- ⚠ **Anomaly Detection** → real-time status + anomaly counter  
- 📋 **Anomaly Log** → last 10 detected anomalies with timestamps  
- 🌡 **Stats Cards** → average temp, average humidity, total anomalies, total data count  
- 🎯 **Project Purpose Section** → explains Fog Computing  
- 🖼 **Architecture Diagram Placeholder** → IoT → Fog → Cloud  

---

