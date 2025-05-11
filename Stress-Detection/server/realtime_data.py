# real time data module
# read eeg data from lsl stream (or mock)
# simulate gsr
# generate mock stress/lie detection
# realtime_data.py

from pylsl import StreamInlet, resolve_byprop
import time, random
import os

USE_MOCK_EEG = False 
USE_MOCK_GSR = True

def stream_mock_data(socketio, eeg_channels):
    print("[EEG] Using MOCK EEG data")
    while True:
        eeg_data = [round(random.uniform(-40, 40), 2) for _ in eeg_channels]
        gsr_value = round(random.uniform(0.01, 0.05), 4)
        stress_level = random.choice(['Low', 'Medium', 'High'])
        lie_status = random.choice(['Truth', 'Lie'])

        socketio.emit('eeg_data', {'data': eeg_data})
        socketio.emit('gsr_data', {'value': gsr_value})
        socketio.emit('stress_detection', {'level': stress_level})
        socketio.emit('lie_detected', {'status': lie_status})
        time.sleep(0.1)

def stream_real_eeg(socketio, eeg_channels):
    print("[EEG] Looking for real EEG stream...")
    streams = resolve_byprop('type', 'Data', timeout=10)
    if not streams:
        print("[EEG] No EEG stream found.")
        return

    inlet = StreamInlet(streams[0])
    print("[EEG] EEG stream found. Streaming...")

    last_stress_update = time.time()

    while True:
        sample, timestamp = inlet.pull_sample(timeout=0.0)
        if sample:
            eeg_data = sample[:len(eeg_channels)]
            socketio.emit('eeg_data', {'data': eeg_data})

            now = time.time()
            if now - last_stress_update >= 1.0:
                gsr_value = round(random.uniform(0.01, 0.05), 4)
                stress_level = random.choice(['Low', 'Medium', 'High'])
                lie_status = random.choice(['Truth', 'Lie'])

                socketio.emit('gsr_data', {'value': gsr_value})
                socketio.emit('stress_detection', {'level': stress_level})
                socketio.emit('lie_detected', {'status': lie_status})
                
                last_stress_update = now

from threading import Thread
from server.gsr_stream import stream_gsr

def start_streaming(socketio):
    # Start GSR in background thread
    gsr_thread = Thread(target=stream_gsr, args=(socketio,), daemon=True)
    gsr_thread.start()

    eeg_channels = ['AF3', 'AF4', 'F3', 'F4', 'T7', 'T8', 'P7', 'P8']
    if USE_MOCK_EEG:
        stream_mock_data(socketio, eeg_channels)
    else:
        stream_real_eeg(socketio, eeg_channels)
