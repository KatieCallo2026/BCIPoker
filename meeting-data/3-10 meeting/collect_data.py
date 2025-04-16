import sys
from pylsl import StreamInlet, resolve_stream
import csv
import time

def collect_data(duration, filename):
    """
    Collects EEG data from each trial in an LSL stream and writes it to a CSV file.

    Parameters:
    - duration (float): Duration in seconds to collect data.
    - filename (str): Path to the output CSV file.
    """
    try:
        # Resolve EEG streams available on the network
        streams = resolve_stream('type', 'EEG')
        if not streams:
            print("No EEG stream found. Please ensure an EEG stream is available.")
            return

        # Create an inlet to receive data from the first EEG stream
        inlet = StreamInlet(streams[0])

        # Open the CSV file in append mode
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            end_time = time.time() + duration

            # Collect data until the specified duration has passed
            while time.time() < end_time:
                sample, timestamp = inlet.pull_sample(timeout=0.5)
                if sample:
                    writer.writerow([timestamp] + sample)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    """
    Entry point of the script. Parses command-line arguments and starts data collection.
    """
    # Parse command-line arguments with default values
    duration = float(sys.argv[1]) if len(sys.argv) > 1 else 5
    filename = sys.argv[2] if len(sys.argv) > 2 else 'eeg_data.csv'
    
    # Start collecting EEG data
    collect_data(duration, filename)
