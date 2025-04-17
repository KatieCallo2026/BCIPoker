from pylsl import StreamInlet, resolve_stream
from datetime import datetime
import time
from cog_states import classify_state # cog state funcs

##################################################
# eeg_client.py - GSR data stream
# now has cognitive state logic
##################################################

# set up circular buffer
BUFFER_SIZE = 250  # 1 sec at 250Hz
eeg_buffer = {i: [] for i in range(8)}
STATE_INTERVAL = 1.0  # seconds between state classification
last_state_time = time.time()

# data sample columns: ['Time',
# 'FZ', 'C3', 'CZ', 'C4', 'PZ', 'PO7', 'OZ', 'PO8',
# 'AccX','AccY','AccZ',
# 'Gyro1','Gyro2','Gyro3', 
# 'Battery','Counter','Validation']

def stream_eeg(socketio):
    global last_state_time # risky..
    streams = resolve_stream()
    inlet = StreamInlet(streams[0])

    while True:
        sample, timestamp = inlet.pull_sample()
        if not sample: continue # err check

        # fill buffer
        for i in range(8):
            eeg_buffer[i].append(sample[i])
            if len(eeg_buffer[i]) > BUFFER_SIZE:
                eeg_buffer[i].pop(0)

        # emit the sample for live plot (first channel)
        socketio.emit('eeg_data', {
            'timestamp': datetime.utcnow().isoformat(),
            'data': sample  # raw values for now
        })

        # classify cognitive state every 1s
        if time.time() - last_state_time > STATE_INTERVAL:
            state = classify_state(eeg_buffer)
            print("Classified state:", state)
            socketio.emit('cognitive_state', {
                'timestamp': datetime.utcnow().isoformat(),
                'state': state
            })
            last_state_time = time.time()

        time.sleep(0.004)  # ~250Hz
