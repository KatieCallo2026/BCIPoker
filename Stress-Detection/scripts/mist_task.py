import time
import random
from threading import Thread
from tqdm import tqdm
import sys

def generate_question(level):
    if level == "easy":
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        op = random.choice(['+', '-'])
    elif level == "medium":
        a = random.randint(10, 30)
        b = random.randint(10, 30)
        op = random.choice(['+', '-'])
    else:  # hard
        op = random.choice(['+', '-', '*'])
        if op == '*':
            a = random.randint(6, 12)
            b = random.randint(10, 20)
        else:
            a = random.randint(30, 60)
            b = random.randint(30, 60)
    question = f"{a} {op} {b}"
    answer = eval(f"{a} {op} {b}")
    return question, answer

def timed_input(prompt, timeout=5):
    user_input = [None]

    def get_input():
        user_input[0] = input(prompt)

    thread = Thread(target=get_input)
    thread.daemon = True
    thread.start()

    for i in range(timeout):
        if user_input[0] is not None:
            break
        print(f"Time remaining: {timeout - i}s", end='\r', flush=True)
        time.sleep(1)

    if thread.is_alive():
        print("\n⏱ Too slow!")
        return None
    return user_input[0]

def run(duration_sec=60, difficulty="mist_1", timed=True):
    print(f"\nStarting MIST Task for {duration_sec} seconds...")
    start = time.time()
    correct = 0
    attempted = 0

    if "1" in difficulty:
        level = "easy"
    elif "2" in difficulty:
        level = "medium"
    else:
        level = "hard"

    while time.time() - start < duration_sec:
        elapsed = time.time() - start
        question, answer = generate_question(level)
        print(f"\nSolve: {question}")

        user_input = timed_input("Your answer: ", timeout=5)

        try:
            if user_input is None:
                pass  # too slow, skip
            elif int(user_input.strip()) == answer:
                print("\u2705 Correct!")
                correct += 1
            else:
                print("\u274C Incorrect!")
        except:
            print("\u26A0\uFE0F Invalid input")

        attempted += 1

        # Mock "verbal" pressure
        if attempted % 3 == 0:
            print("Come on, try harder!")
        elif attempted % 5 == 0:
            print("Your performance is below expectations...")

    print(f"\nMIST complete. Score: {correct}/{attempted}")
