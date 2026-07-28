import pygame
from os import path
from pygame.locals import *
import numpy as np

pygame.init()
clock = pygame.time.Clock()
fps = 60
# Fixed 1920x1080 logical resolution; SCALED scales it to any monitor and remaps mouse input.
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.SCALED)
screen_width, screen_height = pygame.display.get_surface().get_size()
pygame.display.set_caption('Platformer')

RED = (200, 25, 25)
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (30, 144, 255)
drag_coeff = 0.5
density = 1.225
time = 0
radius = 0.05
mass = 3
area = np.pi*radius**2
run = True

def imp_euler_k(area, mass, component):
    pass

class direction():
    def __init__(self):
        self.holding = False
        self.dx = 0
        self.dy = 0
        self.x_prev = 0
        self.y_prev = 0

    def update(self):
        pos = pygame.mouse.get_pos()
        #get mouse position
        x = pos[0]
        y = pos[1]
        if pygame.mouse.get_pressed()[0] == 1 and self.holding == False:
            self.x_prev = x
            self.y_prev = y
            self.holding = True
        if pygame.mouse.get_pressed()[0] == 0 and self.holding == True:
            self.dx = np.floor(x - self.x_prev)
            self.dy = np.floor(y - self.y_prev)
            self.dx = sorted([-50, self.dx, 50])[1]
            self.dy = sorted([-50, self.dy, 50])[1]
            no_drag_class.x_start = self.x_prev
            no_drag_class.y_start = self.y_prev
            no_drag_class.dx = self.dx
            no_drag_class.dy = self.dy
            euler_class.x_prev = self.x_prev
            euler_class.y_prev = self.y_prev
            euler_class.dx_prev = self.dx
            euler_class.dy_prev = self.dy
            self.holding = False
        if self.holding == True:
            pygame.draw.circle(screen, WHITE, (self.x_prev, self.y_prev), 10)
        if self.holding == True:
            pygame.draw.line(screen, WHITE, (self.x_prev, self.y_prev), (x,y))


#calculate projectile with no drag
class no_drag():
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.pos_x = 0
        self.pos_y = 0
        self.x_start = 0
        self.y_start = 0

    def update(self, time):
        self.pos_y = 0.5*9.81*time**2 + self.dy*time + self.y_start
        self.pos_x = self.dx*time + self.x_start
        pygame.draw.circle(screen, WHITE, (self.pos_x, self.pos_y), 10)


#calculate projectile with euler's method
class euler():
    def __init__(self, area, mass):
        self.mass = mass
        self.area = area
        self.dx = 0
        self.dy = 0
        self.dx_prev = 0
        self.dy_prev = 0
        self.pos_x = 0
        self.pos_y = 0
        self.x_prev = 0
        self.y_prev = 0
        self.dt = 0.01

    def update(self):
        self.dx = self.dx_prev + self.dt*(-0.5*1.18*0.5*self.area*self.dx_prev*np.sqrt(self.dx_prev**2 + self.dy_prev**2)/self.mass)
        self.dy = self.dy_prev + self.dt*(9.81 - (0.5*1.18*0.5*self.area*self.dy_prev*np.sqrt(self.dx_prev**2 + self.dy_prev**2)/self.mass))
        self.pos_x = self.x_prev + self.dt*self.dx
        self.pos_y = self.y_prev + self.dt*self.dy
        self.dx_prev = self.dx
        self.dy_prev = self.dy
        self.x_prev = self.pos_x
        self.y_prev = self.pos_y
        pygame.draw.circle(screen, RED, (self.pos_x, self.pos_y), 10)


#calculate projectile with improved euler's method
class imp_euler():
    def __init__(self, area, mass):
        self.mass = mass
        self.area = area
        self.dx = 0
        self.dy = 0
        self.dx_prev = 0
        self.dy_prev = 0
        self.pos_x = 0
        self.pos_y = 0
        self.x_prev = 0
        self.y_prev = 0
        self.k_1 = 0
        self.k_2 = 0
        self.dh = 0.01
    
    def update(self):
        pass

direction_class = direction()
no_drag_class = no_drag()
euler_class = euler(area, mass)
improved_euler_class = imp_euler(area, mass)
while run:
    screen.fill(BLACK)
    time += 0.01
    direction_class.update()
    if direction_class.holding == False:
        no_drag_class.update(time)
        euler_class.update()
    else:
        time = 0
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
    pygame.display.update()
pygame.quit()