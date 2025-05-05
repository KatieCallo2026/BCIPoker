# preprocess.py
import numpy as np
from scipy.signal import butter, filtfilt, iirnotch
import pandas as pd

# Notch filter
def notch(data, fs, notch_freq=60.0, Q=30.0):
    b, a = iirnotch(notch_freq / (0.5 * fs), Q)
    return filtfilt(b, a, data, axis=0)    

# Bandpass filter
def bandpass(data, fs, lowcut, highcut, order=4):
    nyq = 0.5 * fs
    b, a = butter(order, [lowcut / nyq, highcut / nyq], btype='band')
    return filtfilt(b,a,data,axix=0)

# Epoch into 2 second windows
def preprocess_eeg(df, fs, bandpass_hz, notch_hz, artifact_thresh_uv=75):
    data = df.iloc[:, 2:].values  # exclude timestamps

    # apply the filters
    data = notch(data, fs, notch_freq=np.mean(notch_hz))
    data = bandpass(data, fs, *bandpass_hz)
    
    # Epoching into 2 sec windows
    epoch_len = int(fs * 2)
    n_epochs = len(data) // epoch_len
    epochs = data[:n_epochs * epoch_len].reshape(n_epochs, epoch_len, -1)

    # Artifact rejection: zero out epochs with high amplitude
    mask = np.any(np.abs(epochs) > artifact_thresh_uv, axis=(1, 2))
    epochs[mask] = 0

    return epochs