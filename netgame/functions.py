import os
import sys
import pygame
import numpy as np
from itertools import chain, zip_longest
from items import all_description_dict, all_equippable_stats

BLACK = (0,0,0)
WHITE = (255,255,255)
DARKNESS = (30,30,30)
RED = (200, 25, 25)
GREEN = (144, 201, 120)
DARK_GREY = (105, 105, 105)
YELLOW = (242,242,73)
LIGHT_BLUE = (147, 207, 240)

# Define variables used throughout the functions
tile_size = 64
center = (320, 256)
w,h=(704,576)
map_x,map_y = (112,64)

def matprint(mat, fmt="g"):
    col_maxes = [max([len(("{:"+fmt+"}").format(x)) for x in col]) for col in mat.T]
    for x in mat:
        for i, y in enumerate(x):
            print(("{:"+str(col_maxes[i])+fmt+"}").format(y), end="")
        print("")

def open_file_in_same_directory(file_name):
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        script_dir = sys._MEIPASS
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, file_name)

# Function for outputting text onto the screen
def draw_text(text, text_col, x, y, screen, size):
    font = pygame.font.Font(open_file_in_same_directory('editundo.ttf'), size)
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#center and scale the word so that it fits nicely in the settings
def scale_and_center_word(word,fit_inx,fit_iny):
    len_letter = 40
    len_word = len(word)
    if len_word*len_letter > fit_inx:
        len_letter = fit_inx//len_word
    x = (fit_inx - len_letter*len_word)//4
    y = (fit_iny - len_letter)//2
    return x,y,len_letter

# Center text in the x direction, given a text surface and an x coordinate (scroll) to center to. Returns the x coordinate to blit the text
def center_text_x(text_surf, x_coord):
    text_width = text_surf.get_width()
    return x_coord - text_width//2

# Find which room the player is in. Returns the row and column as (m,n)
def obj_in_room(room_rect_list,x,y):
    y_shape,x_shape,_ = np.shape(room_rect_list)
    try:
        for m in range(y_shape):
            for n in range(x_shape):
                if room_rect_list[m][n].collidepoint(x,y):
                    return m,n
        return None,None
    except:
        return None,None

# Find the coordinates of the corners of the screen. padx,pady are extra column and row
def player_tiles_on_screen(scrollx,scrolly,padx=0,pady=0):
    tiles_x = -scrollx//tile_size
    tiles_y = -scrolly//tile_size
    screen_x,screen_y = (11,9)
    y_min = sorted([0,tiles_y - pady])[1]
    y_max = sorted([map_y,tiles_y + screen_y + pady])[0]
    x_min = sorted([0,tiles_x - padx])[1]
    x_max = sorted([map_x,tiles_x + screen_x + padx])[0]
    return y_min,y_max,x_min,x_max

# Iterate through the animations for a tile. Default frame between each iteration is 4.
# Only use this for if there can only exist 1 of this tile per map
def tile_animation(tile_num,min_tile,max_tile,timer,max_timer=4):
    if (tile_num >= min_tile) and (tile_num < max_tile):
        timer += 1
        if (timer > max_timer):
            tile_num += 1
            timer = 0
            if tile_num >= max_tile:
                return min_tile, timer
    return tile_num, timer

# Redefine variables when resetting map and also move player to the spawn point
# Variables are linked together so if variable in network changes, it will also change in canvas class
def map_reset(network,player_dict,canvas,mini_map_class,inventory_class,exit_class,enemy_class,health_class,action_class):
    global m,n
    map_mat,spawn_list,room_list,item_loc,id_list = network.data_list
    player = player_dict[network.index]
    m,n,_ = np.shape(room_list)
    canvas.map_mat = map_mat
    canvas.item_loc = item_loc
    canvas.room_rect_list = [[pygame.Rect(room_list[j,i]) for i in range(n)] for j in range(m)] #2d list of room rect objects
    network.mini_map = mini_map_class
    network.canvas = canvas
    network.enemy_class = enemy_class
    network.health_class = health_class
    network.action_class = action_class
    player.map_mat = map_mat
    exit_class.map_mat = map_mat
    inventory_class.exit_loc = tuple(zip(*np.where(map_mat == 18)))
    mini_map_class.reset_mini_map(map_mat,room_list,item_loc)
    spawn_randx = np.random.randint(spawn_list[2])
    spawn_randy = np.random.randint(spawn_list[3])
    player.scrollx = -tile_size*(spawn_randx + spawn_list[0]) + center[0]
    player.scrolly = -tile_size*(spawn_randy + spawn_list[1]) + center[1]
    return map_mat

