'''
Note:
During the simulation, you can drag the moving bar inside the rectangle to change the time
'''


import pygame
from os import path
from pygame.locals import *
import numpy as np
from scipy.integrate import odeint
import time
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
BLUE = (30, 144, 255)

run = True
timer = 0
timer_index = 0
x_previous = 650
y_previous = 800
time_interval = 15
settling_time = 0
settling_time_index = 0
path_list = []
#Calculations:
c = 0.6
g = 9.81
m = 1
l = 1
y0 = [np.pi / 6, 0]
time_pendulum = np.linspace(0,time_interval,300)
dt = round((300/time_interval)/60, 2)

def pend(y, t, c, g, m, l):
    theta, ang_velocity = y
    dydt = [ang_velocity, (-c * ang_velocity / m) - (g * np.sin(theta) / l)]
    return dydt

sol = odeint(pend, y0, time_pendulum, args = (c, g, m, l))
angle_list = sol[:,0]
x_position = 300*np.sin(angle_list[timer_index])
y_position = 300*np.cos(angle_list[timer_index])
start = time.time()

for row in range(1, np.shape(sol)[0]):
    if abs(sol[-1*row][0]) > 0.02 * np.pi/6:
        settling_time = time_pendulum[-1*row]
        settling_time_index = 300 - row
        break

font = pygame.font.SysFont('Futura', 50)
#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#simulation loop
while run:
    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, (650,900), (1150,900), 3)
    pygame.draw.line(screen, WHITE, (650,800), (650,1000), 3)
    if timer >= 10:
        timer = 0
        x_position = 300*np.sin(angle_list[timer_index])
        y_position = 300*np.cos(angle_list[timer_index])
        path_list.append([650 + (5/3)*timer_index, 900 - 150*angle_list[timer_index]])
        timer_index += 1
        if timer_index > 299:
            timer_index = 0
            timer = -10
            print(time.time() - start)
    for num in path_list:
        pygame.draw.circle(screen, RED, (num), 2)
    
    pos = pygame.mouse.get_pos()
    x_mouse = pos[0]
    y_mouse = pos[1]
    pygame.draw.line(screen, WHITE, (650 + (5/3)*timer_index, 700), (650 + (5/3)*timer_index, 750), 3)
    if (650 < x_mouse < 1150) and (700 < y_mouse < 750):
        if pygame.mouse.get_pressed()[0] == 1:
            pygame.draw.line(screen, WHITE, (x_mouse, 700), (x_mouse, 750), 3)
            timer_index = math.floor((x_mouse - 650)/(5/3))
            x_previous = x_mouse
            x_position = 300*np.sin(angle_list[timer_index])
            y_position = 300*np.cos(angle_list[timer_index])
            pygame.draw.line(screen, WHITE, (900,300), (900 + x_position, 300 + y_position), 3)
            pygame.draw.line(screen, WHITE, (900,300), (900, 600), 2)
            pygame.draw.circle(screen, RED, (900 + x_position,300 + y_position),15)
    else:
        timer += dt
    pygame.draw.line(screen, WHITE, (900,300), (900 + x_position, 300 + y_position), 3)
    pygame.draw.line(screen, WHITE, (900,300), (900, 600), 2)
    pygame.draw.line(screen, BLUE, (650 + (5/3)*settling_time_index, 700), (650 + (5/3)*settling_time_index, 750), 3)
    pygame.draw.rect(screen, WHITE, (650, 700, 500, 50), 5)
    pygame.draw.circle(screen, RED, (900 + x_position,300 + y_position),15)

    draw_text(f'Time: {"{:.3f}".format(time_pendulum[timer_index])}', font, WHITE, 1300, 300)
    draw_text(f'Angle: {"{:.3f}".format(sol[timer_index][0])}', font, WHITE, 1300, 400)
    draw_text(f'Angular Velocity: {"{:.3f}".format(sol[timer_index][1])}', font, WHITE, 1300, 500)
    draw_text(f'Settling Time: {"{:.3f}".format(settling_time)}', font, WHITE, 1300, 600)
    draw_text('Angle Vs Time', font, WHITE, 380, 870)
    draw_text('Ts', font, BLUE, 630 + (5/3)*settling_time_index, 650)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            run = False
    pygame.display.update()
pygame.quit()