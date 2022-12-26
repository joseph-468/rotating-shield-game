import pygame

# CONSTANTS
WIDTH, HEIGHT = 800, 800
FPS = 60
WHITE = (255, 255, 255)


def main():
    # Setup
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    pygame.display.set_caption("Game")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Game loop
    while True:
        # Gets input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

        # Updates screen
        screen.fill(WHITE)
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
