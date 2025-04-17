import time
import numpy as np
from pylsl import StreamInlet, resolve_streams

def main():
    # Step 1: Resolve an LSL stream
    print("Looking for an EEG stream...")
    streams = resolve_streams('type', 'EEG')

    # Create an inlet to read data
    inlet = StreamInlet(streams[0])
    print("Connected to EEG stream.")

    # Sampling rate (modify based on your OpenBCI setup)
    sampling_rate = 250

    # Step 2: Data collection and filtering loop
    try:
        while True:
            # Pull a sample from the LSL stream
            sample, timestamp = inlet.pull_sample()

            # Convert the sample to a numpy array for processing
            eeg_data = np.array(sample)

            # Print raw data (replace this with filtering logic as needed)
            print(f"Timestamp: {timestamp}, EEG Data: {eeg_data}")

            # Sleep to simulate real-time processing
            time.sleep(1.0 / sampling_rate)
    except KeyboardInterrupt:
        print("Streaming stopped.")

if __name__ == "__main__":
    main()
