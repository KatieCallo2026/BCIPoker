# Updated run_experiment.py
import os
import time
import json
import datetime
from pathlib import Path
import scripts.mist_task as mist_task
#import scripts.mist_task_pygame as mist_task
import scripts.spsl_prompt as spsl_prompt
import scripts.lsl_record as lsl_record
from configparser import ConfigParser

# Load config
with open("config/experiment_config.json", "r") as f:
    CONFIG = json.load(f)
MOCK_MODE = CONFIG.get("mock_mode", False)

def log(message):
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {message}")

def get_participant_folder(pid):
    path = Path(CONFIG["output_dir"]) / pid
    path.mkdir(parents=True, exist_ok=True)
    return path

def record_phase(phase_name, duration_sec, lsl_outfile, pid, screen=None):
    log(f"--- Starting {phase_name.upper()} phase ({duration_sec} sec) ---")
    start_time = time.time()

    # Start EEG recording
    lsl_record.start_recording(lsl_outfile, mock=MOCK_MODE)

    if "mist" not in phase_name:
        print(f"> Recording {phase_name} phase...")
        time.sleep(duration_sec)

    lsl_record.stop_recording()
    end_time = time.time()

    # Ask SPSL at end of each atomic phase
    rating = spsl_prompt.ask_scale(pid, phase=phase_name, time_sec=duration_sec)

    return {"phase": phase_name, "start": start_time, "end": end_time}, rating

def run_experiment():
    pid = input("Participant ID: ").strip()
    folder = get_participant_folder(pid)
    eeg_outfile = folder / "eeg_raw.csv"
    timestamp_log = []
    spsl_log = []

    screen = None

    for phase in CONFIG["phases"]:
        name = phase["name"]
        duration = phase["duration_sec"]

        if "mist" in name:
            mist_task.run(duration, difficulty=name)
    
        phase_info, spsl_entry = record_phase(name, duration, eeg_outfile, pid)
        timestamp_log.append(phase_info)
        spsl_log.append(spsl_entry)

    # Save logs
    with open(folder / "spsl_responses.csv", "w") as f:
        f.write("phase,time_sec,rating\n")
        for entry in spsl_log:
            f.write(f"{entry['phase']},{entry['time_sec']},{entry['rating']}\n")

    with open(folder / "phase_timestamps.json", "w") as f:
        json.dump(timestamp_log, f, indent=2)

    log(f"Experiment completed for {pid}.")

if __name__ == "__main__":
    run_experiment()
    