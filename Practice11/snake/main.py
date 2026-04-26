import pygame, random, time
from pygame.locals import *

pygame.init()
WIDTH, HEIGHT = 600, 400
BLOCK = 20
display = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font_style = pygame.font.SysFont("Verdana", 20)

# Colors
C_SNAKE = (50, 205, 50); C_BG = (20, 20, 30)
FOOD_COLORS = {1: (255, 0, 0), 2: (0, 255, 255), 3: (255, 215, 0)}

def gameLoop():
    game_over = game_close = False
    x, y = WIDTH/2, HEIGHT/2
    dx, dy = 0, 0
    snake_List = []; length = 1
    score = 0; speed = 10

    # Food Setup
    def spawn_food():
        fx = round(random.randrange(0, WIDTH - BLOCK) / BLOCK) * BLOCK
        fy = round(random.randrange(0, HEIGHT - BLOCK) / BLOCK) * BLOCK
        # TASK 1: Food with different weights
        weight = random.randint(1, 3)
        # TASK 2: Timer - store spawn time
        spawn_time = pygame.time.get_ticks()
        return fx, fy, weight, spawn_time

    fx, fy, f_weight, f_time = spawn_food()

    while not game_over:
        while game_close:
            display.fill(C_BG)
            msg = font_style.render("Lost! Press C-Play or Q-Quit", True, (255,255,255))
            display.blit(msg, [WIDTH/4, HEIGHT/2])
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_q: game_over = True; game_close = False
                    if event.key == K_c: gameLoop()

        for event in pygame.event.get():
            if event.type == QUIT: game_over = True
            if event.type == KEYDOWN:
                if event.key == K_LEFT and dx == 0: dx, dy = -BLOCK, 0
                elif event.key == K_RIGHT and dx == 0: dx, dy = BLOCK, 0
                elif event.key == K_UP and dy == 0: dx, dy = 0, -BLOCK
                elif event.key == K_DOWN and dy == 0: dx, dy = 0, BLOCK

        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0: game_close = True
        x += dx; y += dy
        display.fill(C_BG)

        # TASK 2: Timer Logic - food disappears after 5 seconds
        current_time = pygame.time.get_ticks()
        if current_time - f_time > 5000: # 5000ms = 5s
            fx, fy, f_weight, f_time = spawn_food()

        # Draw Food
        pygame.draw.rect(display, FOOD_COLORS[f_weight], [fx, fy, BLOCK, BLOCK])
        # Visual Timer Bar
        timer_width = BLOCK * (1 - (current_time - f_time) / 5000)
        pygame.draw.rect(display, (255,255,255), [fx, fy-5, timer_width, 3])

        snake_List.append([x, y])
        if len(snake_List) > length: del snake_List[0]
        for part in snake_List[:-1]:
            if part == [x, y]: game_close = True

        for part in snake_List:
            pygame.draw.rect(display, C_SNAKE, [part[0], part[1], BLOCK, BLOCK])

        # Eating Logic
        if x == fx and y == fy:
            score += f_weight
            length += f_weight
            fx, fy, f_weight, f_time = spawn_food()
            speed += 1

        pygame.display.update()
        clock.tick(speed)

    pygame.quit(); quit()

if __name__ == "__main__":
    gameLoop()