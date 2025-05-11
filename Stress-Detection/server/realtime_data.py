# real time data module
# read eeg data from lsl stream (or mock)
# simulate gsr
# generate mock stress/lie detection
# realtime_data.py

from pylsl import StreamInlet, resolve_byprop
import time, random
import os
import numpy as np
from scipy.signal import welch

USE_MOCK_EEG = True 
USE_MOCK_GSR = True

SAMPLE_RATE = 250  # Hz
WINDOW_DURATION = 1.0  # seconds
WINDOW_SIZE = int(SAMPLE_RATE * WINDOW_DURATION) 

def compute_bandpower(buffer, fs):
    # buffer: shape (WINDOW_SIZE, n_channels)
    bands = {
        'delta': (0.5, 4),
        'theta': (4, 8),
        'alpha': (8, 13),
        'beta':  (13, 30),
        'gamma': (30, 45)
    }
    bandpower = dict.fromkeys(bands, 0)

    # Average across all channels
    for ch in range(buffer.shape[1]):
        freqs, psd = welch(buffer[:, ch], fs=fs, nperseg=fs)

        for band in bands:
            low, high = bands[band]
            idx = np.logical_and(freqs >= low, freqs <= high)
            bandpower[band] += np.trapz(psd[idx], freqs[idx])

    # Normalize by number of channels
    for band in bandpower:
        bandpower[band] = round(bandpower[band] / buffer.shape[1], 3)

    return bandpower

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

        buffer = np.tile(np.array(eeg_data), (WINDOW_SIZE, 1))
        bandpower = compute_bandpower(buffer, SAMPLE_RATE)
        
        socketio.emit('bandpower_data', bandpower)

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

    eeg_buffer = np.zeros((WINDOW_SIZE, len(eeg_channels)))
    buffer_index = 0
    
    while True:
        sample, timestamp = inlet.pull_sample(timeout=0.0)
        if sample:# sample is a list of eeg vals - one per channel
            eeg_data = sample[:len(eeg_channels)]
            socketio.emit('eeg_data', {'data': eeg_data})
            
            eeg_buffer[buffer_index % WINDOW_SIZE] = eeg_data
            buffer_index += 1

            now = time.time()
            
            if buffer_index >= WINDOW_SIZE and (time.time() - last_stress_update >= 1.0):
                bandpower = compute_bandpower(eeg_buffer, SAMPLE_RATE)
                socketio.emit('bandpower_data', bandpower)

                # Send other mock stats
                gsr_value = round(random.uniform(0.01, 0.05), 4)
                stress_level = random.choice(['Low', 'Medium', 'High'])
                lie_status = random.choice(['Truth', 'Lie'])
    
                socketio.emit('gsr_data', {'value': gsr_value})
                socketio.emit('stress_detection', {'level': stress_level})
                socketio.emit('lie_detected', {'status': lie_status})

                last_stress_update = time.time()

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
