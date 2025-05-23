# scripts/predict_live.py

import numpy as np
import joblib
from processing.preprocess import notch, bandpass
from processing.feature_extraction import extract_features

def predict_from_window(window, fs, config, model_path):
    # Apply notch and bandpass filters
    filtered = notch(window, fs, notch_freq=np.mean(config["notch_hz"]))
    filtered = bandpass(filtered, fs, *config["bandpass_hz"])

    # Feature extraction expects a list of epochs
    epochs = [filtered]
    features_df = extract_features(epochs, fs=fs)

    if hasattr(features_df, "values"):
        features = features_df.values[0].reshape(1, -1)
    else:
        features = np.array(features_df[0]).reshape(1, -1)

    # Load model and predict
    model = joblib.load(model_path)
    prediction = model.predict(features)[0]

    return prediction
