import pygame
import random

FPS = 240  # Max is 240, Min is 30, Recommended is 240


def main():
    # Setup
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    pygame.display.set_caption("Game")
    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()

    # Constants
    hit_box = pygame.Rect(383, 383, 32, 32)
    fifteen_seconds = FPS * 15
    frame_interval = 240 // FPS
    delay = FPS
    max_speed = frame_interval*4
    spawn_locations = [(-8, 395), (395, -8), (395, 800), (800, 395)]

    # Variables
    player = pygame.Rect(383, 383, 32, 8)
    waiting = False
    running = True
    delay_counter = 0
    counter = 0
    score = 0
    health = 0
    bullets = []

    # Classes
    class Bullet:
        def __init__(self, rectangle, direction):
            self.rectangle = rectangle
            self.direction = direction
            self.speed = bullet_speed

    # Functions
    def handle_quitting(pygame_event):
        if pygame_event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if pygame_event.type == pygame.KEYDOWN:
            if pygame_event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    def adjust_difficulty(new_delay):
        frame_delay = new_delay - (new_delay*frame_interval/8000)
        pixel_per_frame = frame_interval + counter // fifteen_seconds * frame_interval
        if pixel_per_frame > max_speed:
            pixel_per_frame = max_speed
        return frame_delay, pixel_per_frame

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
        speeds = set(bullet.speed for bullet in bullets)
        wait = False
        for x, bullet in enumerate(bullets):
            if min(speeds) < bullet.speed:
                del bullets[x]
                wait = True
                continue
            if bullet.direction == 0:
                bullet.rectangle.x += bullet.speed
            elif bullet.direction == 1:
                bullet.rectangle.y += bullet.speed
            elif bullet.direction == 2:
                bullet.rectangle.y -= bullet.speed
            elif bullet.direction == 3:
                bullet.rectangle.x -= bullet.speed
        return wait

    def spawn_bullets():
        if not waiting:
            position = random.choice(spawn_locations)
            spawn_side = spawn_locations.index(position)
            bullets.append(Bullet(rectangle=pygame.Rect(position[0], position[1], 8, 8), direction=spawn_side))

    def check_collisions(game_score, game_health):
        for x, bullet in enumerate(bullets):
            if player.colliderect(bullet.rectangle):
                del bullets[x]
                game_score += 1
                pygame.mixer.music.load("Assets/block.wav")
                pygame.mixer.music.play()
            elif hit_box.colliderect(bullet.rectangle):
                del bullets[x]
                game_health -= 1
                pygame.mixer.music.load("Assets/hit.wav")
                pygame.mixer.music.play()
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
            pygame.display.update()
            return True
        else:
            # Read and write scores
            with open("scores.txt", "a") as file:
                file.write(f"{score}:")
            with open("scores.txt", "r") as file:
                scores = file.read().split(":")
                highscore = max(scores)
            # Play game over sound
            pygame.mixer.music.load("Assets/game_over.wav")
            pygame.mixer.music.play()
            main_menu = True
            while main_menu:
                screen.fill((255, 255, 255))
                # Render text
                font = pygame.font.SysFont("", 96)
                end_text0 = font.render(f"Game Over!", True, (0, 0, 0))
                font = pygame.font.SysFont("", 64)
                end_text1 = font.render(f"You scored: {score}", True, (0, 0, 0))
                end_text2 = font.render(f"Highscore: {highscore}", True, (0, 0, 0))
                end_text3 = font.render(f"Restart", True, (0, 0, 0))
                if pygame.Rect(310, 453, 200, 64).collidepoint(pygame.mouse.get_pos()):
                    restart_button_color = (40, 160, 40)
                else:
                    restart_button_color = (32, 128, 32)
                pygame.draw.rect(screen, restart_button_color, pygame.Rect(310, 453, 200, 64))
                screen.blit(end_text0, (210, 240))
                screen.blit(end_text1, (260, 320))
                screen.blit(end_text2, (270, 380))
                screen.blit(end_text3, (330, 464))
                # Handle quitting
                for key in pygame.event.get():
                    if key.type == pygame.MOUSEBUTTONDOWN and restart_button_color == (40, 160, 40):
                        return False
                    handle_quitting(key)
                pygame.display.update()

    while True:
        # Game loop
        while running:
            delay, bullet_speed = adjust_difficulty(delay)
            # Reset or increment counter
            if delay_counter >= delay:
                delay_counter = 0
            else:
                delay_counter += 1
                counter += 1
            # Gets input
            for event in pygame.event.get():
                handle_quitting(event)
                if event.type == pygame.KEYDOWN:
                    handle_turning(event.key)
            # Calculate things
            waiting = move_bullets()
            if delay_counter >= delay:
                spawn_bullets()
            score, health = check_collisions(score, health)
            game_over = game_over_check(health)
            # Update screen
            running = render_game(game_over)
            clock.tick(FPS)  # Frame rate

        # Variables
        player = pygame.Rect(383, 383, 32, 8)
        waiting = False
        running = True
        delay_counter = 0
        counter = 0
        score = 0
        health = 5
        bullets = []


if __name__ == "__main__":
    main()
