import pygame

def ask_scale(pid, phase, time_sec):
    while True:
        try:
            rating = int(input(f"\nParticipant {pid} - {phase.upper()} phase @ {time_sec}s\nRate your stress (1–5): "))
            if 1 <= rating <= 5:
                return {"phase": phase, "time_sec": time_sec, "rating": rating}
            else:
                print("Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number.")



def ask_scale_pygame(pid, phase, time_sec, screen=None):
    if screen is None or not pygame.display.get_init():
        pygame.display.init()
        WIDTH, HEIGHT = 800, 600
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
    else:
        WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Stress Rating")
    FONT = pygame.font.SysFont(None, 60)

    def draw_text(text, y_offset=0):
        text_surface = FONT.render(text, True, (0, 0, 0))
        rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
        screen.blit(text_surface, rect)

    rating = None
    while rating is None:
        screen.fill((255, 255, 255))
        draw_text("Rate your stress (1–5):", y_offset=-40)
        draw_text("Press a number key", y_offset=40)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.KEYDOWN:
                if event.unicode in ['1', '2', '3', '4', '5']:
                    rating = int(event.unicode)

    pygame.quit()
    return {"phase": phase, "time_sec": time_sec, "rating": rating}
