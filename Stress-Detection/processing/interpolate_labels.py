import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import json

# Load config to get phase durations
with open("config/experiment_config.json") as f:
    CONFIG = json.load(f)
PHASE_DURATIONS = {p["name"]: p["duration_sec"] for p in CONFIG["phases"]}

def interpolate_labels(spsl_df, total_samples, method='linear'):
    # Compute cumulative time for each SPSL entry
    cumulative_times = []
    time_elapsed = 0
    for _, row in spsl_df.iterrows():
        cumulative_times.append(time_elapsed + row["time_sec"])
        time_elapsed += PHASE_DURATIONS.get(row["phase"], 0)

    times = np.array(cumulative_times)
    ratings = spsl_df['rating'].values

    if len(times) == 1:
        print("> Only one SPSL point found. Using constant label.")
        return np.full(total_samples, ratings[0])

    try:
        f = interp1d(times, ratings, kind=method, fill_value="extrapolate")
        target_times = np.linspace(0, times[-1], total_samples)
        return f(target_times)
    except Exception as e:
        print(f"> Interpolation failed: {e}")
        return np.full(total_samples, np.nan)
