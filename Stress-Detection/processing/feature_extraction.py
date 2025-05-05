# feature extraction
import numpy as np

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
    
    features = []
    for epoch in epochs:
        bp = [np.mean(bandpower(epoch, fs, b)) for b in bands.values()]
        features.append(bp)
    
    return np.array(features)
