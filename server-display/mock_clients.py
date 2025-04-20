# mock_clients.py
# for providing mock data to the server
import time
import random
from datetime import datetime
from cog_states import classify_state # so i can test the cog-state funcs

BUFFER_SIZE = 250
STATE_INTERVAL = 1.0  # seconds
last_state_time = time.time()
eeg_buffer = {i: [] for i in range(8)}

def stream_gsr(socketio):
    while True:
        fake_val = round(random.uniform(0.4, 0.8), 3)
        socketio.emit('gsr_data', {
            'timestamp': datetime.utcnow().isoformat(),
            'value': fake_val
        })
        time.sleep(0.05)

def stream_eeg(socketio):
    global last_state_time
    while True:
        #fake_sample = [round(random.uniform(-10, 10), 2) for _ in range(8)]
        # want to simulate different states instead of pure random
        current_time = time.time() % 40

        if current_time < 10: # 0-10 relaxed
            # Simulate Relaxed → dominant alpha
            fake_sample = [random.gauss(10, 2) for _ in range(8)]
        elif current_time < 20: # 10-20 focused
            # Simulate Focused → dominant beta
            fake_sample = [random.gauss(30, 8) for _ in range(8)]
        elif current_time < 30: # 20-30 CL
            # Simulate Cognitive Load → high theta, noisy
            fake_sample = [random.gauss(0, 20) for _ in range(8)]
        else: # 30-40 drowsyi
            # Simulate Drowsy → flat, slow signal
            fake_sample = [random.gauss(-5, 1) for _ in range(8)]


        # fill buffer
        for i in range(8):
            eeg_buffer[i].append(fake_sample[i])
            if len(eeg_buffer[i]) > BUFFER_SIZE:
                eeg_buffer[i].pop(0)

        # Emit EEG data (channel 1)
        socketio.emit('eeg_data', {
            'timestamp': datetime.utcnow().isoformat(),
            'data': fake_sample
        })

        # classify every second
        if time.time() - last_state_time > STATE_INTERVAL:
            state = classify_state(eeg_buffer)
            socketio.emit('cognitive_state', {
                'timestamp': datetime.utcnow().isoformat(),
                'state': state
            })
            last_state_time = time.time()

        time.sleep(0.004)
