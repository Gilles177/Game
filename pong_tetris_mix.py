import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Try to initialize the mixer safely
try:
    pygame.mixer.init()
    sound_enabled = True
except pygame.error:
    print("⚠️ Warning: Audio device not available. Sound will be disabled.")
    sound_enabled = False

# Load sound effects only if mixer is initialized
if sound_enabled:
    ball_hit_sound = pygame.mixer.Sound("assets/sounds/hit.wav")
    block_hit_sound = pygame.mixer.Sound("assets/sounds/block.wav")
    game_over_sound = pygame.mixer.Sound("assets/sounds/game_over.wav")
    pygame.mixer.music.load("assets/sounds/music.wav")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
else:
    ball_hit_sound = block_hit_sound = game_over_sound = None

# Screen settings
WIDTH, HEIGHT = 1280, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong + Tetris Mix")

# Colors
WHITE = (255, 255, 255)
NEON_BLUE = (0, 255, 255)
NEON_PURPLE = (199, 21, 133)
BG_COLOR = (5, 5, 15)
BOSS_COLOR = (255, 0, 0)  # Boss color (red)

# Fonts
font = pygame.font.SysFont("Arial", 36, bold=True)
title_font = pygame.font.SysFont("Arial", 64, bold=True)

# Load background image and overlay
bg_image = pygame.image.load("assets/backgrounds/space_bg.jpg")
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
bg_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
bg_overlay.fill((0, 0, 0, 100))

# Clock
clock = pygame.time.Clock()
FPS = 60

