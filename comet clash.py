import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Player
player_img = pygame.image.load('player.png')
player_width, player_height = 64, 64
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 100
player_speed = 1

# Player bullet
bullet_img = pygame.image.load('bullet.png')
bullet_width, bullet_height = 8, 24
bullet_speed = 10
bullets = []

# Enemy
enemy_img = pygame.image.load('enemy.png')
enemy_width, enemy_height = 64, 64
enemy_speed = 0.1
max_enemies = 3
enemies = []

# Score
score = 0
font = pygame.font.SysFont(None, 40)

# Function to draw text on screen
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Function to draw player
def draw_player(x, y):
    screen.blit(player_img, (x, y))

# Function to draw bullet
def draw_bullet(x, y):
    screen.blit(bullet_img, (x, y))

# Function to draw enemy
def draw_enemy(x, y):
    screen.blit(enemy_img, (x, y))

# Function to generate enemies
def generate_enemies():
    if len(enemies) < max_enemies:
        enemy_x = random.randint(0, WIDTH - enemy_width)
        enemy_y = random.randint(-HEIGHT, -enemy_height)
        enemies.append([enemy_x, enemy_y])

# Main game loop
running = True
spawn_timer = 0
enemy_speed_timer = 0
while running:
    screen.fill(BLACK)
    
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_x = player_x + player_width // 2 - bullet_width // 2
                bullet_y = player_y
                bullets.append([bullet_x, bullet_y])

    # Move player with mouse/touchpad
    player_x, _ = pygame.mouse.get_pos()
    player_x -= player_width // 2
    if player_x < 0:
        player_x = 0
    elif player_x > WIDTH - player_width:
        player_x = WIDTH - player_width

    # Draw player
    draw_player(player_x, player_y)

    # Generate enemies
    spawn_timer += 1
    if spawn_timer >= 60:  # Adjust the value to control enemy spawn frequency
        generate_enemies()
        spawn_timer = 0

    # Move and draw bullets
    for bullet in bullets:
        bullet[1] -= bullet_speed
        draw_bullet(bullet[0], bullet[1])

    # Move and draw enemies
    for enemy in enemies:
        enemy[1] += enemy_speed
        draw_enemy(enemy[0], enemy[1])
        
        # Check for collision with player
        if (player_x < enemy[0] + enemy_width and 
            player_x + player_width > enemy[0] and 
            player_y < enemy[1] + enemy_height and 
            player_y + player_height > enemy[1]):
            running = False

        # Check for collision with bullets
        for bullet in bullets:
            if (bullet[0] < enemy[0] + enemy_width and
                bullet[0] + bullet_width > enemy[0] and
                bullet[1] < enemy[1] + enemy_height and
                bullet[1] + bullet_height > enemy[1]):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1
                break

        # Remove enemies that are off the screen
        if enemy[1] > HEIGHT:
            enemies.remove(enemy)

    # Draw score
    draw_text("Score: " + str(score), font, WHITE, 10, 10)

    # Increase enemy speed based on score
    if score > 0 and score % 10 == 0:
        enemy_speed_timer += 0.1
        if enemy_speed_timer >= 60:
            enemy_speed += 0.01
            enemy_speed_timer = 0

    pygame.display.update()

# Game over
screen.fill(BLACK)
draw_text("Game Over", font, RED, WIDTH//2 - 100, HEIGHT//2 - 20)
draw_text("Your Score: " + str(score), font, WHITE, WIDTH//2 - 100, HEIGHT//2 + 20)
pygame.display.update()

# Delay before quitting
pygame.time.delay(2000)

# Quit Pygame
pygame.quit()
sys.exit()
