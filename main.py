import random
import pygame


def main():
    # Setup
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    pygame.display.set_caption("Game")
    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()

    # Variables
    game_over = False
    bullet_speed = 4
    spawn_locations = [(0, 395), (395, 0), (395, 792), (792, 395)]
    counter = 0
    score = 0
    health = 5
    player = pygame.Rect(383, 383, 32, 8)
    hit_box = pygame.Rect(383, 383, 32, 32)
    bullets = []

    # Classes
    class Bullet:
        def __init__(self, rectangle, direction):
            self.rectangle = rectangle
            self.direction = direction

    # Functions
    def handle_quitting(pygame_event):
        if pygame_event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if pygame_event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    def handle_turning(key):
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

    def move_bullets():
        for bullet in bullets:
            if bullet.direction == 0:
                bullet.rectangle.x += bullet_speed
            elif bullet.direction == 1:
                bullet.rectangle.y += bullet_speed
            elif bullet.direction == 2:
                bullet.rectangle.y -= bullet_speed
            elif bullet.direction == 3:
                bullet.rectangle.x -= bullet_speed

    def spawn_bullets():
        position = random.choice(spawn_locations)
        spawn_side = spawn_locations.index(position)
        bullets.append(Bullet(rectangle=pygame.Rect(position[0], position[1], 8, 8), direction=spawn_side))

    def check_collisions(game_score, game_health):
        for x, bullet in enumerate(bullets):
            if player.colliderect(bullet.rectangle):
                del bullets[x]
                game_score += 1
            elif hit_box.colliderect(bullet.rectangle):
                del bullets[x]
                game_health -= 1
        return game_score, game_health

    def game_over_check(game_health):
        if game_health > 0:
            return False
        return True

    def render_game(ended):
        screen.fill((255, 255, 255))
        font = pygame.font.SysFont("", 48)
        if not ended:
            # Text
            score_text = font.render(f"Score: {score}", True, (0, 0, 0))
            health_text = font.render(f"Lives: {health}", True, (0, 0, 0))
            screen.blit(score_text, (20, 20))
            screen.blit(health_text, (20, 68))
            # Objects
            pygame.draw.rect(screen, (0, 0, 0), hit_box, 2)
            pygame.draw.rect(screen, (255, 0, 0), player)
            for bullet in bullets:
                pygame.draw.rect(screen, (0, 0, 255), bullet.rectangle)
        else:
            font = pygame.font.SysFont("", 80)
            end_text0 = font.render(f"Game Over!", True, (0, 0, 0))
            font = pygame.font.SysFont("", 64)
            end_text1 = font.render(f"You scored: {score}", True, (0, 0, 0))
            screen.blit(end_text0, (240, 256))
            screen.blit(end_text1, (260, 364))
        pygame.display.update()

    # Game loop
    while True:
        if not game_over:
            # Reset or increment counter
            if counter == 30:
                counter = 0
            else:
                counter += 1
            # Gets input
            for event in pygame.event.get():
                handle_quitting(event)
                if event.type == pygame.KEYDOWN:
                    handle_turning(event.key)
            # Calculate things
            move_bullets()
            if counter == 30:
                spawn_bullets()
            score, health = check_collisions(score, health)
            game_over = game_over_check(health)
            # Update screen
            render_game(game_over)
            clock.tick(60)  # Frame rate
        else:
            # Handle quitting
            for event in pygame.event.get():
                handle_quitting(event)


if __name__ == "__main__":
    main()
