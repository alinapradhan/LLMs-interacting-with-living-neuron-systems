"""Flask server for the demo-only hybrid AI + living neuron simulation."""

from __future__ import annotations

from flask import Flask, jsonify, request, send_from_directory

from .closed_loop import ClosedCognitiveLoop

app = Flask(__name__, static_folder="../static", static_url_path="/static")
loop = ClosedCognitiveLoop()


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/api/state")
def get_state():
    return jsonify(loop.get_snapshot())


@app.post("/api/control")
def control():
    action = request.json.get("action", "").lower()
    if action == "start":
        loop.start()
    elif action == "pause":
        loop.pause()
    elif action == "reset":
        loop.reset()
    return jsonify({"ok": True, "running": loop.get_snapshot()["running"]})


@app.post("/api/brain_state")
def set_brain_state():
    state = request.json.get("state", "")
    loop.set_brain_state(state)
    return jsonify({"ok": True, "state": state})


@app.get("/api/replay")
def replay():
    return jsonify({"frames": loop.replay()})


@app.post("/api/auto_mode")
def auto_mode():
    """Optional auto simulation mode by cycling states quickly."""
    # For simplicity, this toggles to start; frontend handles rotating states.
    loop.start()
    return jsonify({"ok": True})


if __name__ == "__main__":
    print("Starting demo at http://127.0.0.1:8000")
    app.run(host="127.0.0.1", port=8000, debug=True)
