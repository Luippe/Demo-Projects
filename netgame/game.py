import pygame
import asyncio
import time
import numpy as np
import pygame._sdl2 as sdl2
from pygame.locals import *
from inventory import Inventory
from settings import Settings
from exit_room import ExitRoom
from player_action import Action
from action_particles import ActionParticles
from player_pathfind import PlayerPathFinding
from health import Health
from enemy_client import Enemy
import netgame_img as img
from functions import *

pygame.init()
pygame.mixer.quit()

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (200, 25, 25)
GREEN = (144, 201, 120)
DARK_GREY = (105, 105, 105)
YELLOW = (242,242,73)
LIGHT_BLUE = (147, 207, 240)
ORANGE = (255, 69, 0)
GOLD = (255,215,0)
DARKNESS = (30,30,30)

# Define global variables used throughout the class
tile_size = 64
center = (320, 256)
w,h=(704,576)
map_x,map_y = (112,64)
clock = pygame.time.Clock()

# Function for taking care of keyboard inputs
async def get_events(sum_delay,counter):
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEWHEEL and settings_class.open_settings == True:
            settings_class.scrolly += event.y
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:   #Toggle editor mode
                canvas.show_grid = not canvas.show_grid
            elif event.key == pygame.K_h:
                canvas.show_fps = not canvas.show_fps
            elif (event.key == settings_class.control_dict["Interact"]) and (inventory_class.open_inventory == False):
                if inventory_class.check_pickup(player.rect.x,player.rect.y) == False:  # If there are no items to pick up
                    ready_check,entrance_loc = check_for_entrance(player.rect.x,player.rect.y,canvas.map_mat,canvas.entrance_num)
                    if (ready_check == True) and (player.in_combat == False):    # Check if entrance is nearby
                        player.ready_check = not player.ready_check
                        if (player.rect.x,player.rect.y) == entrance_loc:   # If the player is on the entrance
                            pass
                        else:   # If the player is near entrance, move the player on top of the entrance
                            player.scrollx,player.scrolly = (-entrance_loc[0]*tile_size + center[0], -entrance_loc[1]*tile_size + center[1])
                            player.facing = (1,0)
            elif (event.key == settings_class.control_dict["Open Inventory"]) and (settings_class.open_settings == False):
                inventory_class.open_inventory = not inventory_class.open_inventory
                mini_map_class.draggable = not mini_map_class.draggable
                inventory_class.clicked_options = False
                inventory_class.clicked = False
                inventory_class.open_description = False
                action_class.open_special = False
            elif event.key == pygame.K_r:   #Request for a new map from the server
                network.get_map = True
                canvas.draw_once = False
                if canvas.tile_size == 6:
                    player.scrollx = 0
                    player.scrolly = 0
            elif event.key == pygame.K_g:   #Change canvas size
                # global tile_size
                if canvas.tile_size == 64:
                    # tile_size = 6
                    canvas.tile_size = 6
                else:
                    # tile_size = 64
                    canvas.tile_size = 64
                player.scrollx = 0
                player.scrolly = 0
            elif event.key == pygame.K_q:
                player.take_damage([10,[(player.rect.x,player.rect.y)]])
            elif event.key == settings_class.control_dict["Open Settings"] and inventory_class.open_inventory == False:
                mini_map_class.draggable = not mini_map_class.draggable
                if settings_class.open_settings == True:
                    inventory_class.control_dict = settings_class.control_dict
                settings_class.open_settings = not settings_class.open_settings
            elif event.key == settings_class.control_dict["Toggle Highlight"]:
                canvas.toggle_highlight = not canvas.toggle_highlight
            elif (event.key == settings_class.control_dict["Change Direction"]) and (player.move_allow == True):
                canvas.show_direction_grid = not canvas.show_direction_grid
                player.damage_tile_list = []
                player.damage_delay = 100
            elif event.key == pygame.K_ESCAPE:
                # network.task.cancel()
                print(f"AVERAGE DELAY IS: {sum_delay/counter}")
                pygame.quit()

