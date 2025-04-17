# mock_clients.py
# for providing mock data to the server
import time
import random
from datetime import datetime

def stream_gsr(socketio):
    while True:
        fake_val = round(random.uniform(0.4, 0.8), 3)
        socketio.emit('gsr_data', {
            'timestamp': datetime.utcnow().isoformat(),
            'value': fake_val
        })
        time.sleep(0.05)

def stream_eeg(socketio):
    while True:
        fake_sample = [round(random.uniform(-50, 50), 2) for _ in range(8)]
        socketio.emit('eeg_data', {
            'timestamp': datetime.utcnow().isoformat(),
            'data': fake_sample
        })
        time.sleep(0.004)
