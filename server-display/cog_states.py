#################################################
# cog_states.py - EEG processing and state logic
#################################################

import numpy as np
from scipy.signal import butter, filtfilt, iirnotch
from config import ARTIFACT_FLAG, EPCOH_FLAG

# freq bandpower helper func
def bandpower(data, fs, band):
    freqs = np.fft.rfftfreq(len(data), 1/fs)
    fft = np.abs(np.fft.rfft(data))**2
    idx = np.logical_and(freqs >= band[0], freqs <= band[1])
    return np.sum(fft[idx])

def bandpass_filter(data, fs, lowcut=1.0, highcut=40.0, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band') # def the filter
    filtered_data = filtfilt(b, a, data) # fwd and bckwrd for zero-phase distortion
    return filtered_data

def notch_filter(data, fs, freq=60.0, quality=30): # 60 Hz in US
    # quality factor: higher = narrower notch (30 is a typical value)
    nyquist = 0.5 * fs
    w0 = freq / nyquist
    b, a = iirnotch(w0, quality)
    filtered_data = filtfilt(b, a, data)
    return filtered_data

def has_artifact(data, threshold=100.0):
    """Simple threshold-based artifact rejection"""
    return np.any(np.abs(data) > threshold)

def create_epochs(data, fs, epoch_length=0.5, overlap=0.5):
    """Split data into overlapping epochs."""
    step = int(fs * (epoch_length * (1 - overlap)))
    size = int(fs * epoch_length)
    epochs = []

    for start in range(0, len(data) - size + 1, step):
        epochs.append(data[start:start+size])

    return epochs

# classify cognitive states
def classify_state(eeg_buffer, fs=250):
    ''' Each cognitive state corresponsd to a different dominant frequency in the EEG signals
        Relaxed - low freq, mid amplitude, alpha (8-12 Hz)
        Focused - high freq, spiky amplitude, beta (13-30 Hz)
        Drowsy - sluggish, low amplitude, delta (1-4 Hz)
        Cognitive Load - irregular, noisy, mid amplitude, theta (4-8 Hz)
    '''

    alpha = []
    theta = []
    delta = []
    beta = []

    # Skip if any channel is too short
    if any(len(ch_data) < fs for ch_data in eeg_buffer.values()):
        return {
            "Relaxed": 0.0,
            "Focused": 0.0,
            "Cognitive Load": 0.0,
            "Drowsy": 0.0,
            "Neutral": 1.0
        }

    for ch_data in eeg_buffer.values():
        if len(ch_data) < fs: continue  # skip partial buffers

        # bandpass filter
        filtered_ch = bandpass_filter(np.array(ch_data), fs) 
        # notch filtering
        filtered_ch = notch_filter(filtered_ch, fs)

        if ARTIFACT_FLAG and has_artifact(filtered_ch):
            continue  # skip this channel if artifact detected
        
        if EPCOH_FLAG:
                epochs = create_epochs(filtered_ch, fs, epoch_length=0.5, overlap=0.5)
                alpha_powers = []
                theta_powers = []
                delta_powers = []
                beta_powers = []

                for epoch in epochs:
                    if ARTIFACT_FLAG  and has_artifact(epoch):
                        continue  # optional: skip bad epochs too

                    alpha_powers.append(bandpower(epoch, fs, (8, 12)))
                    theta_powers.append(bandpower(epoch, fs, (4, 8)))
                    delta_powers.append(bandpower(epoch, fs, (1, 4)))
                    beta_powers.append(bandpower(epoch, fs, (13, 30)))

                if alpha_powers:  # avoid division by zero if no clean epochs
                    alpha.append(np.mean(alpha_powers))
                    theta.append(np.mean(theta_powers))
                    delta.append(np.mean(delta_powers))
                    beta.append(np.mean(beta_powers))
        else:
            alpha.append(bandpower(filtered_ch, fs, (8, 12)))
            theta.append(bandpower(filtered_ch, fs, (4, 8)))
            delta.append(bandpower(filtered_ch, fs, (1, 4)))
            beta.append(bandpower(filtered_ch, fs, (13, 30)))

    alpha_avg = np.mean(alpha)
    theta_avg = np.mean(theta)
    delta_avg = np.mean(delta)
    beta_avg = np.mean(beta)

    total = alpha_avg + beta_avg + theta_avg + delta_avg + 1e-6  # prevent div by zero

    return {
        "Relaxed": alpha_avg / total,
        "Focused": beta_avg / total,
        "Cognitive Load": theta_avg / total,
        "Drowsy": delta_avg / total,
        "Neutral": 0.0  # Optional baseline
    }