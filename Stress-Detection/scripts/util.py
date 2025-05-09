# utility functions 
import pandas as pd

def load_eeg_data(csv_path, channels, fs=250):
    df = pd.read_csv(csv_path)
    # Just keep EEG channel data (drop timestamps)
    eeg = df[channels].values
    return eeg



