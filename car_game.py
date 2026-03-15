import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CAR_WIDTH, CAR_HEIGHT = 50, 100
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
GREEN = (0, 200, 0)

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Dodging Game")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 36)
large_font = pygame.font.SysFont("Arial", 72)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def draw_car(x, y, color):
    # Main body
    pygame.draw.rect(screen, color, (x, y, CAR_WIDTH, CAR_HEIGHT))
    # Wheels
    pygame.draw.rect(screen, BLACK, (x - 5, y + 10, 5, 20))
    pygame.draw.rect(screen, BLACK, (x + CAR_WIDTH, y + 10, 5, 20))
    pygame.draw.rect(screen, BLACK, (x - 5, y + CAR_HEIGHT - 30, 5, 20))
    pygame.draw.rect(screen, BLACK, (x + CAR_WIDTH, y + CAR_HEIGHT - 30, 5, 20))
    # Windows
    pygame.draw.rect(screen, (150, 200, 255), (x + 5, y + 15, CAR_WIDTH - 10, 25))
    pygame.draw.rect(screen, (150, 200, 255), (x + 5, y + CAR_HEIGHT - 35, CAR_WIDTH - 10, 20))

def show_start_screen():
    screen.fill(GREEN)
    draw_text("Car Racing", large_font, WHITE, screen, WIDTH // 2, HEIGHT // 4)
    draw_text("Press any key to start", font, WHITE, screen, WIDTH // 2, HEIGHT // 2)
    pygame.display.update()
    
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False

def show_game_over_screen(score):
    screen.fill(RED)
    draw_text("GAME OVER", large_font, WHITE, screen, WIDTH // 2, HEIGHT // 4)
    draw_text(f"Score: {score}", font, WHITE, screen, WIDTH // 2, HEIGHT // 2)
    draw_text("Press any key to play again", font, WHITE, screen, WIDTH // 2, HEIGHT * 3 // 4)
    pygame.display.update()
    
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False

def game_loop():
    # Player start position
    player_x = WIDTH // 2 - CAR_WIDTH // 2
    player_y = HEIGHT - CAR_HEIGHT - 20
    player_speed_x = 0
    player_speed_y = 0
    player_speed = 7

    # Enemy cars
    enemy_cars = []
    enemy_speed = 5
    spawn_rate = 60  # Frames between spawns
    frame_count = 0

    score = 0
    road_offset = 0

    running = True
    while running:
        clock.tick(FPS)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_speed_x = -player_speed
                if event.key == pygame.K_RIGHT:
                    player_speed_x = player_speed
                if event.key == pygame.K_UP:
                    player_speed_y = -player_speed
                if event.key == pygame.K_DOWN:
                    player_speed_y = player_speed
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_speed_x = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player_speed_y = 0

        # Update player position
        player_x += player_speed_x
        player_y += player_speed_y

        # Boundaries for player
        if player_x < 100:
            player_x = 100
        if player_x > WIDTH - 100 - CAR_WIDTH:
            player_x = WIDTH - 100 - CAR_WIDTH
        if player_y < 0:
            player_y = 0
        if player_y > HEIGHT - CAR_HEIGHT:
            player_y = HEIGHT - CAR_HEIGHT

        # Spawning enemies
        frame_count += 1
        if frame_count >= spawn_rate:
            frame_count = 0
            # Ensure enemy spawns within road (road is from 100 to WIDTH-100)
            enemy_x = random.randint(100, WIDTH - 100 - CAR_WIDTH)
            enemy_y = -CAR_HEIGHT
            enemy_color = random.choice([(255, 100, 100), (100, 255, 100), (100, 100, 255), (255, 255, 100), (255, 100, 255), (100, 255, 255)])
            enemy_cars.append([enemy_x, enemy_y, enemy_color])
            
            # Increase difficulty
            if score % 5 == 0 and score > 0:
                enemy_speed += 0.5
                if spawn_rate > 20:
                    spawn_rate -= 2

        # Update enemies
        for enemy in enemy_cars[:]:
            enemy[1] += enemy_speed
            if enemy[1] > HEIGHT:
                enemy_cars.remove(enemy)
                score += 1

        # Check collisions
        player_rect = pygame.Rect(player_x, player_y, CAR_WIDTH, CAR_HEIGHT)
        for enemy in enemy_cars:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], CAR_WIDTH, CAR_HEIGHT)
            if player_rect.colliderect(enemy_rect):
                running = False

        # Draw Background
        screen.fill(GREEN) # Grass
        
        # Road
        pygame.draw.rect(screen, DARK_GRAY, (100, 0, WIDTH - 200, HEIGHT))
        
        # Moving lines on road
        road_offset = (road_offset + enemy_speed) % 40
        for y in range(0, HEIGHT, 40):
            pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 5, y - road_offset, 10, 20))

        # Draw Enemies
        for enemy in enemy_cars:
            draw_car(enemy[0], enemy[1], enemy[2])

        # Draw Player
        draw_car(player_x, player_y, BLUE)

        # Draw Score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Update display
        pygame.display.flip()

    return score

def main():
    while True:
        show_start_screen()
        score = game_loop()
        show_game_over_screen(score)

if __name__ == "__main__":
    main()