# Paddle
paddle = pygame.Rect(WIDTH // 2 - 80, HEIGHT - 30, 160, 15)
paddle_speed = 10

# Ball
ball = pygame.Rect(WIDTH // 2 - 10, HEIGHT - 50, 20, 20)
ball_speed = [6, -6]

# Falling blocks (Tetris-style)
block_width = 50
block_height = 25
blocks = []
spawn_timer = 0
spawn_delay = 900  # milliseconds

# Score and level
score = 0
level = 1
MAX_POINTS_PER_LEVEL = 10

# Pause flag
paused = False

# Screenshot counter
screenshot_count = 0
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

# Boss Class
class Boss:
    def __init__(self):
        self.width = 200
        self.height = 50
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT // 4
        self.speed = 4
        self.health = 10  # Boss health
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        # Boss moves left and right
        self.x += self.speed
        if self.x <= 0 or self.x + self.width >= WIDTH:
            self.speed = -self.speed  # Reverse direction if it hits screen edge
        self.rect.x = self.x

    def draw(self):
        pygame.draw.rect(screen, BOSS_COLOR, self.rect)

# Particle system for block explosion
class Particle:
    def __init__(self, x, y, color, speed, size):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.size = size
        self.lifetime = 50  # Lifespan of the particle
    
    def update(self):
        self.x += self.speed[0]
        self.y += self.speed[1]
        self.lifetime -= 1
    
    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

# Particle list to hold particle effects
particles = []

def spawn_block():
    x = random.randint(0, (WIDTH - block_width) // block_width) * block_width
    blocks.append(pygame.Rect(x, -block_height, block_width, block_height))

def draw_glowing_text(text, font, color, pos, glow_color):
    base = font.render(text, True, color)
    glow = font.render(text, True, glow_color)
    for offset in [(2, 2), (-2, 2), (2, -2), (-2, -2)]:
        screen.blit(glow, (pos[0] + offset[0], pos[1] + offset[1]))
    screen.blit(base, pos)

def draw():
    screen.blit(bg_image, (0, 0))
    screen.blit(bg_overlay, (0, 0))
    pygame.draw.rect(screen, NEON_PURPLE, paddle, border_radius=6)
    pygame.draw.ellipse(screen, NEON_BLUE, ball)
    for block in blocks:
        pygame.draw.rect(screen, WHITE, block, border_radius=4)
    
    # Draw particles
    for particle in particles[:]:
        particle.update()
        particle.draw()
        if particle.lifetime <= 0:
            particles.remove(particle)
    
    # Draw Boss Health Bar
    if boss:
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 250, HEIGHT // 4 - 20, 500, 20))  # Health bar background
        pygame.draw.rect(screen, (255, 0, 0), (WIDTH // 2 - 250, HEIGHT // 4 - 20, (500 * boss.health) // 10, 20))  # Health bar

    draw_glowing_text(f"Score: {score} | Level: {level}", font, WHITE, (20, 20), NEON_PURPLE)
    
    if paused:
        draw_glowing_text("Paused", title_font, NEON_PURPLE, (WIDTH // 2 - 100, HEIGHT // 2), NEON_BLUE)
    
    pygame.display.flip()

def show_intro():
    screen.blit(bg_image, (0, 0))
    screen.blit(bg_overlay, (0, 0))
    draw_glowing_text("Pong + Tetris Mix", title_font, NEON_BLUE, (WIDTH // 2 - 300, HEIGHT // 3), WHITE)
    draw_glowing_text("by Gilles G. Yamdeu Youtebo", font, WHITE, (WIDTH // 2 - 250, HEIGHT // 3 + 80), NEON_PURPLE)
    draw_glowing_text("Press any key to start", font, NEON_PURPLE, (WIDTH // 2 - 220, HEIGHT // 3 + 160), WHITE)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

def show_game_over():
    screen.blit(bg_image, (0, 0))
    screen.blit(bg_overlay, (0, 0))
    draw_glowing_text("Game Over", title_font, NEON_PURPLE, (WIDTH // 2 - 160, HEIGHT // 3), NEON_BLUE)
    draw_glowing_text(f"Final Score: {score} | Level: {level}", font, WHITE, (WIDTH // 2 - 200, HEIGHT // 3 + 80), NEON_PURPLE)
    draw_glowing_text("Press R to Restart or Q to Quit", font, NEON_BLUE, (WIDTH // 2 - 260, HEIGHT // 3 + 160), WHITE)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main_game_loop()
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()

def main_game_loop():
    global score, level, blocks, ball, paddle, ball_speed, spawn_delay, paused, boss
    score = 0
    level = 1
    blocks = []
    ball.x = WIDTH // 2 - 10
    ball.y = HEIGHT - 50
    paddle.x = WIDTH // 2 - 80
    ball_speed = [6, -6]
    spawn_delay = 900
    paused = False
    running = True
    last_spawn = pygame.time.get_ticks()
    
    boss = None
    
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    pygame.image.save(screen, f"screenshots/screenshot_{screenshot_count}.png")
                elif event.key == pygame.K_p:
                    paused = not paused

        if paused:
            draw()
            continue

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.x += paddle_speed

        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        if ball.left <= 0 or ball.right >= WIDTH:
            ball_speed[0] *= -1
        if ball.top <= 0:
            ball_speed[1] *= -1
        if ball.colliderect(paddle):
            ball_speed[1] *= -1
            ball.y = paddle.top - ball.height
            if ball_hit_sound:
                ball_hit_sound.play()

        if ball.bottom >= HEIGHT:
            if game_over_sound:
                game_over_sound.play()
            pygame.time.delay(1000)
            show_game_over()
            return

        now = pygame.time.get_ticks()
        if now - last_spawn > spawn_delay:
            spawn_block()
            last_spawn = now

        for block in blocks:
            block.y += 3 + level

        for block in blocks[:]:
            if block.colliderect(paddle):
                blocks.remove(block)
                score += 1
                if block_hit_sound:
                    block_hit_sound.play()
                # Add particles when the block is destroyed
                for _ in range(10):  # Generate particles
                    particles.append(Particle(block.centerx, block.centery, NEON_BLUE, [random.randint(-2, 2), random.randint(-2, 2)], random.randint(2, 5)))
                if score % MAX_POINTS_PER_LEVEL == 0:
                    level += 1
                    spawn_delay = max(300, spawn_delay - 100)

        # Check if it's time to spawn the boss (after completing the level)
        if score >= MAX_POINTS_PER_LEVEL * level and boss is None:
            boss = Boss()

        # Boss fight logic
        if boss:
            boss.move()
            boss.draw()
            if ball.colliderect(boss.rect):
                boss.health -= 1
                if ball_hit_sound:
                    ball_hit_sound.play()
            if boss.health <= 0:
                boss = None
                score += 10  # Bonus points for defeating the boss
                pygame.time.delay(500)

        draw()

    pygame.quit()

# --- Game starts ---
show_intro()
main_game_loop()