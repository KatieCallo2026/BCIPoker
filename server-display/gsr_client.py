#import pyfirmata
import time
from datetime import datetime
from config import GSR_UPDATE_INTERVAL
import serial
# !pip install bleak


def stream_gsr_usb(socketio,useSocketio=True):
    '''Stream gsr data to serial port'''
    
    # In Windows Powershell:
    # usbipd list
    # usbipd bind --busid N-N
    # usbipd attach --wsl --busid N-N
    # usbipd list <- verify its attached and shared
    
    # To unbind (for BT setup)
    # usbipd unbind --busid N-N

    ser = serial.Serial(
        #port='/dev/cu.usbmodemDC5475E9EE282',
        port='/dev/ttyACM0', # wsl connect to win 
        baudrate=9600,
        parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.SEVENBITS
    )

    while(True):
        val = int(ser.readline().strip())
        resistance = (1024+(2*val)) * (1/(512-val))
        val = (1/resistance) * 100
        if val is not None and useSocketio:
            socketio.emit('gsr_data', {
                'timestamp': datetime.utcnow().isoformat(),
                'value': val
            })

    ser.close()



if __name__ == "__main__":
    stream_gsr(None, useSocketio=False)