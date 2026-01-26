from flask import Flask, jsonify, request, send_from_directory
import subprocess
import signal
import os

app = Flask(__name__, static_folder="static")

process = None
current_preset = None
PRESET_DIR = "presets"

# ---------------- SERVE UI ----------------
@app.route("/")
def index():
    return send_from_directory("static", "index.html")

# ---------------- API ----------------
@app.route("/presets")
def list_presets():
    presets = [
        f.replace(".py", "")
        for f in os.listdir(PRESET_DIR)
        if f.endswith(".py")
    ]
    print("📦 Presets:", presets)  # DEBUG
    return jsonify(presets)

@app.route("/start", methods=["POST"])
def start():
    global process, current_preset

    preset = request.json.get("preset")
    preset_path = os.path.join(PRESET_DIR, f"{preset}.py")

    if not os.path.exists(preset_path):
        return jsonify(error="Preset not found"), 404

    if process:
        process.send_signal(signal.SIGINT)
        process.wait(timeout=5)

    process = subprocess.Popen(["python3", preset_path])
    current_preset = preset

    return jsonify(status="running", preset=preset)

@app.route("/stop", methods=["POST"])
def stop():
    global process, current_preset

    if process:
        process.send_signal(signal.SIGINT)
        process.wait(timeout=5)
        process = None
        current_preset = None

    return jsonify(status="stopped")

@app.route("/status")
def status():
    return jsonify(
        running=process is not None,
        preset=current_preset
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
