from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
import eventlet
eventlet.monkey_patch()

#################################################
# app.py - flask server to display both streams
# 
################################################

# flag for using fake data stream - for testing
USE_MOCK_DATA = True

if USE_MOCK_DATA:
    from mock_clients import stream_gsr, stream_eeg
else:
    from gsr_client import stream_gsr
    from eeg_client import stream_eeg

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    threading.Thread(target=stream_gsr, args=(socketio,), daemon=True).start()
    threading.Thread(target=stream_eeg, args=(socketio,), daemon=True).start()
    socketio.run(app, host="0.0.0.0", port=5000)
