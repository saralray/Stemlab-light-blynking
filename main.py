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

# ================== HOME ASSISTANT CALL ==================
def call_service(service, payload):
    url = f"{HA_URL}/api/services/light/{service}"
    try:
        r = requests.post(url, json=payload, headers=HEADERS, timeout=5)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] HA service failed: {e}")

# ================== BASIC BLINK ==================
def blink_light(entity_id, cycles=3, delay=0.3):
    for _ in range(cycles):
        call_service("turn_on", {"entity_id": entity_id})
        time.sleep(delay)
        call_service("turn_off", {"entity_id": entity_id})
        time.sleep(delay)

# ================== CHAOS PATTERN ==================
def chaos_blink(lights, rounds=20):
    for _ in range(rounds):
        count = random.randint(1, len(lights))
        selected = random.sample(lights, count)

        threads = []

        for light in selected:
            cycles = random.randint(1, 4)
            delay = random.uniform(0.1, 0.5)

            t = threading.Thread(
                target=blink_light,
                args=(light["entity_id"], cycles, delay),
                daemon=True
            )
            t.start()
            threads.append(t)

        # บางรอบรอ บางรอบไม่รอ (chaos จริง)
        if random.random() > 0.4:
            for t in threads:
                t.join()

        time.sleep(random.uniform(0.05, 0.6))

# ================== MAIN ==================
def main():
    lights = load_lights()
    print(f"🔥 Loaded {len(lights)} lights")

    if not lights:
        raise RuntimeError("No lights found in list.json")

    try:
        while True:
            print("💥 CHAOS MODE 💥")
            chaos_blink(
                lights,
                rounds=random.randint(15, 40)
            )
            time.sleep(random.uniform(1, 3))

    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")

# ================== RUN ==================
if __name__ == "__main__":
    main()
