#################################################
# app.py - flask server to display both streams
################################################

from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
import time
import os


CARD_IMAGE_DIR = os.path.join(os.path.dirname(__file__),'static', 'cards')
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

print("🔧 Starting app.py...")
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

dealer_cards = []

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print("🔌 Client connected — sending dealer cards")
    for code in dealer_cards:
        socketio.emit('dealer_card', {'code': code})

def run_server():
    print("🟢 Flask-SocketIO server is about to start")
    socketio.run(app, host="0.0.0.0", port=5000)

import sys
import select

def dealer_input():
    global dealer_cards
    while True:
        msg = input("🃏 Enter card code(s): ").strip().upper()
        codes = msg.split()

        for code in codes:
            file_path = os.path.join(CARD_IMAGE_DIR, f"{code}.png")
            if not os.path.exists(file_path):
                print(f"❌ Card image for '{code}' not found. Skipping.")
                continue

            if len(dealer_cards) >= 5:
                dealer_cards = []

            dealer_cards.append(code)
            socketio.emit('dealer_card', {'code': code})
        time.sleep(0.01)

if __name__ == "__main__":
    threading.Thread(target=stream_gsr, args=(socketio,), daemon=True).start()
    threading.Thread(target=stream_eeg, args=(socketio,), daemon=True).start()
    threading.Thread(target=dealer_input, daemon=True).start()
    threading.Thread(target=run_server, daemon=True).start()
    while True:
        time.sleep(1)

