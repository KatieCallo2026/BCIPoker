from pylsl import StreamInlet, resolve_stream
from datetime import datetime
import time
import csv
import os
from cog_states import classify_state
from config import EEG_BUFFER_SIZE, EEG_STATE_INTERVAL

print("📦 eeg_client.py imported")

##################################################
# eeg_client.py - GSR data stream
# now has cognitive state logic
##################################################

# expected channels from unicorn headset
channel_labels = ['FZ', 'C3', 'CZ', 'C4', 'PZ', 'PO7', 'OZ', 'PO8']
# set up circular buffer with channel labels
eeg_buffer = {label: [] for label in channel_labels}
last_state_time = time.time()

def stream_eeg(socketio):
    print("🔍 Resolving LSL stream...")
    global last_state_time

    inlet = None 
    try:
        streams = resolve_stream()
        inlet = StreamInlet(streams[0])
        print("✅ LSL stream found!")
    except IndexError:
        print("❌ No LSL stream found...")
        return

    has_received_data = False 
    stream_start_time = time.time()

    # Prepare logging directory and file
    filename = f"eeg_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    log_path = os.path.join("logs", filename)
    os.makedirs("logs", exist_ok=True)

    with open(log_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Include both UTC and local timestamps in header
        writer.writerow(['utc_timestamp', 'local_timestamp'] + channel_labels)
        print(f"Logging EEG data to {log_path}")

        while True:
            sample, timestamp = inlet.pull_sample(timeout=0.0)
            if not sample:
                if not has_received_data and time.time() - stream_start_time > 3:
                    print("⚠️  EEG stream open but no data received. It might not be started.")
                    stream_start_time = float('inf')
                time.sleep(0.001)
                continue

            has_received_data = True

            # Save timestamped sample to CSV
            utc_time = datetime.utcnow().isoformat()
            local_time = datetime.now().isoformat()
            writer.writerow([utc_time, local_time] + sample[:len(channel_labels)])

            # Fill buffer for real-time classification
            for i, label in enumerate(channel_labels):
                eeg_buffer[label].append(sample[i])
                if len(eeg_buffer[label]) > EEG_BUFFER_SIZE:
                    eeg_buffer[label].pop(0)

            # Emit data for live plot
            socketio.emit('eeg_data', {
                'timestamp': utc_time,
                'data': sample
            })

            # Classify cognitive state periodically
            if time.time() - last_state_time > EEG_STATE_INTERVAL:
                if all(len(ch) >= EEG_BUFFER_SIZE for ch in eeg_buffer.values()):
                    state = classify_state(eeg_buffer)
                    socketio.emit('cognitive_state', {
                        'timestamp': utc_time,
                        'values': state
                    })
                last_state_time = time.time()
