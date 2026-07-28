# from numpy.lib.shape_base import apply_along_axis
import pygame
import numpy as np
from scipy.integrate import odeint
import Properties as prop
pygame.init()
# Fixed 1920x1080 logical resolution; SCALED scales it to any monitor and remaps mouse input.
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.SCALED)
screen_width, screen_height = pygame.display.get_surface().get_size()
run = True
BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

mean_velocity = 2
length = 2
radius = 0.05
diameter = 2 * radius
area = np.pi * radius**2
Q = mean_velocity * area
mu = prop.search('Air', 'mu', 300) * 10**-6
density = prop.search('Air', 'p', 300)
pressure_change = (8 * mu * length * Q)/(np.pi * radius**4)
radius_check = np.linspace(0,radius, 50)
ReD = (density * mean_velocity * diameter)/(mu)


if ReD < 2100:
    vel_z = -(pressure_change * (radius_check**2 - radius**2))/(4 * mu)
else:
    print(ReD)

font = pygame.font.SysFont('Futura', 50)
#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

while run:
    screen.fill(BLACK)
    draw_text(f'Max Velocity: {2 * mean_velocity} m/s', font, WHITE, 100, 100)
    draw_text(f'Reynolds Number: {"{:.0f}".format(ReD)}', font, WHITE, 100, 200)
    for r, num in enumerate(vel_z):
        red = sorted([0, 10*num, 255])[1]
        color = (red, 0, 0)
        pygame.draw.line(screen, color, (500, 650 + 3*r), (1200, 650 + 3*r), 3)
        pygame.draw.line(screen, color, (500, 650 - 3*r), (1200, 650 - 3*r), 3)
    pygame.draw.line(screen, WHITE, (500, 500), (1200, 500), 5)
    pygame.draw.line(screen, WHITE, (500, 800), (1200, 800), 5)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
    pygame.display.update()
pygame.quit()