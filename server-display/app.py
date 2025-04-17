from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
import eventlet
eventlet.monkey_patch()

#################################################
# app.py - flask server to display both streams
################################################

from config import USE_MOCK_EEG, USE_MOCK_GSR  # import flags from config
# can toggle both eeg and gsr separately 

if USE_MOCK_GSR:
    from mock_clients import stream_gsr
else:
    from gsr_client import stream_gsr

if USE_MOCK_EEG:
    from mock_clients import stream_eeg
else:
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
