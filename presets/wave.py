import json
import os
import time
import requests
from dotenv import load_dotenv

# ================== CONFIG ==================
load_dotenv()

HA_URL = os.getenv("HA_URL")
HA_TOKEN = os.getenv("HA_TOKEN")

# Wave timing (seconds)
WAVE_DELAY = float(os.getenv("WAVE_DELAY", "0.15"))
HOLD_TIME  = float(os.getenv("WAVE_HOLD", "0.3"))

HEADERS = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json",
}

# ================== LOAD LIGHTS ==================
def load_lights():
    with open("list.json", "r") as f:
        data = json.load(f)

    if "lights" not in data or not isinstance(data["lights"], list):
        raise ValueError("list.json must contain a 'lights' list")

    return [l["entity_id"] for l in data["lights"]]

# ================== HA CALL ==================
def call_service(service, payload):
    try:
        requests.post(
            f"{HA_URL}/api/services/light/{service}",
            json=payload,
            headers=HEADERS,
            timeout=2
        )
    except Exception:
        pass

# ================== TURN OFF ALL ==================
def turn_off_all(lights):
    call_service("turn_off", {
        "entity_id": lights
    })

# ================== MAIN ==================
def main():
    lights = load_lights()
    print(f"🌊 Wave preset loaded ({len(lights)} lights)")

    try:
        while True:
            # ---- WAVE ON ----
            for entity_id in lights:
                call_service("turn_on", {"entity_id": entity_id})
                time.sleep(WAVE_DELAY)

            time.sleep(HOLD_TIME)

            # ---- WAVE OFF ----
            for entity_id in lights:
                call_service("turn_off", {"entity_id": entity_id})
                time.sleep(WAVE_DELAY)

            time.sleep(HOLD_TIME)

    except KeyboardInterrupt:
        print("\n🛑 Stopping wave...")
        turn_off_all(lights)
        print("💤 All lights OFF")

# ================== RUN ==================
if __name__ == "__main__":
    main()