# Initialize all the classes. All classes are global
def init_class(network_class):
    global player_dict,network,canvas,mini_map_class,settings_class,inventory_class,exit_class,enemy_class,health_class,action_class,particles
    network = network_class
    player_dict = network.player_dict
    player = player_dict[network.index]
    canvas = Canvas("Multiplayer Game")
    mini_map_class = MiniMap()
    health_class = Health(player,canvas,network)
    particles = ActionParticles(player,canvas)
    enemy_class = Enemy(canvas,network,player,mini_map_class,particles,health_class)
    settings_class = Settings(canvas,mini_map_class)
    exit_class = ExitRoom(canvas, settings_class, network, w, h)
    action_class = Action(player,canvas,network,particles)
    inventory_class = Inventory(player, canvas,mini_map_class,settings_class.control_dict, network, action_class)
    map_reset(network,player_dict,canvas,mini_map_class,inventory_class,exit_class,enemy_class,health_class,action_class)

# Class for player
class Player():
    def __init__(self, startx, starty,player_id):
        self.rect = pygame.Rect(startx,starty,1,1)
        self.scroll_velx = int(tile_size/8)
        self.scroll_vely = int(tile_size/8)
        self.scrollx,self.scrolly = (startx,starty)
        self.rect.x = (-self.scrollx+center[0])//tile_size
        self.rect.y = (-self.scrolly+center[1])//tile_size
        self.move_timer = 0
        self.curr_health,self.max_health = (100,100)
        self.move_allow = True
        self.held = False
        self.start_pathfind = False
        self.wall_tile_num = img.wall_tile_list
        self.direction = (0,-1)
        self.facing = (0,-1)
        self.delay_timer = 0
        self.timer_max = 5
        self.id = player_id
        self.map_mat = None
        self.sol_path = []
        self.in_room_loc = (0,0)
        self.turn = True
        self.dead = False
        self.in_combat = True
        self.ready_check = False
        self.other_obj_pos = []
        self.shake_list = []
        self.base_attack = 10
        self.base_defense = 0
        self.defense = 0
        self.attack = 0
        self.tot_attack = 0
        self.tot_defense = 0
        self.angle = 3*np.pi/2
        self.damage_tile_list = []
        self.damage = 0
        self.damage_delay = 100
        self.max_damage_delay = 0
        self.attack_order = [1]
        self.crit_chance = 0.02

    def player_move_keyboard(self, dirn):
        self.move_timer += 1
        if self.move_timer >= 8:
            self.move_timer = 0
            self.move_allow = True
            if self.in_combat == True:
                self.turn = False
        self.scrollx -= dirn[0]*self.scroll_velx
        self.scrolly -= dirn[1]*self.scroll_vely

    def keyboard_controls(self,tiles_x,tiles_y):
        # check for w,a,s,d key presses if keyboard movement is set to true in settings. else use mouse movements
        # Direction is determined by [dx,dy]. so [1,0] will move the player 1 right and 0 up
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]) and (self.move_allow == True) and (self.ready_check == False):
            action_class.close_all()
            checking = []
            if canvas.show_direction_grid == False:
                self.delay_timer += 1
            elif canvas.show_direction_grid == True:
                self.delay_timer = 0
            if keys[pygame.K_w]:
                self.facing = (0,-1)
                self.angle = 3*np.pi/2
            elif keys[pygame.K_a]:
                self.facing = (-1,0)
                self.angle = np.pi
            elif keys[pygame.K_s]:
                self.facing = (0,1)
                self.angle = np.pi/2
            elif keys[pygame.K_d]:
                self.facing = (1,0)
                self.angle = 0
            if (self.map_mat[tiles_y+self.facing[1], tiles_x+self.facing[0]] not in self.wall_tile_num) and [tiles_x+self.facing[0],tiles_y+self.facing[1]] not in self.other_obj_pos and self.delay_timer >= self.timer_max:
                self.move_allow = False
            else:
                self.move_allow = True
            #if moving diagonal, we need to check if there are no barriers in the diagonal direction
            #get 2x2 matrix (which will be flattened to 1x4) to check if there are any barriers using any()
            if keys[pygame.K_w] and keys[pygame.K_a]:
                self.facing = (-1,-1)
                self.angle = 5*np.pi/4
                checking = [j for sub in self.map_mat[tiles_y-1:tiles_y+1,tiles_x-1:tiles_x+1] for j in sub]
            elif keys[pygame.K_a] and keys[pygame.K_s]:
                self.facing = (-1,1)
                self.angle = 3*np.pi/4
                checking = [j for sub in self.map_mat[tiles_y:tiles_y+2,tiles_x-1:tiles_x+1] for j in sub]
            elif keys[pygame.K_s] and keys[pygame.K_d]:
                self.facing = (1,1)
                self.angle = np.pi/4
                checking = [j for sub in self.map_mat[tiles_y:tiles_y+2,tiles_x:tiles_x+2] for j in sub]
            elif keys[pygame.K_d] and keys[pygame.K_w]:
                self.facing = (1,-1)
                self.angle = 7*np.pi/4
                checking = [j for sub in self.map_mat[tiles_y-1:tiles_y+1,tiles_x:tiles_x+2] for j in sub]
            if checking != []:  # If there is diagonal movement. check surrounding
                if any(x in checking for x in self.wall_tile_num) == False and [tiles_x+self.facing[0],tiles_y+self.facing[1]] not in self.other_obj_pos and self.delay_timer >= self.timer_max:
                    self.move_allow = False
                else:
                    self.move_allow = True
        elif self.move_allow == True:
            self.delay_timer = 0
        if self.move_allow == False:
            self.direction = self.facing
            self.player_move_keyboard(self.direction)

    # Take damage. Data is given in [damage, [(x,y),(x1,y1)...], delay]. where x and y are tiles
    def handle_damage(self):
        self.damage_delay += 1
        if self.damage_delay >= self.max_damage_delay:
            self.damage_delay = 0
            # Iterate through the area. If there is a chunk of area, iterate through that
            for num in range(self.attack_order[0]):
                area = self.damage_tile_list[num]
                # Append tiles which will be highlighted
                particles.damage_tiles.append([(area[0] - player.rect.x)*tile_size + center[0],(area[1] - player.rect.y)*tile_size + center[1],150])
                if canvas.show_direction_grid == False:
                    for players in player_dict:
                        # If any player takes damage
                        if (players.rect.x,players.rect.y) == area:
                            damage = sorted([1,self.damage - players.defense - players.base_defense])[1]   # Make sure the damage is at least 1
                            particles.add_damage_particles(player.scrollx - players.scrollx,player.scrolly - players.scrolly, center)
                            health_class.get_damage_number_surface(damage, player.scrollx - players.scrollx, player.scrolly - players.scrolly, center)
                            players.shake_list = random_shake(-20,20,-20,20)
                    # If I take damage
                    if (player.rect.x,player.rect.y) == area:
                        damage = sorted([1,self.damage - self.defense - self.base_defense])[1]   # Make sure the damage is at least 1
                        if self.curr_health > 0:
                            self.curr_health -= damage
                        if self.curr_health <= 0:
                            self.curr_health = 0
                            self.dead = True
                        health_class.redraw_health()
            # Iterate through the tile list and attack order and remove the first element so we get the next one in the next iteration
            for num in range(self.attack_order[0]):
                self.damage_tile_list.pop(0)
            self.attack_order.pop(0)

    # When player is ready to enter the room
    def handle_ready(self):
        pass

