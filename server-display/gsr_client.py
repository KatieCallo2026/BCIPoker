import pyfirmata
import time
from datetime import datetime

def stream_gsr(socketio):
    board = pyfirmata.Arduino('/dev/tty.YOUR_BLUETOOTH_PORT')  # Replace with your Bluetooth port
    it = pyfirmata.util.Iterator(board)
    it.start()

    gsr_pin = board.analog[0]
    gsr_pin.enable_reporting()

    while True:
        val = gsr_pin.read()
        if val is not None:
            socketio.emit('gsr_data', {
                'timestamp': datetime.utcnow().isoformat(),
                'value': val
            })
        time.sleep(0.05)  # ~20Hz
