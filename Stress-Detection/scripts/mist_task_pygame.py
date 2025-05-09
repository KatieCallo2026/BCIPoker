import pygame
import random
import time
import sys

pygame.init()

# Window setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MIST Task")
FONT = pygame.font.SysFont(None, 60)
SMALL_FONT = pygame.font.SysFont(None, 40)
CLOCK = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 205, 50)
RED = (220, 20, 60)
YELLOW = (255, 215, 0)

def draw_text(text, size=60, color=BLACK, y_offset=0):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(text_surface, rect)

def generate_question(level):
    if level == "easy":
        a, b = random.randint(1, 10), random.randint(1, 10)
        op = random.choice(['+', '-'])
    elif level == "medium":
        a, b = random.randint(10, 30), random.randint(10, 30)
        op = random.choice(['+', '-'])
    else:
        op = random.choice(['+', '-', '*'])
        a, b = (random.randint(6, 12), random.randint(10, 20)) if op == '*' else (random.randint(30, 60), random.randint(30, 60))
    question = f"{a} {op} {b}"
    return question, eval(question)

def run_pygame_mist(duration_sec=60, difficulty="mist_1"):
    start_time = time.time()
    correct = 0
    attempted = 0
    feedback = ""
    feedback_color = BLACK
    pressure = ""
    answer_input = ""
    show_feedback_until = 0

    level = "easy" if "1" in difficulty else "medium" if "2" in difficulty else "hard"
    question, correct_answer = generate_question(level)

    running = True
    while running and time.time() - start_time < duration_sec:
        screen.fill(WHITE)

        # Time management
        current_time = time.time()
        remaining = max(0, int(duration_sec - (current_time - start_time)))
        draw_text(f"Time Left: {remaining}s", size=40, y_offset=-240)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                return screen

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    attempted += 1
                    try:
                        if answer_input.strip() == "":
                            feedback = "⏱ Too slow!"
                            feedback_color = YELLOW
                        elif int(answer_input.strip()) == correct_answer:
                            feedback = "✅ Correct!"
                            feedback_color = GREEN
                            correct += 1
                        else:
                            feedback = "❌ Incorrect!"
                            feedback_color = RED
                    except:
                        feedback = "⚠️ Invalid input"
                        feedback_color = RED

                    # Pressure comments
                    if attempted % 3 == 0:
                        pressure = "Come on, try harder!"
                    elif attempted % 5 == 0:
                        pressure = "Your performance is below expectations..."
                    else:
                        pressure = ""

                    answer_input = ""
                    show_feedback_until = time.time() + 1.5
                    question, correct_answer = generate_question(level)

                elif event.key == pygame.K_BACKSPACE:
                    answer_input = answer_input[:-1]
                elif event.unicode.isdigit() or (event.unicode == '-' and answer_input == ""):
                    answer_input += event.unicode

        # Display question
        draw_text(f"Solve: {question}", size=50, y_offset=-80)
        draw_text(f"Your Answer: {answer_input}", size=45, y_offset=20)

        # Feedback
        if time.time() < show_feedback_until:
            draw_text(feedback, size=45, color=feedback_color, y_offset=120)
            draw_text(pressure, size=30, color=BLACK, y_offset=200)

        pygame.display.flip()
        CLOCK.tick(30)

    # End of session
    screen.fill(WHITE)
    draw_text(f"MIST complete!", size=60, y_offset=-60)
    draw_text(f"Score: {correct}/{attempted}", size=50, y_offset=30)
    pygame.display.flip()
    time.sleep(4)
    
    return pygame.display.get_surface()

if __name__ == "__main__":
    run_mist(duration_sec=60, difficulty="mist_1")
