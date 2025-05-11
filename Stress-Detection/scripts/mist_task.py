import time
import random
from threading import Thread
from tqdm import tqdm
import sys

RED = "\033[91m"
RESET = "\033[0m"

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

def timed_input(prompt="Answer: ", timeout=5):
    import msvcrt  # Windows-specific
    import sys

    answer = ""
    start_time = time.time()

    print("\n", end='')  # spacing
    while True:
        elapsed = time.time() - start_time
        remaining = int(timeout - elapsed)

        if remaining < 0:
            print("\r⏱ Time's up!                    ")
            return None

        # Timer color logic
        timer_str = f"Time Remaining: {remaining}s{RESET}"

        # Build the status line
        status = f"\rTime Remaining: {remaining}s     Answer: {answer} "
        print(status, end='', flush=True)

        if msvcrt.kbhit():
            char = msvcrt.getwche()
            if char in '\r\n':  # Enter
                print()  # Move to next line
                return answer.strip()
            elif char == '\b':  # Backspace
                answer = answer[:-1]
                print('\b \b', end='', flush=True)
            elif char.isprintable():
                answer += char

        time.sleep(0.05)

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
