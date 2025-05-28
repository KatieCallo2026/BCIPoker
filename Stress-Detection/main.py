import os
import json
import argparse
import pandas as pd
from pathlib import Path

from processing.preprocess import preprocess_eeg
from processing.feature_extraction import extract_features
from processing.interpolate_labels import interpolate_labels
from processing.label_alignment import align_labels_to_features
from processing.train_model import train_stress_model, train_model_on_all_sessions

from server.app import run_server 
from scripts.run_experiment import run_experiment
from sklearn.preprocessing import StandardScaler

# Load config
with open("config/experiment_config.json") as f:
    CONFIG = json.load(f)

def run_pipeline(pid):
    data_dir = Path(CONFIG["output_dir"]) / pid
    eeg_path = data_dir / "eeg_raw.csv"
    spsl_path = data_dir / "spsl_responses.csv"

    if not eeg_path.exists() or not spsl_path.exists():
        print(f"Missing data for participant {pid}.")
        return


    print(f"> Running pipeline for {pid}")

    # Load EEG and preprocess
    print("Preprocessing EEG...")
    eeg_df = pd.read_csv(eeg_path)
    epochs = preprocess_eeg(
        eeg_df,
        fs=CONFIG["sampling_rate"],
        bandpass_hz=CONFIG["bandpass_hz"],
        notch_hz=CONFIG["notch_hz"],
        artifact_thresh_uv=CONFIG["artifact_threshold_uv"],
        timestamps=None, 
        expected_duration=None, 
        epoch_length_sec=2, 
        epoch_step_sec=0.01 # sliding window epoching, this is the step size
    )
    # Extract features
    print("Extracting features...")
    features = extract_features(epochs, fs=CONFIG["sampling_rate"])

    # Normalize features
    print("Normalizing features...")
    scaler = StandardScaler()
    features = scaler.fit_transform(features)

    # Interpolate SPSL labels
    print("Interpolating SPSL...")
    spsl_df = pd.read_csv(spsl_path)
    interpolated = interpolate_labels(spsl_df, len(features))

    # Align and save output
    print("Aligning and saving...")
    aligned_df = align_labels_to_features(features, interpolated)
    out_path = data_dir / "processed_data.csv"
    aligned_df.to_csv(out_path, index=False)
    print(f"Done. Output saved to {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--e", action="store_true", help="Run data collection experiment")
    parser.add_argument("--p", type=str, metavar="PID", help="Run preprocessing for given participant ID")
    parser.add_argument("--m", type=str, metavar="PID", help="Train model (placeholder)")
    parser.add_argument("--s", action="store_true", help="Run real-time Flask dashboard server")  # NEW FLAG

    args = parser.parse_args()

    if args.e:
        run_experiment()
    elif args.p:
        run_pipeline(args.p)
    elif args.m:
        if args.m.lower() == "all":
            train_model_on_all_sessions(CONFIG["output_dir"], CONFIG)
        else:
            train_stress_model(args.m, CONFIG)
    elif args.s:
        run_server()
    else:
        parser.print_help()
