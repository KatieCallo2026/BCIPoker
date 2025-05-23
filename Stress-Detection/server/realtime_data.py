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

import joblib
from pathlib import Path
import json
from scripts.predict_live import predict_from_window

USE_MOCK_EEG = True 
USE_MOCK_GSR = True

SAMPLE_RATE = 250  # Hz
WINDOW_DURATION = 1.0  # seconds
WINDOW_SIZE = int(SAMPLE_RATE * WINDOW_DURATION) 

with open("config/experiment_config.json") as f:
    CONFIG = json.load(f)

MODEL_PATH = Path("data") / "stress_model_all.pkl"

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
    eeg_buffer = np.zeros((WINDOW_SIZE, len(eeg_channels)))
    buffer_index = 0
    last_stress_update = time.time()

    while True:
        new_sample = np.random.normal(loc=0, scale=20, size=len(eeg_channels))
        eeg_data = new_sample.tolist()
        eeg_buffer = np.roll(eeg_buffer, -1, axis=0)
        eeg_buffer[-1] = new_sample
        buffer_index += 1

        gsr_value = round(random.uniform(0.01, 0.05), 4)
        lie_status = random.choice(['Truth', 'Lie'])
        bandpower = compute_bandpower(eeg_buffer, SAMPLE_RATE)

        predicted_value = None
        stress_level = "Unknown"
        now = time.time()

        # Predict every 3 seconds once enough buffer is filled
        if buffer_index >= WINDOW_SIZE and (now - last_stress_update >= 1.0):
            try:
                print("[DEBUG] EEG buffer STD per channel:", np.std(eeg_buffer, axis=0))
                predicted_value = predict_from_window(
                    eeg_buffer.copy(),
                    fs=SAMPLE_RATE,
                    config=CONFIG,
                    model_path=MODEL_PATH
                )

                print(f"[PREDICT] Stress value: {predicted_value}")

            except Exception as e:
                print(f"[EEG] Prediction error: {e}")
                predicted_value = None

            last_stress_update = now

        # Emit data to client
        socketio.emit('eeg_data', {'data': eeg_data})
        socketio.emit('gsr_data', {'value': gsr_value})
        socketio.emit('bandpower_data', bandpower)
        socketio.emit('lie_detected', {'status': lie_status})
        if predicted_value is not None:
            socketio.emit('stress_detection', {'value': predicted_value})

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
            print("[DEBUG] Sample:", sample)
            print("[DEBUG] Sample length:", len(sample))
    
            eeg_data = sample[:len(eeg_channels)]
            socketio.emit('eeg_data', {'data': eeg_data})
            
            eeg_buffer = np.roll(eeg_buffer, -1, axis=0)
            eeg_buffer[-1] = eeg_data
            buffer_index += 1

            now = time.time()
            
            if buffer_index >= WINDOW_SIZE and (time.time() - last_stress_update >= 2.0):

                # Send other mock stats
                gsr_value = round(random.uniform(0.01, 0.05), 4)
                #stress_level = random.choice(['Low', 'Medium', 'High'])
                lie_status = random.choice(['Truth', 'Lie'])
                bandpower = compute_bandpower(eeg_buffer, SAMPLE_RATE)
    
                # Predict stress level using the model
                # Run model prediction
                try:
                    print("[DEBUG] EEG buffer STD per channel:", np.std(eeg_buffer, axis=0))
                    predicted_value = predict_from_window(
                        eeg_buffer.copy(),  # (500, 8)
                        fs=SAMPLE_RATE,
                        config=CONFIG,
                        model_path=MODEL_PATH
                    )

                    # Map predicted value to label
                    if predicted_value < 1.5:
                        stress_level = "Low"
                    elif predicted_value < 2.5:
                        stress_level = "Medium"
                    else:
                        stress_level = "High"

                except Exception as e:
                    print(f"[EEG] Prediction error: {e}")
                    stress_level = "Unknown"

                # Send biometric data to the client
                print(f"[PREDICT] Stress value: {predicted_value}")
                socketio.emit('stress_detection', {'value': predicted_value})
                socketio.emit('bandpower_data', bandpower)

                # TODO: real
                socketio.emit('gsr_data', {'value': gsr_value})
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
