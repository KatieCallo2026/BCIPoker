# gsr_stream.py
import serial
import time
import random
from datetime import datetime
from server.realtime_data import USE_MOCK_GSR

def stream_real_gsr(socketio):
    try:
        ser = serial.Serial(
            port='/dev/ttyACM0',  # Adjust as needed
            baudrate=9600
        )
        print("[GSR] Using REAL GSR data")

        while True:
            try:
                val_read = int(ser.readline().strip())
                resistance = (1024 + (2 * val_read)) * (1 / (512 - val_read))
                val_res = (1 / resistance) * 100

                socketio.emit('gsr_data', {
                    'timestamp': datetime.utcnow().isoformat(),
                    'value': val_res
                })

                time.sleep(0.1)

            except ValueError:
                continue  # Skip bad data

    except serial.SerialException as e:
        print(f"[GSR] Serial connection error: {e}")

def stream_mock_gsr(socketio):
    print("[GSR] Using MOCK GSR data")
    while True:
        val_res = round(random.uniform(0.01, 0.05), 4)
        socketio.emit('gsr_data', {
            'timestamp': datetime.utcnow().isoformat(),
            'value': val_res
        })
        time.sleep(0.1)

def stream_gsr(socketio):
    if USE_MOCK_GSR:
        stream_mock_gsr(socketio)
    else:
        stream_real_gsr(socketio)
