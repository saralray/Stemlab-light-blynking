import json
import os
import time
import requests
import random
import threading
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

    return data["lights"]

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
        pass  # chaos mode: ignore errors

# ================== TURN OFF ALL ==================
def turn_off_all(lights):
    call_service("turn_off", {
        "entity_id": [l["entity_id"] for l in lights]
    })

# ================== PER-LIGHT CHAOS ==================
def light_chaos_worker(entity_id):
    while True:
        time.sleep(random.uniform(0.05, 0.6))
        mode = random.random()

        if mode < 0.5:
            call_service("turn_on", {"entity_id": entity_id})
            time.sleep(random.uniform(0.05, 0.2))
            call_service("turn_off", {"entity_id": entity_id})

        elif mode < 0.8:
            call_service("turn_on", {
                "entity_id": entity_id,
                "flash": "short"
            })

        else:
            call_service("turn_on", {"entity_id": entity_id})
            time.sleep(random.uniform(0.2, 0.8))
            call_service("turn_off", {"entity_id": entity_id})

# ================== MAIN ==================
def main():
    lights = load_lights()
    print(f"🔥 Loaded {len(lights)} lights")
    print("💣 TRUE CHAOS MODE (independent lights) 💣")

    for light in lights:
        threading.Thread(
            target=light_chaos_worker,
            args=(light["entity_id"],),
            daemon=True
        ).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping chaos...")
        turn_off_all(lights)
        print("💤 All lights OFF")

# ================== RUN ==================
if __name__ == "__main__":
    main()
