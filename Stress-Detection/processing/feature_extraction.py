# feature extraction
import numpy as np
from scipy.stats import kurtosis, skew

# Bandpower: delta, theta, alpha, beta, gamma
def bandpower(epoch, fs, band):
    freqs = np.fft.rfftfreq(epoch.shape[0], 1/fs)
    fft_vals = np.abs(np.fft.rfft(epoch, axis=0)) ** 2
    idx = np.logical_and(freqs >= band[0], freqs <= band[1])
    return np.sum(fft_vals[idx, :], axis=0)

# TODO Frontal alpha asymmetry

# TODO Relative gamma (RG)

# TODO Statistical moments (mean, std, skew)

def extract_features(epochs, fs):
    bands = {
        'delta': (1, 4), 'theta': (4, 8), 'alpha': (8, 13),
        'beta': (13, 25), 'gamma': (25, 45)
    }
    channel_labels = ['AF3', 'AF4', 'F3', 'F4', 'T7', 'T9', 'P7', 'P8']
    
    features = []
    
    for epoch in epochs:
        feat_vector = []
    
        # ---- Bandpowers ----
        bandpowers = {band: bandpower(epoch, fs, rng) for band, rng in bands.items()}
        for bp in bandpowers.values():
            feat_vector.append(np.mean(bp))  # avg bandpower over channels

        # ---- Frontal Alpha Asymmetry ----
        ch_f3 = channel_labels.index('F3')
        ch_f4 = channel_labels.index('F4')
        alpha_f3 = bandpowers['alpha'][ch_f3]
        alpha_f4 = bandpowers['alpha'][ch_f4]
        faa = np.log(alpha_f4 + 1e-6) - np.log(alpha_f3 + 1e-6)
        feat_vector.append(faa)

        # ---- Relative Gamma ----
        alpha = bandpowers['alpha']
        beta = bandpowers['beta']
        gamma = bandpowers['gamma']
        rg = gamma / (alpha + beta + 1e-6)
        feat_vector.append(np.mean(rg))

        # ---- Statistical Moments per channel ----
        for ch in range(epoch.shape[1]):
            signal = epoch[:, ch]
            feat_vector.extend([
                np.mean(signal),
                np.std(signal),
                skew(signal),
                kurtosis(signal)
            ])

        features.append(feat_vector)

    return np.array(features)
