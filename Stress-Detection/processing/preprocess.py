# preprocess.py
import numpy as np
from scipy.signal import butter, filtfilt, iirnotch, resample
import pandas as pd

# resampling
def resample_to_duration(data, target_duration_sec, fs):
    current_duration = data.shape[0] / fs
    target_samples = int(target_duration_sec * fs)
    return resample(data, target_samples, axis=0)

# Notch filter
def notch(data, fs, notch_freq=60.0, Q=30.0):
    b, a = iirnotch(notch_freq / (0.5 * fs), Q)
    return filtfilt(b, a, data, axis=0)    

# Bandpass filter
def bandpass(data, fs, lowcut, highcut, order=4):
    nyq = 0.5 * fs
    b, a = butter(order, [lowcut / nyq, highcut / nyq], btype='band')
    return filtfilt(b,a,data,axis=0)

# Epoch into 2 second windows    
def preprocess_eeg(df, fs, bandpass_hz, notch_hz, artifact_thresh_uv=75,
                   timestamps=None, expected_duration=None, epoch_length_sec=2, epoch_step_sec=2):
    
    data = df.iloc[:, 2:].values  # exclude timestamps

    # apply the filters
    data = notch(data, fs, notch_freq=np.mean(notch_hz))
    data = bandpass(data, fs, *bandpass_hz)

    # resample to match expected duration (if needed)
    if timestamps is not None and expected_duration is not None:
        actual_duration = timestamps[-1] - timestamps[0]
        if abs(actual_duration - expected_duration) > 1.0:
            print(f"> Resampling from {actual_duration:.2f}s to {expected_duration:.2f}s...")
            data = resample_to_duration(data, expected_duration, fs)

    # Epoching into 2 sec windows
    epoch_len = int(fs * epoch_length_sec)
    step_len = int(fs * epoch_step_sec)

    epochs = []
    for start in range(0, len(data) - epoch_len + 1, step_len):
        epoch = data[start:start + epoch_len]
        # Optional: Artifact rejection (commented out)
        # if np.any(np.abs(epoch) > artifact_thresh_uv):
        #     continue
        epochs.append(epoch)

    return np.array(epochs)
