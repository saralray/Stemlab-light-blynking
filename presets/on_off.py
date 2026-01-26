import json
import os
import time
import requests
from dotenv import load_dotenv

# ================== CONFIG ==================
load_dotenv()

HA_URL = os.getenv("HA_URL")
HA_TOKEN = os.getenv("HA_TOKEN")

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

# ================== MAIN ==================
def main():
    lights = load_lights()
    print(f"💡 ON/OFF preset loaded ({len(lights)} lights)")

    # TURN ON
    call_service("turn_on", {
        "entity_id": lights
    })
    print("✅ Lights ON")

    try:
        # Stay alive until stopped
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        # TURN OFF
        call_service("turn_off", {
            "entity_id": lights
        })
        print("🛑 Lights OFF")

# ================== RUN ==================
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

