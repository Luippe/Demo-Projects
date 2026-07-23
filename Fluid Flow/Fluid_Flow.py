import numpy as np
import pygame
from pygame.locals import *
#define variables and initialize graph
pygame.init()
clock = pygame.time.Clock()
fps = 60
field = pygame.display.set_mode((300,300))
screen_width, screen_height = pygame.display.get_surface().get_size()
run = True

tile_size = 10
num = 0
change = 0.5
h = 1/10
previous_x = 0
previous_y = 0


pygame.display.set_caption('Fluid Flow')
grid_array = np.zeros((int(screen_height / tile_size) + 2, int(screen_width / tile_size) + 2))
velocity_x = np.zeros((int(screen_height / tile_size) + 2, int(screen_width / tile_size) + 2))
velocity_y = np.zeros((int(screen_height / tile_size) + 2, int(screen_width / tile_size) + 2))
velocity_x_prev = np.zeros((int(screen_height / tile_size) + 2, int(screen_width / tile_size) + 2))
velocity_y_prev = np.zeros((int(screen_height / tile_size) + 2, int(screen_width / tile_size) + 2))
density_array = np.zeros((int(screen_height / tile_size) + 2, int(screen_width / tile_size) + 2))
density_array_prev = np.zeros((int(screen_height / tile_size) + 2, int(screen_width / tile_size) + 2))
divergence_array = np.zeros((int(screen_height / tile_size) + 2, int(screen_width / tile_size) + 2))
poisson_array = np.zeros((int(screen_height / tile_size) + 2, int(screen_width / tile_size) + 2))


def project(vel_x, vel_y):
    for i in range(np.shape(density_array)[0] - 1):
        for j in range(np.shape(density_array)[1] - 1):
            divergence_array[i][j] = -0.5 * h * (vel_x[i + 1][j] - vel_x[i - 1][j] + vel_y[i][j + 1] - vel_y[i][j - 1])
            poisson_array[i][j] = 0
    
    for k in range(0,5):
        for i in range(np.shape(density_array)[0] - 1):
            for j in range(np.shape(density_array)[1] - 1):
                poisson_array[i][j] = (divergence_array[i][j] + poisson_array[i - 1][j] + poisson_array[i + 1][j] + poisson_array[i][j - 1] + poisson_array[i][j + 1]) / 4

    for i in range(np.shape(density_array)[0] - 1):
            for j in range(np.shape(density_array)[1] - 1):
                vel_x[i][j] -= 0.5 * (poisson_array[i + 1][j] - poisson_array[i - 1][j]) / h
                vel_y[i][j] -= 0.5 * (poisson_array[i][j + 1] - poisson_array[i][j - 1]) / h
    return vel_x, vel_y


def diffuse(array):
    for k in range(0,5):
        for i in range(np.shape(density_array)[0] - 1):
            for j in range(np.shape(density_array)[1] - 1):
                array[i][j] = (array[i][j] +  change * (array[i + 1][j] + array[i - 1][j] + array[i][j + 1] + array[i][j - 1]) / 4) / (1 + change)
    return array


def advect(d_array, v_x, v_y):
    for i in range(np.shape(d_array)[0] - 1):
        for j in range(np.shape(d_array)[1] - 1):
            y_real = j - v_x[i][j]
            x_real = i - v_y[i][j]
            if y_real < 0:
                y_real = 0
            if y_real > 30:
                y_real = 30
            if x_real < 0:
                x_real = 0
            if x_real > 30:
                x_real = 30
            i_init = int(x_real)
            i_fin = i_init + 1
            j_init = int(y_real)
            j_fin = j_init + 1
            s_fin = x_real - i_init
            s_init = 1 - s_fin
            t_fin = y_real - j_init
            t_init = 1 - t_fin
            d_array[i][j] = s_init * (t_init * d_array[i_init, j_init] + t_fin * d_array[i_init, j_fin]) + s_fin * (t_init * d_array[i_fin, j_init] + t_fin * d_array[i_fin, j_fin])
            d_array[i][j] = sorted((0,d_array[i][j], 255))[1]
    return d_array


def draw(den_array):
    for i in range(np.shape(den_array)[0] - 1):
        for j in range(np.shape(den_array)[1] - 1):
            pygame.draw.rect(field, (den_array[i][j], den_array[i][j], den_array[i][j]), (j * tile_size, i * tile_size, tile_size, tile_size))


while run:
    clock.tick(fps)
    pos = pygame.mouse.get_pos()
    if 0 < pos[0] < screen_width and 0 < pos[1] < screen_height:
        x = (pos[0])//tile_size
        y = (pos[1])//tile_size
        velocity_x[y][x] += 10*(x - previous_x)
        velocity_y[y][x] += 10*(y - previous_y)
        density_array_prev[y][x] -= 300
        previous_x = x
        previous_y = y

    #velocity step
    velocity_x_prev = velocity_x
    velocity_y_prev = velocity_y
    velocity_x = diffuse(velocity_x_prev)
    velocity_y = diffuse(velocity_y_prev)
    velocity_x_prev = velocity_x
    velocity_y_prev = velocity_y
    velocity_x, velocity_y = project(velocity_x, velocity_y)
    velocity_x = advect(velocity_x, velocity_x, velocity_y)
    velocity_y = advect(velocity_y, velocity_x, velocity_y)
    velocity_x, velocity_y = project(velocity_x, velocity_y)
    

    #density step
    density_array_prev[15][15] = 300
    density_array = diffuse(density_array_prev)
    density_array = advect(density_array, velocity_x, velocity_y)

    
    #draw field
    draw(density_array)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            run = False
        elif event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()