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

    # Simple logic-based classifier
    if alpha_avg > theta_avg * 2:
        return "Relaxed"
    elif theta_avg > alpha_avg * 1.5:
        return "Cognitive Load"
    elif delta_avg > beta_avg * 1.2:
        return "Drowsy"
    elif beta_avg > theta_avg * 2:
        return "Focused"
    else:
        return "Neutral"
    
    # for now it shows 1 state, might switch to all and display the most probable ? 