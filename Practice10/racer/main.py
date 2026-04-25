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

# Screen and Game Variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS = 0

# Setup Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over_text = font.render("Game Over", True, WHITE)
restart_text = font_small.render("Press 'R' to Restart or 'Q' to Quit", True, WHITE)

# Load Sound Effects (using error handling just in case)
try:
    sound_coin = pygame.mixer.Sound('coin.wav')
    sound_crash = pygame.mixer.Sound('crash.wav')
except FileNotFoundError:
    sound_coin = None
    sound_crash = None

# Load background image
try:
    background = pygame.image.load("AnimatedStreet.png")
except FileNotFoundError:
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill(BLACK) 

# Create display
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer Game")

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
        # Respawn at top and add score when enemy passes the screen
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
        # Keep player within screen bounds
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load("Coin.png")
        except FileNotFoundError:
            self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
            pygame.draw.circle(self.image, YELLOW, (15, 15), 15)
            
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), random.randint(-100, -40))
        
    def move(self):
        self.rect.move_ip(0, SPEED)
        # Respawn coin if missed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(-100, -40))

# Helper function to reset game variables
def reset_game():
    global SCORE, COINS, SPEED
    SCORE = 0
    COINS = 0
    SPEED = 5
    P1.rect.center = (160, 520)
    E1.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)
    C1.rect.center = (random.randint(40, SCREEN_WIDTH-40), random.randint(-100, -40))

# Initialize Sprites
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Sprite Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Custom Event for increasing speed
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Game State Variable
game_state = "PLAYING"

# --- MAIN GAME LOOP ---
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        # Increase speed only when actively playing
        if game_state == "PLAYING":
            if event.type == INC_SPEED:
                  SPEED += 0.5      
                  
        # Menu navigation on Game Over
        elif game_state == "GAME_OVER":
            if event.type == KEYDOWN:
                if event.key == K_r:
                    reset_game()
                    game_state = "PLAYING"
                elif event.key == K_q:
                    pygame.quit()
                    sys.exit()

    # --- PLAYING STATE ---
    if game_state == "PLAYING":
        DISPLAYSURF.blit(background, (0,0))
        
        # Render Enemy Avoidance Score (White Text)
        scores = font_small.render(str(SCORE), True, WHITE)
        DISPLAYSURF.blit(scores, (10,10))
        
        # Render Collected Coins Score (White Text)
        coins_text = font_small.render(f"Coins: {COINS}", True, WHITE)
        text_x_pos = SCREEN_WIDTH - coins_text.get_width() - 10
        DISPLAYSURF.blit(coins_text, (text_x_pos, 10))

        # Move and Draw Entities
        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)
            entity.move()

        # --- COLLISION LOGIC ---
        
        # 1. Coin Collection
        collected_coins = pygame.sprite.spritecollide(P1, coins, False)
        for coin in collected_coins:
            if sound_coin:
                sound_coin.play() # PLAY COIN SOUND
            COINS += 1 
            coin.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(-100, -40))

        # 2. Enemy Collision
        if pygame.sprite.spritecollideany(P1, enemies):
            if sound_crash:
                sound_crash.play() # PLAY CRASH SOUND
            game_state = "GAME_OVER"
            
    # --- GAME OVER STATE ---
    elif game_state == "GAME_OVER":
        DISPLAYSURF.fill(RED)
        
        # Center texts on screen
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 20))
        
        DISPLAYSURF.blit(game_over_text, game_over_rect)
        DISPLAYSURF.blit(restart_text, restart_rect)

    pygame.display.update()
    FramePerSec.tick(FPS)