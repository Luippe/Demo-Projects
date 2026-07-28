import pygame
import numpy as np
import os
import sys
from functions import draw_text,open_file_in_same_directory,scale_and_center_word

enemy_names = ['goblin','ogre','whisp']
WHITE = (255,255,255)

pygame.init()
screen = pygame.display.set_mode((0,0),pygame.HIDDEN)
#tiles 0~14 are all wall tiles
#tiles 15~17 are all floor tiles
#tile 18~28 is exit tile
#tile 28~38 is shrine tile
#tile 38 is entrance tile

#min is inclusive
#max is not inclusive
#ex: min of 15 and max of 18 means the dict will have keys 15,16 and 17
walkable_list = []
wall_tile_list = []
wall_tile_list = list(range(0,15))
wall_tile_list.append(37)
wall_tile_list.append(38)

stone_list = []
file_path = open_file_in_same_directory("netgame_img\\scaled tiles\\stone walls")
len_stone = 15
min_stone = 0
max_stone = 15
for num in range(len_stone):
    stone_list.append(pygame.image.load(file_path + f"\\rock{num}.png").convert_alpha())
stone_dict = dict(zip(range(min_stone, max_stone+1), stone_list))

stone_floor_list = []
file_path = open_file_in_same_directory("netgame_img\\scaled tiles\\stone floors")
len_floor = 3
min_floor = 15
max_floor = 18
walkable_list.append(15)
walkable_list.append(16)
walkable_list.append(17)
for num in range(len_floor):
    stone_floor_list.append(pygame.image.load(file_path + f"\\stone_floor{num}.png").convert_alpha())
stone_floor_dict = dict(zip(range(min_floor, max_floor), stone_floor_list))

# get the image for the players
player_list = []
player_icon_list = []
dirn_list = [(0,-1),(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1)]
file_path = open_file_in_same_directory("netgame_img\\player")
for num in range(5):
    temp_list = []
    orig_player = pygame.image.load(file_path + f"\\player{num}.png").convert_alpha()
    player_icon = pygame.transform.scale(orig_player,(16,16))
    player_icon_list.append(player_icon)
    orig_player_rot = pygame.transform.rotate(orig_player,45)
    orig_player_rot = pygame.transform.chop(orig_player_rot,(0,0,15,15))
    orig_player_rot = pygame.transform.chop(orig_player_rot,(64,64,15,15))
    for i in range(4):
        img = pygame.transform.rotate(orig_player, i*90)
        img_rot = pygame.transform.rotate(orig_player_rot, i*90)
        temp_list.append(img)
        temp_list.append(img_rot)
    player_list.append(dict(zip(dirn_list,temp_list)))

enemy_list = []
file_path = open_file_in_same_directory("netgame_img\\enemy")
for num in range(len(enemy_names)): # For each enemy name
    temp_list = []
    orig_enemy = pygame.image.load(file_path + f"\\enemy{num}.png").convert_alpha()
    orig_enemy_rot = pygame.transform.rotate(orig_enemy,45)
    orig_enemy_rot = pygame.transform.chop(orig_enemy_rot,(0,0,12,12))
    orig_enemy_rot = pygame.transform.chop(orig_enemy_rot,(64,64,15,15))
    for i in range(4):  # For rotating image
        img = pygame.transform.rotate(orig_enemy, i*90)
        img_rot = pygame.transform.rotate(orig_enemy_rot, i*90)
        temp_list.append(img)
        temp_list.append(img_rot)
    enemy_list.append(dict(zip(dirn_list,temp_list)))
enemy_img_dict = dict(zip(enemy_names, enemy_list))


#===================ARMOR AND WEAPONS===================
armor_dict = {'chest':[], 'head':[], 'legs':[]}
equipment_icon_dict = {'chest':[], 'head':[], 'legs':[], 'weapon':[], 'charm':[]}
equipment_fade_dict = {'chest':[], 'head':[], 'legs':[], 'weapon':[], 'charm':[]}
file_path = open_file_in_same_directory("netgame_img\\armor\\chest")
num_armor = 4
for num in range(num_armor):
    armor_img = pygame.image.load(file_path + f"\\chest{num}.png").convert_alpha()
    armor_dict['chest'].append(armor_img)
    equipment_icon_dict['chest'].append(pygame.transform.scale(armor_img,(16,16)))
    equipment_fade_dict['chest'].append(pygame.transform.scale(armor_img,(32,32)))
    
file_path = open_file_in_same_directory("netgame_img\\armor\\legs")
for num in range(num_armor):
    armor_img = pygame.image.load(file_path + f"\\legs{num}.png").convert_alpha()
    armor_dict['legs'].append(armor_img)
    equipment_icon_dict['legs'].append(pygame.transform.scale(armor_img,(16,16)))
    equipment_fade_dict['legs'].append(pygame.transform.scale(armor_img,(32,32)))