# Class for game. main loop occurs here
class Game:
    def __init__(self,network_class):
        self.level = 0
        self.has_light = False
        init_class(network_class)
        self.room_rect_list = canvas.room_rect_list

    def new_map(self):
        enemy_class.enemy_pos = {}
        enemy_class.enemy_names = []
        enemy_class.shake_list = []
        map_reset(network,player_dict,canvas,mini_map_class,inventory_class,exit_class,enemy_class,health_class,action_class)
        self.room_rect_list = canvas.room_rect_list

    def new_player(self,new_player_dict):
        global player_dict,player
        player_dict = new_player_dict
        player = player_dict[network.index]

    def run(self,loop):
        run = True
        sum_delay = 0
        counter = 0
        global player
        player = player_dict[network.index]
        while run:
            clock.tick(60)
            start = time.time()
            x,y = pygame.mouse.get_pos()
            player.other_obj_pos = []
            for players in player_dict:
                players.rect.x = (-players.scrollx+center[0])/tile_size
                players.rect.y = (-players.scrolly+center[1])/tile_size
                if players.id != network.id:
                    player.other_obj_pos.append([players.rect.x,players.rect.y])
            player.in_room_loc = obj_in_room(self.room_rect_list,player.rect.x,player.rect.y)
            if len(player.damage_tile_list) > 0:
                player.handle_damage()
            # Update canvas
            canvas.draw_map(player.scrollx, player.scrolly,self.has_light)
            canvas.draw_selected_tile(x,y)
            canvas.draw_grid_or_fps()
            particles.draw_damage_tiles()
            enemy_class.draw()
            if canvas.show_direction_grid == True:
                canvas.draw_nearby_tiles(player.scrollx,player.scrolly,player.rect.x,player.rect.y)
                canvas.draw_attack_area()
            if canvas.tile_size == 64:
                # Draw players if their ready check is False
                for players in player_dict:
                    if players.ready_check == False:
                        player_center = (-players.scrollx + player.scrollx + center[0], -players.scrolly + player.scrolly + center[1])
                        canvas.draw_player(players.id, players.facing, player_center, players.shake_list)
                mini_map_class.update(x,y)
                if self.has_light == False:
                    canvas.draw_lighting()
            exit_class.update(player.rect.x,player.rect.y,center)
            health_class.update()
            if (settings_class.open_settings == True) and (player.move_allow == True):
                action_class.open_action = False
                settings_class.update()
            elif (inventory_class.open_inventory == True) and (player.move_allow == True):
                action_class.open_action = False
                inventory_class.update_inventory(player.rect.x,player.rect.y)
            elif player.turn == True:
                action_class.right_clicked(x,y)
                player.keyboard_controls(player.rect.x,player.rect.y)
            if (action_class.open_action == True) and (canvas.show_direction_grid == False):
                action_class.update()
            particles.draw_damage_particles()
            particles.special_img_fade()
            canvas.draw_cursor(x,y)
            # await canvas.update()
            # await get_events()
            # await asyncio.sleep(0.01)
            asyncio.run_coroutine_threadsafe(canvas.update(),loop)
            asyncio.run_coroutine_threadsafe(get_events(sum_delay,counter),loop)
            # asyncio.run_coroutine_threadsafe(asyncio.sleep(10),loop)
            # print(clock.get_fps())
            end = time.time()
            counter += 1
            sum_delay += (end-start)
            # print(end-start)
        print('game loop end')
        pygame.quit()

