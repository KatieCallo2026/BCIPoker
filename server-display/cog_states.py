#################################################
# cog_states.py - EEG processing and state logic
#################################################

import numpy as np

# freq bandpower helper func
def bandpower(data, fs, band):
    freqs = np.fft.rfftfreq(len(data), 1/fs)
    fft = np.abs(np.fft.rfft(data))**2
    idx = np.logical_and(freqs >= band[0], freqs <= band[1])
    return np.sum(fft[idx])

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
        alpha.append(bandpower(ch_data, fs, (8, 12)))
        theta.append(bandpower(ch_data, fs, (4, 8)))
        delta.append(bandpower(ch_data, fs, (1, 4)))
        beta.append(bandpower(ch_data, fs, (13, 30)))

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