import pygame
from os import path
from pygame.locals import *
import numpy as np
from scipy.integrate import odeint
import time
import math

flags = FULLSCREEN | DOUBLEBUF

pygame.init()
clock = pygame.time.Clock()
fps = 120
run = True
mass = 3
length = 4
WHITE = (255,255,255)
BLACK = (0,0,0)
dt = 0.002
gravity_accel = 9.81
theta1_prev = np.pi/2
theta2_prev = np.pi/2
theta1 = 0
theta2 = 0
vel1_prev = 0
vel2_prev = 0
momentum1_prev = 0
momentum2_prev = 0
method = 1

# Fixed 1920x1080 logical resolution; SCALED scales it to any monitor and remaps mouse input.
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.SCALED)
screen_width, screen_height = pygame.display.get_surface().get_size()

def theta1_dot(t1_prev, t2_prev, p1_prev, p2_prev):
    vel1 = (6 * (2 * p1_prev - 3 * np.cos(t1_prev - t2_prev) * p2_prev)) / (mass * length**2 * (16 - 9 * np.cos(t1_prev - t2_prev)**2))
    return vel1


def theta2_dot(t1_prev, t2_prev, p1_prev, p2_prev):
    vel2 = (6 * (8 * p2_prev - 3 * np.cos(t1_prev - t2_prev) * p1_prev)) / (mass * length**2 * (16 - 9 * np.cos(t1_prev - t2_prev)**2))
    return vel2


def momentum1(v1_prev, v2_prev, t1_prev, t2_prev):
    p1 = -0.5 * mass * length**2 * (v1_prev * v2_prev * np.sin(t1_prev - t2_prev) + (3 * gravity_accel * np.sin(t1_prev) / length))
    return p1


def momentum2(v1_prev, v2_prev, t1_prev, t2_prev):
    p2 = -0.5 * mass * length**2 * (-v1_prev * v2_prev * np.sin(t1_prev - t2_prev) + (gravity_accel * np.sin(t2_prev) / length))
    return p2


while run:
    screen.fill(BLACK)
    if method == 0:
        p1 = momentum1_prev + dt * momentum1(vel1_prev, vel2_prev, theta1_prev, theta2_prev)
        p2 = momentum2_prev + dt * momentum2(vel1_prev, vel2_prev, theta1_prev, theta2_prev)
        theta1 = theta1_prev + dt * theta1_dot(theta1_prev, theta2_prev, momentum1_prev, momentum2_prev)
        theta2 = theta2_prev + dt * theta2_dot(theta1_prev, theta2_prev, momentum1_prev, momentum2_prev)
        vel1_prev = theta1_dot(theta1_prev, theta2_prev, momentum1_prev, momentum2_prev)
        vel2_prev = theta2_dot(theta1_prev, theta2_prev, momentum1_prev, momentum2_prev)
        momentum1_prev = p1
        momentum2_prev = p2
        theta1_prev = theta1
        theta2_prev = theta2
    pygame.draw.line(screen, WHITE, (1000, 300), (1000 + 100 * length * np.sin(theta1), 300 + 100 * length * np.cos(theta1)), 10)
    pygame.draw.line(screen, WHITE, (1000 + 100 * length * np.sin(theta1), 300 + 100 * length * np.cos(theta1)), (1000 + 100 * length * np.sin(theta1) + 100 * length * np.sin(theta2), 300 + 100 * length * np.cos(theta1) + 100 * length * np.cos(theta2)), 10)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            run = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            method = 0
    pygame.display.update()
pygame.quit()