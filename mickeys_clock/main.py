import pygame
import datetime

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey's Clock")
clock = pygame.time.Clock()

bg = pygame.image.load("images/mainclock.png").convert()
bg = pygame.transform.scale(bg, (600, 600))
left_hand = pygame.image.load("images/leftarm.png").convert_alpha()

right_hand = pygame.image.load("images/rightarm.png").convert_alpha()


def blit_rotate_center(surf, image, center, angle):
    rotated_image = pygame.transform.rotate(image, -angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=center).center)
    surf.blit(rotated_image, new_rect)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = datetime.datetime.now()
    sec_angle = now.second * 6
    min_angle = now.minute * 6

    screen.fill((0, 0, 0))
    screen.blit(bg, (WIDTH//2 - bg.get_width()//2, HEIGHT//2 - bg.get_height()//2))

    blit_rotate_center(screen, right_hand, (WIDTH//2 - right_hand.get_width()//2, HEIGHT//2 - right_hand.get_height()//2), sec_angle)
    blit_rotate_center(screen, left_hand, (WIDTH//2 - left_hand.get_width()//2, HEIGHT//2 - left_hand.get_height()//2), min_angle)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()