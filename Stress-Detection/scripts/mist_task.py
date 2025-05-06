import time
import random

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
    answer = eval(question)
    return question, answer

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
        t0 = time.time()

        try:
            user_input = input("Your answer: ")
            response_time = time.time() - t0

            if timed and response_time > 5:
                print("\u23F1 Too slow!")
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
