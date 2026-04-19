import pygame

from ball import RADIUS, STEP, COLOR, BG_COLOR, WIDTH, HEIGHT

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball Game")
clock = pygame.time.Clock()


x = WIDTH // 2
y = HEIGHT // 2

running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_UP and (y - STEP - RADIUS) >= 0:
                y -= STEP
            
            elif event.key == pygame.K_DOWN and (y + STEP + RADIUS) <= HEIGHT:
                y += STEP
            
            elif event.key == pygame.K_LEFT and (x - STEP - RADIUS) >= 0:
                x -= STEP
            
            elif event.key == pygame.K_RIGHT and (x + STEP + RADIUS) <= WIDTH:
                x += STEP

    
    screen.fill(BG_COLOR)
    pygame.draw.circle(screen, COLOR, (x, y), RADIUS)
    pygame.display.flip()
    
    
    clock.tick(60)

pygame.quit()