# BCIPOKER

BCI for AULI.TEC and Crux@UCLA's Poker Night

# Project Contributors 
Katie Callo
Vikram Ganesan
Abril Aguilar Lopez
Raymond Kallely
Simran Tawari
Natalie Sim
Umair Khan
Fulati Aizihaer
Joseph Dekel

# Project Description

### Summary: Real-Time Emotion Measurement Poker Tournament  

This project integrates brain computer interface technology into poker, using biometric data to analyze and visualize players' cognitive states during a game of poker.

### Objectives  
- Showcase Auli.tech, Cato, and CruX technologies.  
- Fundraise for ALS foundations and CruX initiatives.  
- Engage audiences through interactive gameplay and live data visualizations.  

### Timeline  
- Recruit team, secure venue.  
- Finalize designs, train emotion models, promote event.  
- Present demo at California Neurotech Conference in San Diego
- Host poker tournament at UCLA.  
- Display at Los Angeles Walk for ALS.  

This event blends entertainment and education, highlighting biometric tech while supporting meaningful causes.

# Data Pipeline

**Where do we get data, and what do we do with it?**

![Whoops! Should be the data pipeline here](Graphics/data-pipeline-v2.png)
./ru    
# Demo Display

![Should be our screen display here!](Graphics/demo-gui.png)

# Usage

## Server Display (DEMO)

```bash
python app.py
```

## Stress Detection

This script serves as the main entry point for running the EEG experiment pipeline, including data collection, preprocessing, and future model training.

```bash
python main.py [--e | --p PID | --m PID]
```

Flags

### `--e`

Runs the live EEG experiment, including:
- Participant ID prompt
- Real-time EEG recording (mock or real LSL stream)
- MIST task (math stressor)
- SPSL (subjective stress rating) prompts
- Saves:
    - eeg_raw.csv
    - spsl_responses.csv
    - phase_timestamps.json

### `--p`
Processes data for a given participant:
- Loads eeg_raw.csv and spsl_responses.csv
- Applies preprocessing (notch filter, bandpass, artifact rejection)
- Epochs into 2s segments
- Extracts bandpower features (delta–gamma)
- Interpolates SPSL ratings to match features
- Aligns and saves to processed_data.csv

### `--m PID` (placeholder)
- This flag is reserved for future model training. It will:
- Load processed_data.csv for the specified participant
- Train a machine learning classifier
- Output model performance and optionally save the trained model

### `--s` 

Runs the ral-time server display dashboard, including:
- starting the flask + socketIO server
- streams EEG and GSR data
- generated predictions for 
    - stress detection
    - lie detection
- displays all signals and predictions in the interactive GUI

# Credits 

- Fulati Aizihaer
- Katie Callo
- Joseph Dekel
- Abdallah Fares
- Omar Fayaz
- Vikram Ganesan
- Raymond Kallely
- Umair Khan
- Abril Aguilar Lopez
- Chrysa Prentza
- Natalie Sim
- Simran Tawari
- Alizee Wouters

