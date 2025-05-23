import pandas as pd
import joblib
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def train_stress_model(pid, config):
    """Train a model for a single participant ID"""
    data_path = Path(config["output_dir"]) / pid / "processed_data.csv"
    if not data_path.exists():
        print(f"Processed data not found for participant {pid}")
        return

    df = pd.read_csv(data_path)
    X = df.drop(columns=["label"]).values
    y = df["label"].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print(f"[{pid}] R² Score: {r2_score(y_test, y_pred):.4f}")
    print(f"[{pid}] MSE: {mean_squared_error(y_test, y_pred):.4f}")

    model_path = Path(config["output_dir"]) / pid / "stress_model.pkl"
    joblib.dump(model, model_path)
    print(f"[{pid}] Model saved to {model_path}")


def train_model_on_all_sessions(data_dir, config):
    """Train a single model using all participant data combined"""
    all_data = []

    for session_dir in Path(data_dir).iterdir():
        file = session_dir / "processed_data.csv"
        if file.exists():
            print(f"> Including {session_dir.name}")
            df = pd.read_csv(file)
            all_data.append(df)
        else:
            print(f"> Skipping {session_dir.name} — no processed_data.csv")

    if not all_data:
        print("❌ No session data found. Aborting.")
        return

    df = pd.concat(all_data, ignore_index=True)
    X = df.drop(columns=["label"]).values
    y = df["label"].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print(f"[ALL] R² Score: {r2_score(y_test, y_pred):.4f}")
    print(f"[ALL] MSE: {mean_squared_error(y_test, y_pred):.4f}")

    model_path = Path(data_dir) / "stress_model_all.pkl"
    joblib.dump(model, model_path)
    print(f"[ALL] Model saved to {model_path}")
