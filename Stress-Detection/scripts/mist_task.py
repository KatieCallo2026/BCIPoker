import time
import random

def generate_question(elapsed_sec):
    if elapsed_sec < 60:
        # Easy: +/-, small numbers
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        op = random.choice(['+', '-'])
        
    elif elapsed_sec < 180:
        # Medium: +/-, medium numbers
        a = random.randint(10, 30)
        b = random.randint(10, 30)
        op = random.choice(['+', '-'])

    elif elapsed_sec < 270:
        # Harder: mix of +/- (medium) and * (small)
        op = random.choice(['+', '-', '*'])
        if op in ['+', '-']:
            a = random.randint(20, 40)
            b = random.randint(20, 40)
        else:  # '*'
            a = random.randint(2, 5)
            b = random.randint(5, 10)

    else:
        # Hardest: mix of +/- (large) and * (large)
        op = random.choice(['+', '-', '*'])
        if op in ['+', '-']:
            a = random.randint(30, 60)
            b = random.randint(30, 60)
        else:  # '*'
            a = random.randint(6, 12)
            b = random.randint(10, 20)

    question = f"{a} {op} {b}"
    answer = eval(question)
    return question, answer

    question = f"{a} {op} {b}"
    answer = eval(question)
    return question, answer


def run(duration_sec=60, timed=True):
    print(f"\nStarting MIST Task for {duration_sec} seconds...")
    start = time.time()
    correct = 0
    attempted = 0

    while time.time() - start < duration_sec:
        question, answer = generate_question()
        print(f"\nSolve: {question}")
        t0 = time.time()

        try:
            user_input = input("Your answer: ")
            elapsed = time.time() - t0

            if timed and elapsed > 5:  # simulate pressure
                print("⏱ Too slow!")
            elif int(user_input.strip()) == answer:
                print("✅ Correct!")
                correct += 1
            else:
                print("❌ Incorrect!")
        except:
            print("⚠️ Invalid input")

        attempted += 1

        # Mock "verbal" pressure
        if attempted % 3 == 0:
            print("Come on, try harder!")
        elif attempted % 5 == 0:
            print("Your performance is below expectations...")

    print(f"\nMIST complete. Score: {correct}/{attempted}")
