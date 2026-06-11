from flask import Flask, render_template, jsonify
from flask_cors import CORS
from gpiozero import DigitalInputDevice
import requests
import time
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# ---------------- CONFIG ----------------

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

SENSOR_GPIO = 27

# If the app says LOW when sensor is wet, change this to False
WET_STATE_IS_HIGH = True

# Debounce settings
STABLE_READINGS_REQUIRED = 3
READ_DELAY_SECONDS = 0.2

last_confirmed_state = None

# ---------------- SENSOR SETUP ----------------

sensor = DigitalInputDevice(
    SENSOR_GPIO,
    pull_up=True,
    bounce_time=0.2
)


def raw_sensor_value():
    return sensor.value


def is_water_detected_once():
    value = raw_sensor_value()

    if WET_STATE_IS_HIGH:
        return value == 1
    else:
        return value == 0


def get_stable_water_state():
    readings = []

    for _ in range(STABLE_READINGS_REQUIRED):
        readings.append(is_water_detected_once())
        time.sleep(READ_DELAY_SECONDS)

    wet_count = readings.count(True)
    dry_count = readings.count(False)

    return wet_count > dry_count


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(url, data=payload, timeout=10)
        print(response.status_code)
        print(response.text)
        response.raise_for_status()
        return True

    except requests.RequestException as error:
        print("Telegram message failed:", error)
        return False


def build_message(water_detected):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if water_detected:
        return (
            "✅ Water Level OK\n\n"
            "Water is now detected by the sensor.\n"
            "The refrigerator water container is above the 10% limit.\n\n"
            "You can disregard previous low-water alerts.\n\n"
            f"Time: {current_time}"
        )
    else:
        return (
            "⚠️ Low Water Alert\n\n"
            "No water is detected by the sensor.\n"
            "The refrigerator water container is below the 10% limit.\n\n"
            "Please refill the container.\n\n"
            f"Time: {current_time}"
        )


def get_current_data():
    global last_confirmed_state

    water_detected = get_stable_water_state()
    alert_sent = False

    # Send message only when the state changes
    if last_confirmed_state is None:
        last_confirmed_state = water_detected

    elif water_detected != last_confirmed_state:
        message = build_message(water_detected)
        alert_sent = send_telegram_message(message)
        last_confirmed_state = water_detected

    if water_detected:
        status = "OK"
        message = "Water is detected. Level is above the 10% limit."
    else:
        status = "LOW"
        message = "No water detected. Level is below the 10% limit."

    return {
        "sensor_gpio": SENSOR_GPIO,
        "sensor_value": raw_sensor_value(),
        "water_detected": water_detected,
        "status": status,
        "message": message,
        "alert_sent": alert_sent,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/status")
def api_status():
    return jsonify(get_current_data())


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False
    )