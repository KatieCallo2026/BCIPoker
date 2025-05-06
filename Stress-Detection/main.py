import os
import json
import argparse
import pandas as pd
from pathlib import Path

from processing.preprocess import preprocess_eeg
from processing.feature_extraction import extract_features
from processing.interpolate_labels import interpolate_labels
from processing.label_alignment import align_labels_to_features

from scripts.run_experiment import run_experiment

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

    # Load EEG and preprocess
    print("Preprocessing EEG...")
    eeg_df = pd.read_csv(eeg_path)
    epochs = preprocess_eeg(
        eeg_df,
        fs=CONFIG["sampling_rate"],
        bandpass_hz=CONFIG["bandpass_hz"],
        notch_hz=CONFIG["notch_hz"],
        artifact_thresh_uv=CONFIG["artifact_threshold_uv"]
    )

    # Extract features
    print("Extracting features...")
    features = extract_features(epochs, fs=CONFIG["sampling_rate"])

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
    args = parser.parse_args()

    if args.e:
        run_experiment()
    else:
        pid = input("Enter participant ID: ").strip()
        run_pipeline(pid)
