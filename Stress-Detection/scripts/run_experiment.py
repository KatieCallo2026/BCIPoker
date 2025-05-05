import os
import time
import json
import datetime
from pathlib import Path
import mist_task
import spsl_prompt
import lsl_record
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

def record_phase(phase_name, duration_sec, lsl_outfile):
    log(f"--- Starting {phase_name.upper()} phase ({duration_sec} sec) ---")
    start_time = time.time()
    lsl_record.start_recording(lsl_outfile, mock=MOCK_MODE)
    time.sleep(duration_sec)
    lsl_record.stop_recording()
    end_time = time.time()
    return {"phase": phase_name, "start": start_time, "end": end_time}

def run_experiment():
    pid = input("Participant ID: ").strip()
    folder = get_participant_folder(pid)
    eeg_outfile = folder / "eeg_raw.csv"
    timestamp_log = []
    spsl_log = []

    for phase in CONFIG["phases"]:
        name = phase["name"]
        duration = phase["duration_sec"]

        # Prepare EEG recording
        phase_info = record_phase(name, duration, eeg_outfile)
        timestamp_log.append(phase_info)

        if name == "mist":
            mist_task.run(duration)  # purely visual / print-based for now

        # After EEG ends, prompt for SPSL (to avoid recording artifacts)
        for prompt_time in CONFIG["spsl_prompts"].get(name, []):
            log(f"SPSL prompt for phase {name} at {prompt_time}s")
            rating = spsl_prompt.ask_scale(pid, phase=name, time_sec=prompt_time)
            spsl_log.append(rating)

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
