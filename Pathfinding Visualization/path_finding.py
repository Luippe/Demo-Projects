import numpy as np
import pygame
from os import path
from pygame.locals import *
from math import ceil, floor
from xml.dom.pulldom import parseString
import os, sys

def resource_path(rel):
    """Locate an asset whether run from source or a bundled PyInstaller .exe."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel)

flags = FULLSCREEN | DOUBLEBUF

pygame.init()
screen = pygame.display.set_mode((1920, 1080), FULLSCREEN | SCALED)
screen_width, screen_height = pygame.display.get_surface().get_size()
bg_surface = pygame.Surface((screen_width, screen_height))
text_surface = pygame.Surface((screen_width, screen_height),SRCALPHA)

run = True
x_size = 30
y_size = 18
A = np.zeros((x_size,y_size))
A[:,0] = 1
A[:,-1] = 1
A[0,:] = 1
A[-1,:] = 1
priority_queue = []
path_pos = []
checked_pos = []
sol_path = []
direc_path = []
next_path = []
goal_pos = [1,1]
start_pos = [1,1]
new_path = [0,0]
WHITE = (255, 255, 255)
RED = (200, 25, 25)
BLACK = (0, 0, 0)
GREEN = (144, 201, 120)
LIGHT_BLUE = (8, 65, 194)
ORANGE = (255, 69, 0)
YELLOW = (220, 220, 0)
ORANGE = (255, 69, 0)

tile_size = 50
edge_x = 250
edge_y = 200
start = False
got_sol = False
counter = 0
steps = 0
sorted_index = 0

font = pygame.font.Font(resource_path('editundo.ttf'), 30)
def draw_text(text, font, text_col, x, y,screen_surf):
    img = font.render(text, True, text_col)
    screen_surf.blit(img, (x, y))

def draw_grid():
    pygame.draw.rect(bg_surface, WHITE, (edge_x, edge_y, tile_size*x_size, tile_size*y_size))
    for i in range(x_size):
        pygame.draw.line(bg_surface, RED, (tile_size*i+edge_x,edge_y), (tile_size*i+edge_x, tile_size*y_size+edge_y-tile_size))
    for j in range(y_size):
        pygame.draw.line(bg_surface, RED, (edge_x,tile_size*j+edge_y), (tile_size*x_size+edge_x-tile_size, tile_size*j+edge_y))

def draw_path(new_loc,color):
    x_loc = new_loc[0]
    y_loc = new_loc[1]
    pygame.draw.rect(bg_surface, color, (tile_size*x_loc+edge_x, tile_size*y_loc+edge_y, tile_size, tile_size))

def draw_objects(A):
    x_size = np.shape(A)[0]
    y_size = np.shape(A)[1]
    for i in range(x_size):
         for j in range(y_size):
            #Draw rectangles on the grid
            if A[i][j] == 1:
                pygame.draw.rect(bg_surface, BLACK, (tile_size*i+edge_x, tile_size*j+edge_y, tile_size, tile_size))
            elif A[i][j] == 2:
                 pygame.draw.rect(bg_surface, LIGHT_BLUE, (tile_size*i+edge_x, tile_size*j+edge_y, tile_size, tile_size))
                 
def in_grid(x, y):
    """True when a tile coordinate is actually on the board.

    Guards every A[x][y] lookup driven by the mouse. Clicking right of the grid
    gives x >= x_size (IndexError), and clicking left of or above it gives a
    negative x/y -- which numpy happily accepts as an index from the far end,
    silently editing a tile on the opposite edge.
    """
    return 0 <= x < x_size and 0 <= y < y_size

def draw_legend():
    pygame.draw.rect(screen, LIGHT_BLUE, (850, 50, tile_size,tile_size))
    draw_text("Shortest Path", font, WHITE, 900, 50,screen)
    pygame.draw.rect(screen, RED, (850, 100, tile_size,tile_size))
    draw_text("Checked Areas", font, WHITE, 900, 100,screen)
    pygame.draw.rect(screen, GREEN, (850, 150, tile_size,tile_size))
    draw_text("Border", font, WHITE, 900, 150,screen)


draw_grid()
draw_objects(A)
#Start loop
while run:
    pygame.display.update()
    screen.blit(bg_surface, (0,0))
    screen.blit(text_surface, (0,0))
    draw_legend()
    if start == True and counter <= 5000:
        path_pos.append(current_pos)
        draw_path(path_pos[-1],RED)
        x_curr = current_pos[0]
        y_curr = current_pos[1]
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                next_pos = [x_curr+i, y_curr+j]
                # Normally the all-wall border keeps the search inside A, but a
                # start tile placed ON the border scans past the edge.
                if in_grid(next_pos[0], next_pos[1]) == False:
                    continue
                if (next_pos in path_pos) == False and (A[x_curr+i][y_curr+j] != 1):
                    goal_dist = np.linalg.norm([a_i - b_i for a_i, b_i in zip(next_pos, goal_pos)])
                    start_dist = np.linalg.norm([a_i - b_i for a_i, b_i in zip(next_pos, current_pos)]) + curr_start_val
                    if (next_pos in checked_pos) == False:
                        checked_pos.append(next_pos)
                        draw_path(checked_pos[-1],GREEN)
                        priority_queue.append([goal_dist+start_dist,start_dist])
                        test_queue.append([goal_dist+start_dist,start_dist])
                        direc_path.append(current_pos)
                        next_path.append(next_pos)
                    else:
                        comparing_index = checked_pos.index(next_pos)
                        if priority_queue[comparing_index][0] > goal_dist + start_dist:
                            priority_queue[comparing_index] = [goal_dist+start_dist,start_dist]
                            test_queue[comparing_index] = [goal_dist+start_dist,start_dist]
                            path_index = next_path.index(next_pos)
                            direc_path[path_index] = current_pos
                            next_path[path_index] = next_pos
        
        checked_pos.remove(current_pos)
        # Pop the current node's frontier entry by INDEX. The original code removed
        # it by value (priority_queue.remove(...)), which deletes the FIRST entry
        # with a matching f-score -- and duplicate f-scores are very common on a grid.
        # That desynced priority_queue from checked_pos and drained the frontier,
        # leaving min() below with an empty list.
        priority_queue.pop(sorted_index)
        # Frontier empty => everything reachable was explored without hitting the
        # goal, i.e. no path exists. Stop gracefully instead of crashing on min().
        if len(priority_queue) == 0:
            start = False
            counter = 0
            draw_text("No path found!", font, RED, edge_x, edge_y - 60, text_surface)
            continue
        high_priority = min(priority_queue, key = lambda x: x[0])        
        sorted_index = priority_queue.index(high_priority)
        curr_start_val = priority_queue[sorted_index][1]
        current_pos = checked_pos[sorted_index]

        counter += 1
        if current_pos == goal_pos:
            start = False
            path_pos.append(current_pos)
            counter = 0
            next_loc = goal_pos
            sum_path = 0
            while got_sol == False:
                place = next_path.index(next_loc)
                next_loc = direc_path[place]
                sum_path += test_queue[place][0]
                sol_path.append(next_loc)
                draw_path(sol_path[-1], LIGHT_BLUE)
                if sol_path[-1] == start_pos:
                    got_sol = True
                    draw_path(goal_pos, LIGHT_BLUE)
            for loc in next_path:
                place = next_path.index(loc)
                # uncomment if you want to see the queue values
                # draw_text(f'{round(test_queue[place][0],1)}',font,ORANGE,edge_x + tile_size*loc[0],edge_y + tile_size*loc[1] + (tile_size//2),text_surface)

    pos = pygame.mouse.get_pos()
    x = (pos[0] - edge_x)//tile_size
    y = (pos[1] - edge_y)//tile_size
    # Checked before every A[x][y] below -- the cursor is free to leave the grid.
    on_grid = in_grid(x, y)
    if on_grid and pygame.mouse.get_pressed()[0] == 1 and A[x][y] != 1:
         A[x][y] = 1
         draw_objects(A)
    elif on_grid and pygame.mouse.get_pressed()[2] == 1 and A[x][y] != 0:
         A[x][y] = 0
         pygame.draw.rect(bg_surface, WHITE, (tile_size*x+edge_x, tile_size*y+edge_y, tile_size, tile_size))
         draw_grid()
         draw_objects(A)
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            elif event.key == pygame.K_g and on_grid and A[x][y] != 2:
                 A[goal_pos[0]][goal_pos[1]] = 0
                 A[x][y] = 2
                 goal_pos = [x,y]
                 draw_objects(A)
            elif event.key == pygame.K_s and on_grid and A[x][y] != 3:
                 A[start_pos[0]][start_pos[1]] = 0
                 start_pos = [x,y]
                 current_pos = [x,y]
                 priority_queue = []
                 checked_pos = []
                 path_pos = [1,1]
                 sol_path = [goal_pos]
                 next_path = []
                 direc_path = []
                 all_path = []
                 test_queue = [[1000,0]]
                 priority_queue.append([1000,0])
                 checked_pos.append(current_pos)
                 next_path.append(current_pos)
                 direc_path.append(current_pos)
                 curr_start_val = 0
                 sorted_index = 0
                 counter = 0
                 start = True
                 got_sol = False
                 bg_surface.fill(BLACK)
                 text_surface.fill((0,0,0,0))
                 draw_grid()
                 draw_objects(A)

pygame.quit()