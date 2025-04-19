from pylsl import StreamInlet, resolve_stream
from datetime import datetime
import time
from cog_states import classify_state # cog state funcs
from config import EEG_BUFFER_SIZE, EEG_STATE_INTERVAL  #import config values
print("📦 eeg_client.py imported")

##################################################
# eeg_client.py - GSR data stream
# now has cognitive state logic
##################################################

# set up circular buffer with channel labels
channel_labels = ['FZ', 'C3', 'CZ', 'C4', 'PZ', 'PO7', 'OZ', 'PO8']
eeg_buffer = {label: [] for label in channel_labels} 
last_state_time = time.time()

# data sample columns (full thing):
# [ 'FZ', 'C3', 'CZ', 'C4', 'PZ', 'PO7', 'OZ', 'PO8', 'AccX','AccY','AccZ', 'Gyro1','Gyro2','Gyro3',  'Battery','Counter','Validation']

def stream_eeg(socketio):
    print("🔍 Resolving LSL stream...")
    global last_state_time # risky..
    
    inlet = None 
    try:
        streams = resolve_stream()
        inlet = StreamInlet(streams[0])
        print("✅ LSL stream found!")
    except IndexError:
        print("❌ No LSL stream found...")
        return

    
    while True:
        sample, timestamp = inlet.pull_sample(timeout=0.0)
        if not sample: 
            time.sleep(0.001)
            continue

        # fill buffer
        for i, label in enumerate(channel_labels):
            eeg_buffer[label].append(sample[i])
            if len(eeg_buffer[label]) > EEG_BUFFER_SIZE:
                eeg_buffer[label].pop(0)

        # emit the sample for live plot (first channel)
        socketio.emit('eeg_data', {
            'timestamp': datetime.utcnow().isoformat(),
            'data': sample  # raw values for now
        })

        # classify cognitive state every 1s
        if time.time() - last_state_time > EEG_STATE_INTERVAL:
            if all(len(ch) >= EEG_BUFFER_SIZE for ch in eeg_buffer.values()):
                state = classify_state(eeg_buffer)
                #print("🧠 Cognitive state:", state)
                socketio.emit('cognitive_state', {
                    'timestamp': datetime.utcnow().isoformat(),
                    'values': state
                })
            last_state_time = time.time()
        
