#################################################
# config.py — Global constants for timing/sampling
#################################################
# this is so we can tweak timing changes in one place
# files will import these macros from here


# -----------------------------------------------
# EEG SETTINGS
# -----------------------------------------------

# Sampling rate of the EEG device (samples per second - 250 common )
EEG_SAMPLING_RATE = 250             # Hz
# Duration of the EEG buffer window used for analysis (in seconds) - how many seconds of eeg data are used for FFT/state classification
EEG_BUFFER_DURATION = 0.5           # seconds
# Number of EEG samples to store in the buffer - sampling rate × duration
EEG_BUFFER_SIZE = int(EEG_SAMPLING_RATE * EEG_BUFFER_DURATION)

EEG_STATE_INTERVAL = 0.5            # seconds between state classifications


# -----------------------------------------------
# GSR SETTINGS
# -----------------------------------------------

# How often to sample and emit GSR data (in seconds) 
GSR_UPDATE_INTERVAL = 0.05          # 20Hz = every 50 ms, smooth enough for skin conductance
