### app.py
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import threading
from server.realtime_data import start_streaming_eeg, start_streaming_gsr
import json
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

@app.route('/')
def index():
    return render_template("index.html")

# arduino endpoint
from datetime import datetime

@app.route("/update", methods=["POST"])
def update_from_arduino():
    data = request.get_json()
    if "gsr" in data:
        try:
            val_read = int(data["gsr"])
            #if val_read >= 512:  # Avoid division by zero or negative resistance
            #    return jsonify({"status": "error", "reason": "invalid sensor value"}), 400

            resistance = (1024 + (2 * val_read)) * (1 / (512 - val_read))
            val_res = (1 / resistance) * 100

            socketio.emit("gsr_data", { "value": val_res })
        
        except (ValueError, ZeroDivisionError) as e:
            return jsonify({"status": "error", "reason": str(e)}), 400

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
