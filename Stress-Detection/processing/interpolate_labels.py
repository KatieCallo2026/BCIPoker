# interpolate spsl labels
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

def interpolate_labels(spsl_df, total_samples, method='linear'):
    times = spsl_df['time_sec'].values
    ratings = spsl_df['rating'].values
    f = interp1d(times, ratings, kind=method, fill_value="extrapolate")
    
    target_times = np.linspace(0, times[-1], total_samples)
    return f(target_times)
