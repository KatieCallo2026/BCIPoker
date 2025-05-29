### app.py
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import threading
from server.realtime_data import start_streaming_eeg, start_streaming_gsr
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

@app.route('/')
def index():
    return render_template("index.html")

# arduino endpoint
@app.route("/update", methods=["POST"])
def update_from_arduino():
    data = request.get_json()
    #print("Arduino sent:", data)
    if "gsr" in data:
        socketio.emit("gsr_data", {"value": data["gsr"]})

    return jsonify({"status": "success"})

@socketio.on('connect')
def test_connect():
    print("Client connected")

def run_server():
    with open("config/experiment_config.json") as f:
        CONFIG = json.load(f)

    threading.Thread(target=start_streaming_eeg, args=(socketio,), daemon=True).start()
    threading.Thread(target=start_streaming_gsr, args=(socketio,), daemon=True).start()
    
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)

if __name__ == '__main__':
    run_server()
