from pylsl import StreamInlet, resolve_streams
from datetime import datetime
import threading
import random
import json
import time
import csv

# G.TEC Unicorn 8-channel labels
channel_labels = ['FZ', 'C3', 'CZ', 'C4', 'PZ', 'PO7', 'OZ', 'PO8']

# Load config and check mock mode
with open("config/experiment_config.json", "r") as f:
    CONFIG = json.load(f)
MOCK_MODE = CONFIG.get("mock_mode", False)

# Recorder globals
recording = False
inlet = None
thread = None
writer = None
log_file = None

def start_recording(output_path, mock=False):
    global recording, inlet, thread, writer, log_file

    if recording:
        print(">Already recording!")
        return
    
    if mock:
       print(">MOCK MODE: Streaming fake EEG data.")
    else:
        print(">Resolving EEG LSL stream...")
        streams = resolve_streams()
        print("> Resolving stream.")
        inlet = StreamInlet(streams[0])
        print("> LSL stream found.")

    log_file = open(output_path, mode='w', newline='')
    writer = csv.writer(log_file)
    writer.writerow(['utc_timestamp', 'local_timestamp'] + channel_labels)

    recording = True
    thread = threading.Thread(target=_record_loop)
    thread.start()

def stop_recording():
    global recording, thread, log_file

    recording = False
    if thread is not None:
        thread.join()
    if log_file is not None:
        log_file.close()
    print("> Recording paused.")

def _record_loop():
    global recording, inlet, writer

    while recording:
        if MOCK_MODE:
            sample = [random.uniform(-40, 40) for _ in channel_labels]
            timestamp = time.time()
        else:
            sample, timestamp = inlet.pull_sample(timeout=1.0)
            if not sample:
                time.sleep(0.01)
                continue

        utc_time = datetime.utcnow().isoformat()
        local_time = datetime.now().isoformat()
        writer.writerow([utc_time, local_time] + sample[:len(channel_labels)])