# Class for drawing objects (players, items, tiles, etc) onto screen
class Canvas:
    def __init__(self, name="None"):
        self.width = w
        self.height = h
        self.see_radius = 128
        self.tile_size = tile_size #originally 64
        self.screen = pygame.display.set_mode((w,h), pygame.SCALED|pygame.RESIZABLE)
        pygame.display.set_caption(name)
        self.lighting_screen = pygame.Surface((w,h))
        self.lighting_screen.set_colorkey((BLACK))
        self.screen_x,self.screen_y = (11,9)
        self.room_rect_list = None
        self.map_mat = None
        self.item_loc = None
        self.cursor_list = img.cursor_list
        self.stone_img = img.stone_dict
        self.stone_floor_img = img.stone_floor_dict
        self.floor_tiles = range(img.min_floor,img.max_floor)
        self.exit_num = range(img.min_exit,img.max_exit)
        self.shrine_num = range(img.min_shrine,img.max_shrine)
        self.entrance_num = range(img.min_entrance,img.max_entrance)
        self.wall_tile_num = range(0,15)
        self.selected_tile = img.item_select_list
        self.exit_tile = img.exit_floor_dict
        self.shrine_tile = img.shrine_dict
        self.entrance_tile = img.entrance_dict
        self.player_img = img.player_list
        self.all_obj_img_dict = img.all_obj_img_dict
        self.exit_animation_timer = 0
        self.show_grid = False
        self.show_fps = False
        self.toggle_highlight = False
        self.show_direction_grid = False
        self.custom_cursor = False
        self.draw_once = False
        self.show_attack_timer = 0
        self.lit_rooms = []

    @staticmethod
    async def update():
        pygame.display.update()

    # Draws the black lines
    def draw_grid_or_fps(self):
        if self.show_fps == True:
            draw_text(f"FPS:{round(clock.get_fps(),2)}",WHITE, 0,0,canvas.screen,50)
        if self.show_grid == True:
            for c in range(100):
                pygame.draw.line(self.screen, BLACK, (c * self.tile_size, 0), (c * self.tile_size, self.height))
            for c in range(100):
                pygame.draw.line(self.screen, BLACK, (0, c * self.tile_size), (self.width, c * self.tile_size))

    # Draw the map
    def draw_map(self,scrollx,scrolly,has_light):
        y_min,y_max,x_min,x_max = player_tiles_on_screen(scrollx,scrolly,padx=1,pady=1)
        if self.tile_size == 64:
            self.draw_once = False
            # Only load in tiles that fit in your screen
            for j in range(y_min,y_max):
                for i in range(x_min,x_max):
                    curr_loc = self.map_mat[j,i]
                    if curr_loc in self.floor_tiles:
                        self.screen.blit(self.stone_floor_img[curr_loc],(self.tile_size*i + scrollx,self.tile_size*j + scrolly,self.tile_size,self.tile_size))
                    elif curr_loc in self.wall_tile_num:
                        self.screen.blit(self.stone_img[curr_loc],(self.tile_size*i + scrollx,self.tile_size*j + scrolly,self.tile_size,self.tile_size))
                    elif curr_loc in self.exit_num:
                        self.map_mat[j,i], self.exit_animation_timer = tile_animation(curr_loc, img.min_exit,img.max_exit_frame, self.exit_animation_timer)
                        self.screen.blit(self.exit_tile[curr_loc],(self.tile_size*i + scrollx,self.tile_size*j + scrolly,self.tile_size,self.tile_size))
                    elif curr_loc in self.shrine_num:
                        self.screen.blit(self.shrine_tile[curr_loc],(self.tile_size*i + scrollx,self.tile_size*j + scrolly,self.tile_size,self.tile_size))
                    elif curr_loc in self.entrance_num:
                        self.screen.blit(self.entrance_tile[curr_loc],(self.tile_size*i + scrollx,self.tile_size*j + scrolly,self.tile_size,self.tile_size))
            # Draw items onto screen. Only draw items that are in the same room as players
            for name,val in self.item_loc.items():
                for loc in val:
                    if loc[1] < y_max and loc[1] > y_min and loc[0] > x_min and loc[0] < x_max:
                        m_room,n_room = obj_in_room(self.room_rect_list,loc[0],loc[1])
                        if  (m_room,n_room) in canvas.lit_rooms or ((m_room,n_room) == (None,None)):
                            self.screen.blit(self.all_obj_img_dict[name][loc[2]],(self.tile_size*loc[0] + scrollx,self.tile_size*loc[1] + scrolly,self.tile_size,self.tile_size))
        elif self.draw_once == False:
            self.draw_once = True
            for j in range(map_y):
                for i in range(map_x):
                    curr_loc = self.map_mat[j,i]
                    if curr_loc in self.floor_tiles:
                        pygame.draw.rect(self.screen, BLACK, (self.tile_size*i + scrollx,self.tile_size*j + scrolly,self.tile_size,self.tile_size))
                    if curr_loc in self.wall_tile_num:
                        pygame.draw.rect(self.screen, DARK_GREY, (self.tile_size*i + scrollx,self.tile_size*j + scrolly,self.tile_size,self.tile_size))
                    if curr_loc in self.exit_num:
                        pygame.draw.rect(self.screen, LIGHT_BLUE, (self.tile_size*i + scrollx,self.tile_size*j + scrolly,self.tile_size,self.tile_size))
                    if curr_loc in self.shrine_num:
                        pygame.draw.rect(self.screen, YELLOW, (self.tile_size*i + scrollx,self.tile_size*j + scrolly,self.tile_size,self.tile_size))
            for loc in self.item_loc:
                pygame.draw.rect(self.screen, RED,(self.tile_size*loc[0] + scrollx,self.tile_size*loc[1] + scrolly,self.tile_size,self.tile_size))
    
    # Draw nearby tiles when LCTRL (by default) is pressed
    def draw_nearby_tiles(self,scrollx,scrolly,tiles_x,tiles_y):
        m_room,n_room = obj_in_room(self.room_rect_list,tiles_x,tiles_y)
        y_min,y_max,x_min,x_max = player_tiles_on_screen(scrollx,scrolly)
        # Find intersection between the tiles on screen and walkable tiles in the room you are in
        if (m_room,n_room) != (None,None):
            player_room_rect = pygame.Rect(self.room_rect_list[m_room][n_room])
            for j in range(y_min,y_max):
                for i in range(x_min,x_max):
                    if player_room_rect.collidepoint(i,j):
                        pygame.draw.rect(self.screen,GOLD,(i*tile_size + scrollx,j*tile_size + scrolly,tile_size,tile_size),1)
            # Highlight tiles in which the player is looking at
            for const in range(6):
                look_tile = [const*player.facing[0] + tiles_x, const*player.facing[1] + tiles_y]
                if player_room_rect.collidepoint(look_tile):
                    pygame.draw.rect(self.screen,ORANGE,(look_tile[0]*tile_size + scrollx,look_tile[1]*tile_size + scrolly,tile_size,tile_size),5)

    # Draw the tiles in which the players will hit when attacking
    def draw_attack_area(self):
        self.show_attack_timer += 1
        if len(player.damage_tile_list) == 0:
            self.show_attack_timer += 1
            if self.show_attack_timer > 100:
                # Update the attack area as the player turns in different direction
                action_class.attack_order,action_class.attack_area = action_class.handle_attack(action_class.attack_diag, action_class.attack_linear)
                self.show_attack_timer = 0
                player.damage_tile_list = action_class.attack_area
                player.attack_order = action_class.attack_order
                player.max_damage_delay = action_class.max_damage_delay
                player.damage_delay = 100

    # Draw highlight around hovering tile and show cursor. Cursor size is 8x8 pixels
    def draw_selected_tile(self,x,y):
        if self.toggle_highlight == True:
            tiles_x = x//self.tile_size
            tiles_y = y//self.tile_size
            self.screen.blit(self.selected_tile[0],(tile_size*tiles_x-4,tile_size*tiles_y-4))

    def draw_cursor(self,x,y):
        if self.custom_cursor == True:
            self.screen.blit(self.cursor_list[0],(x-8,y-8))

    def draw_player(self, player_id, facing, loc, shake_list):
        if len(shake_list) > 0:
            self.screen.blit(self.player_img[player_id][facing],(loc[0] + shake_list[0][0], loc[1] + shake_list[0][1]))
            shake_list.pop(0)
        else:
            self.screen.blit(self.player_img[player_id][facing],loc)

    def draw_lighting(self):
        self.lighting_screen.fill(DARKNESS)
        surf,self.lit_rooms = lighting(self.lighting_screen,self.room_rect_list,player.scrollx,player.scrolly,player_dict)
        self.screen.blit(surf, (0,0), special_flags = BLEND_RGB_SUB)

