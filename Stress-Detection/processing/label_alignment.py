# label alignment
import numpy as np
import pandas as pd

def align_labels_to_features(features, interpolated_labels):
    assert len(features) == len(interpolated_labels), "Mismatched lengths"

    num_features = features.shape[1]
    columns = [f"f{i}" for i in range(num_features)]  # generic: f0, f1, f2, ...

    df = pd.DataFrame(features, columns=columns)
    df['label'] = interpolated_labels
    return df
