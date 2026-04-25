import pygame, random, time
from pygame.locals import *

pygame.init()

# Colors & Config
C_SNAKE = (50, 205, 50)  # Lime Green
C_HEAD = (34, 139, 34)   # Forest Green
C_FOOD = (255, 0, 0)
C_BG = (20, 20, 30)
C_TEXT_WHITE = (255, 255, 255)
C_TEXT_RED = (213, 50, 80)
BLOCK = 20
WIDTH, HEIGHT = 600, 400

display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Fonts
font_style = pygame.font.SysFont("Verdana", 20, bold=True)
font_menu = pygame.font.SysFont("Verdana", 25, bold=True)

def draw_snake(snake_list, direction):
    """Draws the snake: head with eyes and rounded body"""
    for i, x in enumerate(snake_list):
        if i == len(snake_list) - 1: # HEAD
            pygame.draw.rect(display, C_HEAD, [x[0], x[1], BLOCK, BLOCK], border_radius=6)
            # Eyes direction logic
            eye_c = (255, 255, 255)
            if direction == "UP":
                pygame.draw.circle(display, eye_c, (x[0]+5, x[1]+5), 3)
                pygame.draw.circle(display, eye_c, (x[0]+15, x[1]+5), 3)
            elif direction == "DOWN":
                pygame.draw.circle(display, eye_c, (x[0]+5, x[1]+15), 3)
                pygame.draw.circle(display, eye_c, (x[0]+15, x[1]+15), 3)
            elif direction == "LEFT":
                pygame.draw.circle(display, eye_c, (x[0]+5, x[1]+5), 3)
                pygame.draw.circle(display, eye_c, (x[0]+5, x[1]+15), 3)
            else: # RIGHT
                pygame.draw.circle(display, eye_c, (x[0]+15, x[1]+5), 3)
                pygame.draw.circle(display, eye_c, (x[0]+15, x[1]+15), 3)
        else: # BODY
            pygame.draw.rect(display, C_SNAKE, [x[0]+2, x[1]+2, BLOCK-4, BLOCK-4], border_radius=4)

def show_message(msg, color, y_displace=0):
    """Helper function to render centered text"""
    mesg = font_menu.render(msg, True, color)
    text_rect = mesg.get_rect(center=(WIDTH/2, HEIGHT/2 + y_displace))
    display.blit(mesg, text_rect)

def gameLoop():
    game_over = False
    game_close = False

    x1, y1 = WIDTH/2, HEIGHT/2
    x1_c, y1_c = 0, 0
    snake_List = []
    Length_of_snake = 1
    score = 0
    level = 1
    speed = 10
    direction = "RIGHT"
    
    # Initial food placement
    fx = round(random.randrange(0, WIDTH - BLOCK) / BLOCK) * BLOCK
    fy = round(random.randrange(0, HEIGHT - BLOCK) / BLOCK) * BLOCK

    while not game_over:

        # --- GAME OVER MENU LOOP ---
        while game_close:
            display.fill(C_BG)
            show_message("You Lost!", C_TEXT_RED, -30)
            show_message("Press C to Play Again or Q to Quit", C_TEXT_WHITE, 10)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_q:
                        game_over = True
                        game_close = False
                    if event.key == K_c:
                        gameLoop() # Restart game
                if event.type == QUIT:
                    game_over = True
                    game_close = False

        # --- MAIN PLAYING LOOP ---
        for event in pygame.event.get():
            if event.type == QUIT: 
                game_over = True
            if event.type == KEYDOWN:
                if event.key == K_LEFT and x1_c == 0: x1_c, y1_c, direction = -BLOCK, 0, "LEFT"
                elif event.key == K_RIGHT and x1_c == 0: x1_c, y1_c, direction = BLOCK, 0, "RIGHT"
                elif event.key == K_UP and y1_c == 0: x1_c, y1_c, direction = 0, -BLOCK, "UP"
                elif event.key == K_DOWN and y1_c == 0: x1_c, y1_c, direction = 0, BLOCK, "DOWN"

        # Wall collision -> Triggers Game Over
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0: 
            game_close = True

        x1 += x1_c
        y1 += y1_c
        display.fill(C_BG)
        
        # Grid Background for aesthetics
        for x in range(0, WIDTH, BLOCK):
            pygame.draw.line(display, (40, 40, 50), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, BLOCK):
            pygame.draw.line(display, (40, 40, 50), (0, y), (WIDTH, y))

        # Draw Food
        pygame.draw.circle(display, C_FOOD, (int(fx+BLOCK/2), int(fy+BLOCK/2)), int(BLOCK/2 - 2))
        
        # Snake logic
        head = [x1, y1]
        snake_List.append(head)
        if len(snake_List) > Length_of_snake: 
            del snake_List[0]

        # Self collision -> Triggers Game Over
        for x in snake_List[:-1]:
            if x == head: 
                game_close = True

        draw_snake(snake_List, direction)
        
        # Stats Overlay
        pygame.draw.rect(display, (0,0,0), [5, 5, 110, 55], border_radius=5)
        s_txt = font_style.render(f"Score: {score}", True, C_TEXT_WHITE)
        l_txt = font_style.render(f"Level: {level}", True, (255, 215, 0))
        display.blit(s_txt, (10, 10))
        display.blit(l_txt, (10, 32))

        pygame.display.update()

        # Eating food logic
        if x1 == fx and y1 == fy:
            fx = round(random.randrange(0, WIDTH - BLOCK) / BLOCK) * BLOCK
            fy = round(random.randrange(0, HEIGHT - BLOCK) / BLOCK) * BLOCK
            Length_of_snake += 1
            score += 1
            if score % 3 == 0:
                level += 1
                speed += 2

        clock.tick(speed)

    pygame.quit()
    quit()

gameLoop()