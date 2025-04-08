import pandas as pd
import time
from datetime import datetime
import pyfirmata
import atexit
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

board = pyfirmata.Arduino('/dev/cu.usbmodemDC5475E9EE282')

it = pyfirmata.util.Iterator(board)
it.start()


output_df = pd.DataFrame(columns=["Timestamp", "Raw Sensor Value"])

analog_input = board.get_pin('a:0:o')
analog_input.enable_reporting()

plt.ion()



data_window_size = 200

data = np.zeros([data_window_size])
timestamps = np.zeros([data_window_size])
figure, ax = plt.subplots(figsize=(10, 8))
plt.title('Realtime Galvanic Skin Response Plot')
line1, = ax.plot(timestamps, data)


plt.xlabel("Time")
plt.ylabel("Raw Sensor Value (micro-Siemens)")


def save_csv():
    output_df.to_csv('gsr_test.csv')

# Set Sampling Rate Here
fs = 100
time_initial = time.time()

try:
    while True:
        time.sleep(1/fs)
        sensor_val = analog_input.read()
        if sensor_val is not None:
            
            data = np.hstack((data[1:], np.array([sensor_val])))
            print(timestamps[:])
            timestamps = np.hstack((timestamps[1:], np.array([time.time() - time_initial])))
            
            ax.plot(timestamps, data)
            # line1.set_xdata(timestamps)
            # line1.set_ydata(data)
        
            # drawing updated values
            figure.canvas.draw()
        
            # This will run the GUI event
            # loop until all UI events
            # currently waiting have been processed
            figure.canvas.flush_events()

            print(sensor_val)
            output_df = pd.concat([pd.DataFrame([[datetime.now(), sensor_val]], columns=output_df.columns), output_df], ignore_index=True)

except KeyboardInterrupt:
    save_csv()
finally:
    save_csv()

atexit.register(save_csv)