file_path = open_file_in_same_directory("netgame_img\\armor\\head")
for num in range(num_armor):
    armor_img = pygame.image.load(file_path + f"\\head{num}.png").convert_alpha()
    armor_dict['head'].append(armor_img)
    equipment_icon_dict['head'].append(pygame.transform.scale(armor_img,(16,16)))
    equipment_fade_dict['head'].append(pygame.transform.scale(armor_img,(32,32)))

weapon_dict = {'weapon':[]}
file_path = open_file_in_same_directory("netgame_img\\weapon")
num_weapons = 11
for num in range(num_weapons):
    weapon_img = pygame.image.load(file_path + f"\\weapon{num}.png").convert_alpha()
    weapon_dict['weapon'].append(weapon_img)
    equipment_icon_dict['weapon'].append(pygame.transform.scale(weapon_img,(16,16)))
    equipment_fade_dict['weapon'].append(pygame.transform.scale(weapon_img,(32,32)))

#======================================================


setting_list = []
file_path = open_file_in_same_directory("netgame_img\\setting")
tab_names = ['Game','Control','Others']
for num in range(3):
    image = pygame.image.load(file_path + f"\\setting{num}.png").convert_alpha()
    for num in range(3):
        draw_text(tab_names[num], WHITE, 20 + 168*num,30,image,40)
    setting_list.append(image)


inventory_list = []
tab_names = ['Items', 'Equipment', 'Stats']
file_path = open_file_in_same_directory("netgame_img\\inventory")
for num in range(3):
    image = pygame.image.load(file_path + f"\\inventory{num}.png").convert_alpha()
    for num in range(3):
        center_x,center_y,letter_size = scale_and_center_word(tab_names[num],280,64)
        draw_text(tab_names[num], WHITE, 20 + 168*num + center_x, 16 + center_y, image, letter_size)
    inventory_list.append(image)


open_option_list = []
file_path = open_file_in_same_directory("netgame_img\\inventory")
for num in range(1):
    open_option_list.append(pygame.image.load(file_path + f"\\open_option.png").convert_alpha())


item_select_list = []
file_path = open_file_in_same_directory("netgame_img\\inventory")
for num in range(1):
    item_select_list.append(pygame.image.load(file_path + f"\\item_select.png").convert_alpha())


option_select_list = []
file_path = open_file_in_same_directory("netgame_img\\inventory")
for num in range(1):
    option_select_list.append(pygame.image.load(file_path + "\\option_select.png").convert_alpha())

item_description_list = []
file_path = open_file_in_same_directory("netgame_img\\inventory")
for num in range(1):
    item_description_list.append(pygame.image.load(file_path + f"\\item_description{num}.png").convert_alpha())

test_item_dict = {'item':[]}
file_path = open_file_in_same_directory("netgame_img\\items\\test_item")
for num in range(6):
    test_item_dict['item'].append(pygame.image.load(file_path + f"\\test_item{num}.png").convert_alpha())

open_action_list = []
file_path = open_file_in_same_directory("netgame_img\\action")
for num in range(1):
    open_action_list.append(pygame.image.load(file_path + "\\open_action.png").convert_alpha())

exit_list = []
min_exit,max_exit = (18,28)
max_exit_frame =  24
exit_frame_delay = 10
len_exit = max_exit - min_exit
file_path = open_file_in_same_directory("netgame_img\\scaled tiles\\exit")
for num in range(len_exit):
    exit_list.append(pygame.image.load(file_path + f"\\exit{num}.png").convert_alpha())
exit_floor_dict = dict(zip(range(min_exit, max_exit), exit_list))

shrine_list = []
min_shrine,max_shrine = (28,38)
len_shrine = max_shrine - min_shrine
file_path = open_file_in_same_directory("netgame_img\\scaled tiles\\shrine")
for num in range(len_shrine):
    shrine_list.append(pygame.image.load(file_path + f"\\shrine{num}.png").convert_alpha())
shrine_dict = dict(zip(range(min_shrine, max_shrine), shrine_list))

entrance_list = []
min_entrance,max_entrance = (38,39)
len_entrance = max_entrance - min_entrance
file_path = open_file_in_same_directory("netgame_img\\scaled tiles\\room entrance")
for num in range(len_entrance):
    entrance_list.append(pygame.image.load(file_path + '\\room_entrance.png').convert_alpha())
entrance_dict = dict(zip(range(min_entrance, max_entrance), entrance_list))

cursor_list = []
file_path = open_file_in_same_directory("netgame_img\\cursor")
for num in range(1):
    cursor_list.append(pygame.image.load(file_path + f"\\cursor{num}.png").convert_alpha())
exit_floor_dict = dict(zip(range(min_exit, max_exit), exit_list))


all_obj_img_dict = test_item_dict.copy()
all_obj_img_dict.update(armor_dict)
all_obj_img_dict.update(weapon_dict)
pygame.quit()