# label alignment
import numpy as np
import pandas as pd

def align_labels_to_features(features, interpolated_labels):
    assert len(features) == len(interpolated_labels), "Mismatched lengths"
    df = pd.DataFrame(features, columns=["delta", "theta", "alpha", "beta", "gamma"])
    df['label'] = interpolated_labels
    return df
