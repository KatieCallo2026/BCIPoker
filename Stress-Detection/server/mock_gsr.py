# mock_gsr.py
import time, random

def get_gsr_sample():
    return round(random.uniform(0.01, 0.05), 4)

if __name__ == "__main__":
    while True:
        print(get_gsr_sample())
        time.sleep(0.25)