# Class to draw minimap onto screen
class MiniMap:
    def __init__(self):
        self.mini_screen = pygame.Surface((700,500), SRCALPHA)
        self.obj_screen = pygame.Surface((700,500), SRCALPHA)
        self.enemy_screen = pygame.Surface((700,500), SRCALPHA)
        self.screen_rect = self.mini_screen.get_rect()
        self.map_x, self.map_x = (map_x,map_y)
        self.screen_rect.x,self.screen_rect.y = (0,100)
        self.prevx,self.prevy = (0,0)
        self.main_screen = canvas.screen
        self.scale = 6
        self.scale_by = 3   # Change self.scale_by to change the size of map
        self.held = False
        self.draggable = True
        self.color = LIGHT_BLUE
        self.player_color = WHITE
        self.item_color = YELLOW
        self.enemy_color = RED
        self.entrance_color = DARK_GREY
        self.blink_timer = 0
        self.blink_max = 20

    #find what rooms the player has gone into
    def update(self,x,y):
        player_rect_list = [x.rect for x in player_dict]
        self.obj_screen.fill((0,0,0,0))
        for player_rect in player_rect_list:
            if (num := player_rect.collidelist(self.unexplored_room_rect)) != -1:
                room_rect = self.unexplored_room_rect[num]
                left = room_rect.x - 1
                right = room_rect.x + room_rect.width + 1
                top = room_rect.y - 1
                bot = room_rect.y + room_rect.height + 1
                self.draw_room(self.map_mat[top:bot,left:right], room_rect.x, room_rect.y)
                self.unexplored_room_rect.pop(num)
            self.draw_player(player_rect.x,player_rect.y)
            self.draw_path(player_rect.x,player_rect.y)
        self.mouse_move(x,y)
        self.draw_items()
        self.draw_mini()

    # Draw the minimap. pygame.transform is not ideal so change later if possible. self.scale is constant, while self.scale_by is changeable
    def draw_mini(self):
        mini_screen = pygame.transform.scale_by(self.mini_screen,self.scale_by/self.scale)
        obj_screen = pygame.transform.scale_by(self.obj_screen,self.scale_by/self.scale)
        enemy_screen = pygame.transform.scale_by(self.enemy_screen,self.scale_by/self.scale)
        self.main_screen.blit(mini_screen,(self.screen_rect.x,self.screen_rect.y))
        self.main_screen.blit(obj_screen,(self.screen_rect.x,self.screen_rect.y))
        self.main_screen.blit(enemy_screen,(self.screen_rect.x,self.screen_rect.y))

    # Draw items onto obj_screen since items can be picked up and dropped
    def draw_items(self):
        for val in self.display_items_list:
            pygame.draw.circle(self.obj_screen,self.item_color,(self.scale*val[0] + self.scale/2,self.scale*val[1] + self.scale/2),3)

    # Reset the minimap for a new map
    def reset_mini_map(self,map_mat, room_list,item_loc):
        self.mini_screen.fill((0,0,0,0))
        self.obj_screen.fill((0,0,0,0))
        # Make map_mat which sets all wall tiles equal to 0 and walkable tile to 1. However exclude the entrance tile
        self.map_mat = [[element not in player_dict[network.index].wall_tile_num for element in row] for row in map_mat]
        self.map_mat = np.array(self.map_mat,dtype=int)
        self.wall_mat = np.copy(self.map_mat)
        self.item_mat = [item[0:2] for sublist in list(item_loc.values()) for item in sublist]
        self.room_list = room_list
        self.unexplored_room_rect = [j for sub in canvas.room_rect_list for j in sub]
        self.y_num,self.x_num = np.shape(room_list)[0:2]
        self.display_items_list = []
        self.display_enemy_list = []

    # Draw the rooms onto the transparent canvas
    # Checks up, down, left, right to see where the walls are at
    # Additionally, locate any item. If there are any, append the location to a list so items can be displayed
    def draw_room(self,room_region, xstart,ystart):
        y_num,x_num = np.shape(room_region)
        for j in range(1,y_num-1):
            for i in range(1,x_num-1):
                x = i + xstart - 1
                y = j + ystart - 1
                if room_region[j,i] > 0:
                    self.map_mat[y,x] = -1
                    if ((x,y) in self.item_mat):
                        self.display_items_list.append((x,y))
                    if (canvas.map_mat[y,x] >= img.min_exit and canvas.map_mat[y,x] < img.max_exit_frame):
                        pygame.draw.rect(self.mini_screen,LIGHT_BLUE,(self.scale*x,self.scale*y,self.scale,self.scale))
                    if room_region[j,i-1] == 0:
                        pygame.draw.line(self.mini_screen,self.color,(self.scale*x,self.scale*y),(self.scale*x,self.scale*y+self.scale))
                    if room_region[j,i+1] == 0:
                        pygame.draw.line(self.mini_screen,self.color,(self.scale*x+self.scale,self.scale*y),(self.scale*x+self.scale,self.scale*y+self.scale))
                    if room_region[j+1,i] == 0:
                        pygame.draw.line(self.mini_screen,self.color,(self.scale*x,self.scale*y+self.scale),(self.scale*x+self.scale,self.scale*y+self.scale))
                    if room_region[j-1,i] == 0:
                        pygame.draw.line(self.mini_screen,self.color,(self.scale*x,self.scale*y),(self.scale*x+self.scale,self.scale*y))

    #draw the path that the player walks through. player has a 3x3 vision
    #get a 5x5 matrix. in a 3x3 region near you, find tiles where you have no explored. find the walls near those unexplored tiles
    def draw_path(self,tiles_x,tiles_y):
        if self.map_mat[tiles_y,tiles_x] != -1:
            surr_mat = self.map_mat[tiles_y-2:tiles_y+3,tiles_x-2:tiles_x+3]
            if len(surr_mat) > 0:
                for j in range(1,4):
                    for i in range(1,4):
                        x = i + tiles_x - 2
                        y = j + tiles_y - 2
                        if (canvas.map_mat[y,x] in canvas.entrance_num):
                            pygame.draw.rect(self.mini_screen,GREEN,(self.scale*x,self.scale*y,self.scale,self.scale))
                        if surr_mat[j,i] == 1:
                            if surr_mat[j,i-1] == 0:
                                pygame.draw.line(self.mini_screen,self.color,(self.scale*x,self.scale*y),(self.scale*x,self.scale*y+self.scale))
                            if surr_mat[j,i+1] == 0:
                                pygame.draw.line(self.mini_screen,self.color,(self.scale*x+self.scale,self.scale*y),(self.scale*x+self.scale,self.scale*y+self.scale))
                            if surr_mat[j+1,i] == 0:
                                pygame.draw.line(self.mini_screen,self.color,(self.scale*x,self.scale*y+self.scale),(self.scale*x+self.scale,self.scale*y+self.scale))
                            if surr_mat[j-1,i] == 0:
                                pygame.draw.line(self.mini_screen,self.color,(self.scale*x,self.scale*y),(self.scale*x+self.scale,self.scale*y))
            self.map_mat[tiles_y,tiles_x] = -1

    # Make the mini-map moveable with mouse drag
    def mouse_move(self,x,y):
        if self.draggable == True:
            # If mouse is held, move the mini-map
            if (self.screen_rect.collidepoint((x,y))) and (pygame.mouse.get_pressed()[0] == 1) and (self.held == False):
                self.held = True
            elif self.held == True:
                self.screen_rect.x += (x-self.prevx)
                self.screen_rect.y += (y-self.prevy)
            if (pygame.mouse.get_pressed()[0] == 0):
                self.held = False
            self.prevx,self.prevy = (x,y)

    # Draw player on the mini-map
    def draw_player(self,tiles_x,tiles_y):
        self.blink_timer += 1
        if self.blink_timer >= 2*self.blink_max:
            self.blink_timer = 0
        elif self.blink_timer >= self.blink_max:
            pygame.draw.rect(self.obj_screen, self.player_color, (self.scale*tiles_x,self.scale*tiles_y,self.scale,self.scale))

