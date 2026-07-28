import numpy as np
import pygame
from os import path
from pygame.locals import *
flags = FULLSCREEN | DOUBLEBUF

pygame.init()
# Fixed 1920x1080 logical resolution; SCALED scales it to any monitor and remaps mouse input.
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.SCALED)
screen_width, screen_height = pygame.display.get_surface().get_size()
bg_surface = pygame.Surface((screen_width, screen_height))

run = True
start = False
WHITE = (255, 255, 255)
RED = (200, 25, 25)
BLACK = (0, 0, 0)

tile_size = 15
x_size = int(screen_width/tile_size)
y_size = int(screen_height/tile_size)
A = np.zeros((x_size,y_size))

direc = [[1,0],[1,1],[0,1],[-1,0],[-1,-1],[0,-1],[1,-1],[-1,1]]


def draw_grid():
    pygame.draw.rect(bg_surface, WHITE, (0, 0, screen_width, screen_height))
    for i in range(x_size):
        pygame.draw.line(bg_surface, RED, (tile_size*i,0), (tile_size*i, screen_height))
    for j in range(y_size):
        pygame.draw.line(bg_surface, RED, (0,tile_size*j), (screen_width, tile_size*j))

def draw_objects(A):
    for i in range(x_size):
         for j in range(y_size):
            #Draw rectangles on the grid
            if A[i][j] == 1:
                pygame.draw.rect(bg_surface, BLACK, (tile_size*i, tile_size*j, tile_size, tile_size))

def check_neighbor(i,j):
    num_live = 0
    for coord in direc:
        x_new = i + coord[0]
        y_new = j + coord[1]
        if (0 <= x_new < x_size) and (0 <= y_new < y_size):
            if (A[i + coord[0]][j + coord[1]]) == 1:
                num_live += 1
                if num_live > 3:
                    break
    return num_live

def check_grid(A):
    B = np.zeros((x_size,y_size))
    for i in range(x_size):
        for j in range(y_size):
            num_live = check_neighbor(i,j)
            if A[i][j] == 1:
                if num_live < 2:    # Underpopulation
                    B[i,j] = 0
                elif (num_live == 2) or (num_live == 3):    # Lives on
                    B[i,j] = 1
                else:   # Overpopulation
                    B[i,j] = 0
            else:   # Reproduction
                if num_live == 3:
                    B[i,j] = 1
    return B
            
#Start loop
while run:
    pygame.display.update()
    screen.blit(bg_surface, (0,0))

    pos = pygame.mouse.get_pos()
    x = (pos[0])//tile_size
    y = (pos[1])//tile_size

    if start == True:
        A = check_grid(A)

    try:
        if pygame.mouse.get_pressed()[0] == 1 and A[x][y] != 1:
            A[x][y] = 1
        elif pygame.mouse.get_pressed()[2] == 1 and A[x][y] != 0:
            A[x][y] = 0
    except:
        pass

    draw_grid()
    draw_objects(A)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            elif event.key == pygame.K_SPACE:
                start = not start

pygame.quit()