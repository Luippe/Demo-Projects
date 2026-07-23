'''
Note:
During the simulation, you can drag the moving bar inside the rectangle to change the time
'''


import pygame
from os import path
from pygame.locals import *
import numpy as np
from scipy.integrate import odeint
import math

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
run = True
timer = 0
timer_index = 0
time_interval = 5
path_list = []

font = pygame.font.SysFont('Futura', 50)
#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#Calculations:
mass = 30
gravity_accel = 9.8
v_init = 20
theta_init = np.pi/4
vx_init = v_init * np.cos(theta_init)
vy_init = v_init * np.sin(theta_init)
time = np.linspace(0, time_interval, 100)
init_condition = [vx_init, vy_init, 0, 0]
dt = round((100/time_interval)/60, 2)

def velocity_and_displacement(y, time, mass, gravity_accel):
    vx, vy, y_pos, x_pos = y
    dydt = [(-5 * vx) / mass, -gravity_accel - (5 * vy) / mass, vy, vx]
    return dydt

sol = odeint(velocity_and_displacement, init_condition, time, args = (mass, gravity_accel))
x_position_list = sol[:,3]
y_position_list = sol[:,2]
x_position = x_position_list[timer_index]
y_position = y_position_list[timer_index]
velocity = np.sqrt(sol[:,0] ** 2 + sol[:,1] ** 2)

#simulation loop
while run:
    screen.fill(BLACK)
    if timer >= 10:
        timer = 0
        x_position = 15*x_position_list[timer_index]
        y_position = 15*y_position_list[timer_index]
        path_list.append([500 + x_position, 500 - y_position])
        timer_index += 1
        if timer_index > 99:
            timer_index = 0
            timer = -10
            path_list.clear()
    for num in path_list:
        pygame.draw.circle(screen, RED, (num), 3)
    pygame.draw.circle(screen, RED, (500 + x_position,500 - y_position),15)
    pygame.draw.line(screen, WHITE, (500,500), (1000,500), 3)
    pygame.draw.line(screen, WHITE, (500,500), (500,200), 3)
    pos = pygame.mouse.get_pos()
    x_mouse = pos[0]
    y_mouse = pos[1]
    pygame.draw.line(screen, WHITE, (650 + 5*timer_index, 700), (650 + 5*timer_index, 750), 3)
    if (650 < x_mouse < 1150) and (700 < y_mouse < 750):
        if pygame.mouse.get_pressed()[0] == 1:
            pygame.draw.line(screen, WHITE, (x_mouse, 700), (x_mouse, 750), 3)
            timer_index = math.floor((x_mouse - 650)/5)
            x_previous = x_mouse
            x_position = 15*x_position_list[timer_index]
            y_position = 15*y_position_list[timer_index]
    else:
        timer += dt
    pygame.draw.rect(screen, WHITE, (650, 700, 500, 50), 5)
    draw_text(f'Time: {"{:.3f}".format(time[timer_index])}', font, WHITE, 1300, 300)
    draw_text(f'X Displacement: {"{:.3f}".format(sol[timer_index][3])}', font, WHITE, 1300, 400)
    draw_text(f'Y Displacement: {"{:.3f}".format(sol[timer_index][2])}', font, WHITE, 1300, 500)
    draw_text(f'Velocity: {"{:.3f}".format(velocity[timer_index])}', font, WHITE, 1300, 600)
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            run = False
    pygame.display.update()
pygame.quit()