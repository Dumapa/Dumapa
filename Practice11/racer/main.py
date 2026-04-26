import pygame, sys
from pygame.locals import *
import random

# Initialize pygame and mixer for audio
pygame.init()
pygame.mixer.init()

# Setup FPS 
FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)

# Practice 11 Colors for weighted coins
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)

# Screen and Game Variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS = 0
N = 5 # TASK: Increase speed every N coins collected

# Setup Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over_text = font.render("Game Over", True, WHITE)
restart_text = font_small.render("Press 'R' to Restart or 'Q' to Quit", True, WHITE)

# Load Sound Effects
try:
    sound_coin = pygame.mixer.Sound('coin.wav')
    sound_crash = pygame.mixer.Sound('crash.wav')
except FileNotFoundError:
    sound_coin = None
    sound_crash = None

# Load original background
try:
    background = pygame.image.load("AnimatedStreet.png")
except FileNotFoundError:
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill(BLACK) 

# Create display
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer Game - Practice 11")

# --- CLASSES ---

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        try:
            self.image = pygame.image.load("Enemy.png")
        except FileNotFoundError:
            self.image = pygame.Surface((40, 60))
            self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > SCREEN_HEIGHT):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        try:
            self.image = pygame.image.load("Player.png")
        except FileNotFoundError:
            self.image = pygame.Surface((40, 60))
            self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # TASK 1: Generating coins with different weights (1, 2, or 3)
        # Instead of a single image, we create 3 different visuals automatically
        self.coin_images = {
            1: self.make_coin_img(BRONZE, 15), # Weight 1: Small Bronze
            2: self.make_coin_img(SILVER, 20), # Weight 2: Medium Silver
            3: self.make_coin_img(YELLOW, 25)  # Weight 3: Large Gold
        }
        self.spawn()

    def make_coin_img(self, color, radius):
        """Helper to 'draw' new coin images since we are lazy to use Photoshop"""
        surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(surf, color, (radius, radius), radius)
        # Add a border for better look
        pygame.draw.circle(surf, BLACK, (radius, radius), radius, 2)
        return surf

    def spawn(self):
        # Randomly choose weight for the new coin
        self.weight = random.choices([1, 2, 3], weights=[60, 30, 10])[0]
        self.image = self.coin_images[self.weight]
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), random.randint(-100, -40))

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn()

# Helper function to reset game variables
def reset_game():
    global SCORE, COINS, SPEED
    SCORE = 0
    COINS = 0
    SPEED = 5
    P1.rect.center = (160, 520)
    E1.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)
    C1.spawn()

# Initialize Sprites
P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Game State Variable
game_state = "PLAYING"

# --- MAIN GAME LOOP ---
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        elif game_state == "GAME_OVER":
            if event.type == KEYDOWN:
                if event.key == K_r:
                    reset_game()
                    game_state = "PLAYING"
                elif event.key == K_q:
                    pygame.quit()
                    sys.exit()

    if game_state == "PLAYING":
        DISPLAYSURF.blit(background, (0,0))
        
        # UI Rendering
        scores = font_small.render(f"Score: {SCORE}", True, WHITE)
        coins_text = font_small.render(f"Coins: {COINS}", True, YELLOW)
        speed_text = font_small.render(f"Speed: {SPEED:.1f}", True, GREEN)
        
        DISPLAYSURF.blit(scores, (10,10))
        DISPLAYSURF.blit(coins_text, (SCREEN_WIDTH - 120, 10))
        DISPLAYSURF.blit(speed_text, (SCREEN_WIDTH - 120, 35))

        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)
            entity.move()

        # --- COLLISION LOGIC ---
        
        # Coin Collection
        collected = pygame.sprite.spritecollide(P1, coins, False)
        for coin in collected:
            if sound_coin:
                sound_coin.play()
            
            # Save old count to check for milestone
            old_milestone = COINS // N
            COINS += coin.weight 
            new_milestone = COINS // N
            
            # TASK 2: Increase the speed of Enemy when the player earns N coins
            if new_milestone > old_milestone:
                SPEED += 0.5
                
            coin.spawn()

        # Enemy Collision
        if pygame.sprite.spritecollideany(P1, enemies):
            if sound_crash:
                sound_crash.play()
            game_state = "GAME_OVER"
            
    elif game_state == "GAME_OVER":
        DISPLAYSURF.fill(RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 20))
        DISPLAYSURF.blit(game_over_text, game_over_rect)
        DISPLAYSURF.blit(restart_text, restart_rect)

    pygame.display.update()
    FramePerSec.tick(FPS)