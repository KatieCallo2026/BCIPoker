from pylsl import StreamInlet, resolve_stream
from datetime import datetime
import time

# columns: ['Time',
# 'FZ', 'C3', 'CZ', 'C4', 'PZ', 'PO7', 'OZ', 'PO8',
# 'AccX','AccY','AccZ',
# 'Gyro1','Gyro2','Gyro3', 
# 'Battery','Counter','Validation']

def stream_eeg(socketio):
    streams = resolve_stream()
    inlet = StreamInlet(streams[0])

    while True:
        sample, timestamp = inlet.pull_sample()
        socketio.emit('eeg_data', {
            'timestamp': datetime.utcnow().isoformat(),
            'data': sample  # raw values for now
        })
        time.sleep(0.004)  # ~250Hz
