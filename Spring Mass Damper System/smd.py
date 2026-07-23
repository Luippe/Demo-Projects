import pygame
from pygame.locals import *
import numpy as np
flags = FULLSCREEN | DOUBLEBUF

pygame.init()
clock = pygame.time.Clock()
fps = 60
run = True
t = 0
delay = 0
cart_time = 0
cart_pos = 0

WHITE = (255,255,255)
BLACK = (0,0,0)
stop = True
# Fixed 1920x1080 logical resolution; SCALED scales it to any monitor and remaps mouse input.
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.SCALED)
screen_width, screen_height = pygame.display.get_surface().get_size()
spring = pygame.image.load('spring.png').convert_alpha()
base_spring = pygame.image.load('spring.png').convert_alpha()
damp1 = pygame.image.load('damp1.png').convert_alpha()
damp2 = pygame.image.load('damp2.png').convert_alpha()
damp1 = pygame.transform.scale(damp1, (700,100))
damp2 = pygame.transform.scale(damp2, (700,100))


while run:
    screen.fill(BLACK)
    if stop == False:
        delay += 1
        if delay >= 150:
            if cart_pos < 200:
                cart_pos += 2
            elif cart_pos >= 200:
                cart_time += 1
            if cart_time >= 200:
                t += 0.01

    x_pos = 200*(1 - np.exp(-t)*np.cos(3*t) + (1/3)*np.exp(-t)*np.sin(3*t))
    spring = pygame.transform.scale(base_spring, (600 + round(x_pos - cart_pos), 100))
    if t > 13:
        cart_pos = 0
        x_pos = 0
        cart_time = 0
        delay = 0
        t = 0
    screen.blit(spring, (250 + cart_pos,400))
    screen.blit(damp1, (250 + cart_pos, 550))
    screen.blit(damp2, (200 + x_pos, 550))
    pygame.draw.rect(screen, WHITE, (850 + x_pos,250,700,500))
    pygame.draw.circle(screen, WHITE, (1000 + x_pos, 750), 100)
    pygame.draw.circle(screen, WHITE, (1400 + x_pos, 750), 100)
    pygame.draw.rect(screen, WHITE, (200 + cart_pos,200,50,700))
    pygame.draw.rect(screen, WHITE, (200 + cart_pos,850,1400,80))
    pygame.draw.circle(screen, WHITE, (500 + cart_pos, 930), 70)
    pygame.draw.circle(screen, WHITE, (1300 + cart_pos, 930), 70)
    pygame.draw.rect(screen, WHITE, (0, 1000, 2050, 200))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            run = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if stop == False:
                stop = True
            elif stop == True:
                stop = False
    pygame.display.update()
pygame.quit()