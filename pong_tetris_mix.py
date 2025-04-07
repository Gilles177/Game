import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Sound setup
pygame.mixer.init()
ball_hit_sound = pygame.mixer.Sound("assets/sounds/hit.wav")
block_hit_sound = pygame.mixer.Sound("assets/sounds/block.wav")
game_over_sound = pygame.mixer.Sound("assets/sounds/game_over.wav")

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong + Tetris Mix")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
BLUE  = (30, 144, 255)
GREY  = (100, 100, 100)
BG_COLOR = (20, 20, 30)

# Fonts
font = pygame.font.SysFont("Arial", 36)
title_font = pygame.font.SysFont("Arial", 48, bold=True)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Paddle
paddle = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 20, 120, 10)
paddle_speed = 8

# Ball
ball = pygame.Rect(WIDTH // 2 - 10, HEIGHT - 40, 20, 20)
ball_speed = [5, -5]

# Falling blocks (Tetris-style)
block_width = 40
block_height = 20
blocks = []
spawn_timer = 0
spawn_delay = 1000  # milliseconds

# Score
score = 0

# Screenshot counter
screenshot_count = 0
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

def spawn_block():
    x = random.randint(0, (WIDTH - block_width) // block_width) * block_width
    blocks.append(pygame.Rect(x, -block_height, block_width, block_height))

def draw():
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    for block in blocks:
        pygame.draw.rect(screen, GREY, block)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

def show_intro():
    screen.fill(BG_COLOR)
    title = title_font.render("Pong + Tetris Mix", True, BLUE)
    byline = font.render("by Gilles G. Yamdeu Youtebo", True, WHITE)
    prompt = font.render("Press any key to start", True, GREY)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
    screen.blit(byline, (WIDTH // 2 - byline.get_width() // 2, HEIGHT // 3 + 60))
    screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 3 + 120))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

# --- Game starts ---
show_intro()

running = True
last_spawn = pygame.time.get_ticks()
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                pygame.image.save(screen, f"screenshots/screenshot_{screenshot_count}.png")
                screenshot_count += 1

    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += paddle_speed

    # Ball movement
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed[0] *= -1
    if ball.top <= 0:
        ball_speed[1] *= -1
    if ball.colliderect(paddle):
        ball_speed[1] *= -1
        ball.y = paddle.top - ball.height
        ball_hit_sound.play()

    # Ball falls below screen = game over
    if ball.bottom >= HEIGHT:
        game_over_sound.play()
        pygame.time.delay(2000)
        running = False

    # Block spawning
    now = pygame.time.get_ticks()
    if now - last_spawn > spawn_delay:
        spawn_block()
        last_spawn = now

    # Block movement
    for block in blocks:
        block.y += 2

    # Check block collision with paddle
    for block in blocks[:]:
        if block.colliderect(paddle):
            blocks.remove(block)
            score += 1
            block_hit_sound.play()

    draw()

pygame.quit()