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

    # Variables
    player = pygame.Rect(383, 383, 32, 8)

    def move(key):
        if key == pygame.K_w:
            player.size = (32, 8)
            player.x = 383
            player.y = 383
        if key == pygame.K_s:
            player.size = (32, 8)
            player.x = 383
            player.y = 407
        if key == pygame.K_a:
            player.size = (8, 32)
            player.x = 383
            player.y = 383
        if key == pygame.K_d:
            player.size = (8, 32)
            player.x = 407
            player.y = 383

    # Game loop
    while True:
        # Gets input
        for event in pygame.event.get():
            # Handle quitting
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                # Handle useful input
                move(event.key)

        # Do stuff

        # Updates screen
        screen.fill(WHITE)
        pygame.draw.rect(screen, (255, 0, 0), player)
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
