from flask import Flask, jsonify, render_template
from flask_cors import CORS
import random
import time
from threading import Thread

app = Flask(__name__, template_folder='../templates')
CORS(app)

# Global variable to store simulated EEG data
latest_data = {"band_power": {}, "emotion": "Neutral"}

def compute_synthetic_band_power():
    return {
        "Delta": random.randint(10, 100),
        "Theta": random.randint(10, 100),
        "Alpha": random.randint(10, 100),
        "Beta": random.randint(10, 100),
        "Gamma": random.randint(10, 100),
    }

def estimate_emotion(band_power):
    if band_power["Alpha"] > band_power["Beta"] and band_power["Gamma"] > band_power["Delta"]:
        return "Happiness"
    elif band_power["Delta"] > band_power["Alpha"] and band_power["Theta"] > band_power["Beta"]:
        return "Sadness"
    elif band_power["Beta"] > band_power["Alpha"] and band_power["Beta"] > band_power["Theta"]:
        return "Fear"  # Changed from "Fear/Anxiety" to "Fear"
    elif band_power["Alpha"] > band_power["Theta"] and band_power["Theta"] > band_power["Delta"]:
        return "Relaxation"
    else:
        return "Neutral"


def simulate_eeg_data():
    global latest_data
    while True:
        band_power = compute_synthetic_band_power()
        emotion = estimate_emotion(band_power)
        latest_data = {"band_power": band_power, "emotion": emotion}
        time.sleep(1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/eeg-data')
def get_eeg_data():
    return jsonify(latest_data)

if __name__ == '__main__':
    # Run EEG simulation in a separate thread
    Thread(target=simulate_eeg_data, daemon=True).start()
    app.run(debug=True)