# Create light around players and rooms. Return the surface that needs lighting, as well as the room that the players are in.
def lighting(surf,room_rect_list,scrollx,scrolly,player_dict,radius=128):
    lit_rooms = []
    for players in player_dict:
        m_room,n_room = obj_in_room(room_rect_list,players.rect.x,players.rect.y)
        if ((m_room,n_room) != (None,None)) and ((m_room,n_room) not in lit_rooms):
            lit_rooms.append((m_room,n_room))
            room_scaled = [room_rect_list[m_room][n_room][num]*tile_size for num in range(4)]
            # Move the rect so that it covers the room and 1 extra tile outwards
            room_scaled[0] -= tile_size - scrollx
            room_scaled[1] -= tile_size - scrolly
            room_scaled[2] += 2*tile_size
            room_scaled[3] += 2*tile_size
            pygame.draw.rect(surf,BLACK,room_scaled,0,80)
        elif (m_room,n_room) == (None,None):
            pygame.draw.circle(surf,BLACK,(-players.scrollx + scrollx + center[0] + (tile_size/2), -players.scrolly + scrolly + center[1] + (tile_size/2)),radius)
    return surf,lit_rooms

# Given coordinates (scroll) and the min and max amount of shake, return a list of coordinates that represents a shake
def random_shake(min_x,max_x,min_y,max_y):
    t = np.linspace(0,5,5)
    rand_x = np.random.uniform(min_x,max_x)
    rand_y = np.random.uniform(min_y,max_y)
    coorx = rand_x*np.cos(t)*np.exp(-0.5**t)
    coory = rand_y*np.cos(t)*np.exp(-0.5**t)
    return list(zip(coorx,coory))

# Find the index in a 2d list. Returns (row, col)
def index_2d(myList, look_for):
    for i, x in enumerate(myList):
        if look_for in x:
            return (i, x.index(look_for))
    return (None,None)

# Interweave two lists together without having to create a temporarily list. Used for getting the attack area
def weave_two_lists(l1, l2):
    return [x for x in chain(*zip_longest(l1, l2)) if x is not None]

# Add two lists together without having to create a temporarily list. Used for getting teh attack area
def add_two_lists(l1,l2):
    return [x+y for x,y in zip_longest(l1,l2, fillvalue=0)]

# Wrap text to make sure it fits properly onto the screen
def fit_description_text(val,description_text_size,stat_text_size,description_screen,window_width,equip_keys):
    word_list = all_description_dict[val[0]][val[1]].split(" ")
    text_len = 5   # Start at 5 pixels since there is a border
    row = 0
    font = pygame.font.Font(open_file_in_same_directory('editundo.ttf'), description_text_size)
    for word in word_list:
        text_width = font.size(word + " ")[0]
        if text_len + text_width > window_width:
            row += 1
            text_len = 5
            draw_text(word,highlight_text(word),text_len,4 + description_text_size*row,description_screen,description_text_size)
        else:
            draw_text(word,highlight_text(word),text_len,4 + description_text_size*row,description_screen,description_text_size)
        text_len += font.size(word + " ")[0]
    
    # If the item has stats draw the stats
    if val[0] in equip_keys:
        curr_y = description_text_size*(row+1) # Add 1 since we don't want to write on the same line as the description
        text_len = 5
        row = 0
        font = pygame.font.Font(open_file_in_same_directory('editundo.ttf'), stat_text_size)
        stats = all_equippable_stats[val[0]][val[1]]
        if stats['Attack'] != 0:
            word = stats['Attack']
            word = f'+{word}'
            text_width = font.size(word + " ")[0]
            draw_text(word,WHITE,text_len,4 + curr_y + stat_text_size*row,description_screen,stat_text_size)
            text_len += text_width
            draw_text('Attack',RED,text_len,4 + curr_y + stat_text_size*row,description_screen,stat_text_size)
            row += 1
            text_len = 5
        if stats['Defense'] != 0:
            word = stats['Defense']
            word = f'+{word}'
            text_width = font.size(word + " ")[0]
            draw_text(word,WHITE,text_len,4 + curr_y + stat_text_size*row,description_screen,stat_text_size)
            text_len += text_width
            draw_text('Defense',LIGHT_BLUE,text_len,4 + curr_y + stat_text_size*row,description_screen,stat_text_size)
            row += 1
            text_len = 5
        if stats['Special'] != None:
            word = stats['Special CD']
            word = f'{word} turns'
            text_width = font.size('Cooldown ')[0]
            draw_text('Cooldown ',YELLOW,text_len,4 + curr_y + stat_text_size*row,description_screen,stat_text_size)
            text_len += text_width
            draw_text(word,WHITE,text_len,4 + curr_y + stat_text_size*row,description_screen,stat_text_size)
    return description_screen

# Highlight word with certain colors
def highlight_text(word):
    if word == 'attack':
        return RED
    elif word == 'defense':
        return LIGHT_BLUE
    else:
        return WHITE

# Check if player is near an entrance. Checks up, down, left, right, and current tile.
# Returns True if entrance is in those checked tiles. Also returns the location of the entrance. Else return False
# If player is on the entrance, it will also return True.
def check_for_entrance(tiles_x,tiles_y,map_mat,tile_num):
    direc_list = [(-1,0),(1,0),(0,-1),(0,1),(0,0)]
    for direc in direc_list:
        x_check = tiles_x+direc[0]
        y_check = tiles_y+direc[1]
        if map_mat[y_check,x_check] == tile_num:
            return True,(x_check,y_check)
    return False,(None,None)
