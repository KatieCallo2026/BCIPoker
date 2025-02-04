import os
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BrainFlowError, BoardIds
import time
import matplotlib.pyplot as plt
import numpy as np
import collections
import pandas as pd

DEMO_TIME = 15
WINDOW_SIZE = 80  # Points displayed in the sliding window
BUFFER_SIZE = 100  # Save to CSV every 100 samples

CSV_FILENAME = "eeg_stream_data.csv"  # Output file

columns = ['Time', 'FZ', 'C3', 'CZ', 'C4', 'PZ', 'PO7', 'OZ', 'PO8',
           'AccX', 'AccY', 'AccZ', 'Gyro1', 'Gyro2', 'Gyro3', 
           'Battery', 'Counter', 'Validation']

# Control which columns to display & save (True = Display & Save)
control = [True, True, True, True, True, True, True, True, False,
           False, False, False, False, False, False, 
           False, False, False]  # Only display first 8 electrodes

color_cycle = plt.cm.get_cmap("tab10", len(columns))  # Get distinct colors

def save_to_csv(buffer):
    """Appends data buffer to a CSV file."""
    if not buffer:
        return  # Don't write an empty buffer

    df = pd.DataFrame(buffer, columns=selected_columns)  # Create DataFrame

    file_exists = os.path.exists(CSV_FILENAME)  # Check if file exists

    try:
        df.to_csv(CSV_FILENAME, mode='a', header=not file_exists, index=False)  # Append mode
        print(f"✅ Data saved to {CSV_FILENAME} ({len(buffer)} rows)")
    except Exception as e:
        print(f"❌ Error saving to CSV: {e}")

    buffer.clear()  # Reset buffer

def main():
    params = BrainFlowInputParams()
    board = BoardShim(BoardIds.SYNTHETIC_BOARD, params)  # Change to UNICORN_BOARD for real EEG

    try:
        BoardShim.enable_dev_board_logger()
        board.prepare_session()
        board.start_stream()
        print(f"Data stream started. Saving to {CSV_FILENAME}")

        plt.ion()

        # Select only columns where control[i] is True
        global selected_columns
        selected_columns = [col for col, show in zip(columns, control) if show]

        num_signals = len(selected_columns) - 1  # Exclude 'Time' from count

        if num_signals == 0:
            print("⚠️ No signals selected for display.")
            return

        fig, axes = plt.subplots(num_signals, 1, figsize=(10, 2 * num_signals), sharex=True)
        if num_signals == 1:
            axes = [axes]

        data_buffers = {col: collections.deque(maxlen=WINDOW_SIZE) for col in selected_columns[1:]}
        lines = {}
        csv_buffer = []  # Data buffer for CSV

        for i, (ax, col) in enumerate(zip(axes, selected_columns[1:])):
            color = color_cycle(i)
            lines[col], = ax.plot([], [], label=col, color=color)
            ax.set_xlim(0, WINDOW_SIZE)
            ax.set_ylim(-50, 100)  # Adjust for EEG signal scale
            ax.set_ylabel(col)
            ax.legend(loc="upper right")

        start_time = time.time()
        while time.time() - start_time < DEMO_TIME:
            data = board.get_current_board_data(10)  # Get new data
            
            if data.shape[1] > 0:
                row_data = []  # Store data row-wise
                for i, col in enumerate(columns):
                    if col in selected_columns:
                        row_data.append(data[i, -1])  # Take the latest sample

                    if col in data_buffers and i > 0:
                        data_buffers[col].extend(data[i])

                csv_buffer.append(row_data)

                for col in data_buffers:
                    lines[col].set_xdata(range(len(data_buffers[col])))
                    lines[col].set_ydata(data_buffers[col])

                plt.draw()
                plt.pause(0.01)

                if len(csv_buffer) >= BUFFER_SIZE:
                    save_to_csv(csv_buffer)

        if csv_buffer:
            save_to_csv(csv_buffer)

        board.stop_stream()
        board.release_session()
        print(f"✅ Demo complete. Data saved to {CSV_FILENAME}")

    except BrainFlowError as e:
        print(f"❌ BrainFlowError: {e}")

if __name__ == "__main__":
    main()
