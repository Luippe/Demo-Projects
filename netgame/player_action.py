import netgame_img as img
import pygame
from pygame.locals import *
import numpy as np
from functions import draw_text,weave_two_lists,add_two_lists
import random
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (200, 25, 25)
YELLOW = (242,242,73)
GREY = (67,67,67)
LIGHT_BLUE = (147, 207, 240)
ORANGE = (255, 69, 0)
GOLD = (255,215,0)
tile_size = 64
w,h=(704,576)
center = (320, 256)

# Class for player action such as attacks, spells, etc...
class Action:
    def __init__(self,player,canvas,network,particles):
        self.option_width, self.option_height = (120,30)
        self.option_screen = pygame.Surface((128,192), SRCALPHA)
        self.detail_screen = pygame.Surface((w,h), SRCALPHA)
        self.particle_screen = pygame.Surface((w,h), SRCALPHA)
        self.special_screen = pygame.Surface((128,192), SRCALPHA)    # Open when special is selected
        self.option_words = ['Attack','Abilities','Specials','Defend']
        self.open_option = img.open_action_list
        self.option_rect = self.open_option[0].get_rect()
        self.special_rect = self.open_option[0].get_rect()
        self.option_select = img.option_select_list
        self.canvas = canvas
        self.main_screen = canvas.screen
        self.network = network
        self.particles = particles
        self.open_action = False
        self.open_special = False
        self.player = player
        self.attack_delay_timer = 0
        self.wall_tile_list = img.wall_tile_list

        self.max_damage_delay = 0
        self.attack_linear = [[(1,0)]]
        self.attack_diag = [[(1,-1)]]
        self.special_data_list = []

        # Draw text and option onto screen beforehand
        self.option_screen.fill((67,67,67,150))
        self.option_screen.blit(self.open_option[0],(0,0))
        for num in range(len(self.option_words)):
            draw_text(self.option_words[num], WHITE, 10, 10 + self.option_height*num, self.option_screen, 30)

    # Open action option when right clicking on screen
    def right_clicked(self,x,y):
        if (pygame.mouse.get_pressed()[2] == 1) and (self.clicked == False):
            self.open_action = True
            self.open_special = False
            self.clicked = True
            self.option_rect.x,self.option_rect.y = (x,y)
            self.option_rect_list = [pygame.Rect(self.option_rect.x + 4, self.option_rect.y + self.option_height*j + 4, self.option_width, self.option_height) for j in range(len(self.option_words))]
        elif (pygame.mouse.get_pressed()[2] == 0):
            self.clicked = False

    # Main update function for action class
    def update(self):
        self.detail_screen.fill((0,0,0,0))
        x,y = pygame.mouse.get_pos()
        self.right_clicked(x,y)
        if self.open_action == True:
            self.select_action(x,y)
            if self.open_special == True:
                self.draw_special()
                self.select_special(x,y)
        self.draw_action()

    # Draw the action option onto screen
    def draw_action(self):
        self.main_screen.blit(self.option_screen,(self.option_rect.x,self.option_rect.y))
        self.main_screen.blit(self.detail_screen,(0,0))

    # Draw all special moves
    def draw_special(self):
        self.main_screen.blit(self.special_screen, (self.option_rect.x + self.option_rect.width - 4, self.option_rect.y))

    # If player clicks outside the option rect, close the option
    def clicked_out(self,x,y):
        if (pygame.mouse.get_pressed()[0] == 1) and not self.option_rect.collidepoint((x,y)) and not self.special_rect.collidepoint((x,y)):
            self.close_all()

    # Close all action window
    def close_all(self):
        self.clicked = False
        self.open_action = False
        self.open_special = False
        
    # Select action after right clicking
    def select_action(self,x,y):
        self.clicked_out(x,y)
        for num, obj in enumerate(self.option_rect_list):
            if obj.collidepoint((x,y)):
                self.detail_screen.blit(self.option_select[0], (obj.x,obj.y))
                if (pygame.mouse.get_pressed()[0] == 1) and (self.open_action == True):
                    # If player clicks on any of the actions, do the following
                    # Attack (num == 0)
                    # Abilities (num == 1)
                    # Specials (num == 2)
                    # Defend (num == 3)
                    self.open_special = False
                    if (num == 0):  # Handle attack, then send the data
                        self.clicked = False
                        self.open_action = False
                        self.attack_order,self.attack_area = self.handle_attack(self.attack_diag, self.attack_linear)
                        self.send_attack(self.player.attack + self.player.base_attack, self.attack_area, self.max_damage_delay, self.attack_order)
                        if self.player.in_combat == True:
                            self.player.turn = False
                    elif (num == 1):
                        pass
                    elif (num == 2):
                        self.open_special = True
                        self.special_rect.x,self.special_rect.y = (self.option_rect.x + self.option_width + 8,self.option_rect.y + 4)
                        self.special_rect_list = [pygame.Rect(self.option_rect.x + self.option_width + 8, self.option_rect.y + self.option_height*j + 4, self.option_width, self.option_height) for j in range(len(self.special_data_list))]
                    elif (num == 3):
                        pass
    
    # Function for when player selects a special move
    def select_special(self,x,y):
        self.clicked_out(x,y)
        for num, obj in enumerate(self.special_rect_list):
            if obj.collidepoint((x,y)):
                self.detail_screen.blit(self.option_select[0], (obj.x,obj.y))
                if (pygame.mouse.get_pressed()[0] == 1) and (self.open_special == True):
                    # if self.special_data_list[num][-1] == 0:
                    self.open_special = False
                    self.handle_special_moves(self.special_data_list[num])
                    self.special_data_list[num][-1] = self.special_data_list[num][-2]
                    self.particles.special_img_data = [self.special_data_list[num][2].copy(), 20]
                    self.redraw_special()

    # Handle normal attacks
    def handle_attack(self, attack_diag, attack_linear,pierce=False):
        # Get the tile in which the player has attacked and deal damage to whatever is there
        if (self.player.facing[0] != 0) and (self.player.facing[1] != 0):   # If the player is facing diagonally (diag)
            angle = self.player.angle + np.pi/4
            attack_tiles = attack_diag
        else:   # If the player is facing horizontally or vertically (linear)
            attack_tiles = attack_linear
            angle = self.player.angle
        # Calculate the location of tiles when the player is facing different ways. Use 2D rotation matrix. Because attack_area is a row vector
        # we need to turn it into a column vector so we can multiply it by the rotation matrix
        rot_mat = np.array([[np.cos(angle), -np.sin(angle)],
                            [np.sin(angle), np.cos(angle)]])
        # Attacks cannot go through walls, so handle that
        attack_area = []
        attack_order = []
        playerx,playery = (self.player.rect.x,self.player.rect.y)
        for vec in attack_tiles:
            temp_tiles = []
            temp_order = []
            vec_rotated = np.transpose(np.matmul(rot_mat,np.transpose(vec)))
            vec_rounded = [(round(val[0]) + playerx, round(val[1]) + playery) for val in vec_rotated]
            for tile in vec_rounded:
                if (self.canvas.map_mat[tile[1],tile[0]] in self.wall_tile_list) or (tile in attack_area):
                    if pierce == True:  # Only special moves can pass through walls
                        pass
                    else:
                        break
                else:
                    temp_order.append(1)
                    temp_tiles.append(tile)
            attack_order = add_two_lists(attack_order, temp_order)  # Add the orders of 1's
            attack_area = weave_two_lists(attack_area, temp_tiles)   # Weave the lists such that we have attack_area in the right order
        return attack_order,attack_area

    # Handle special moves
    def handle_special_moves(self, data):
        if data[3] == 'Attack':
            attack_data = data[4]
            attack_order,attack_area = self.handle_attack(attack_data[1], attack_data[0], True)
            self.send_attack(20, attack_area, attack_data[2], attack_order)
            

    # Handle cooldown for abilities and special moves
    def handle_cooldown(self):
        for special in self.special_data_list:
            if special[-1] > 0:
                special[-1] -= 1
        self.redraw_special()

    # Send the attack data to the server
    def send_attack(self, damage, attack_area, max_damage_delay, attack_order):
        # do_action = [damage, tile(s) to damage, delay between each tile attack, order of attack]
        self.network.do_action = {'type':'action','id':self.network.id,'action':'attack','data':[damage, attack_area, max_damage_delay, attack_order]}
    
    # Draw text and option onto screen beforehand
    def redraw_special(self):
        self.special_screen.fill((67,67,67,150))
        self.special_screen.blit(self.open_option[0],(0,0))
        for num,data in enumerate(self.special_data_list):
            pygame.draw.rect(self.special_screen, (147, 207, 240, 150), (4, 4 + self.option_height*num, self.option_width, 4 + self.option_height))
            self.special_screen.blit(data[1],(12,12 + self.option_height*num))
            draw_text(data[0], WHITE, 32, 16 + self.option_height*num, self.special_screen, 10)
            draw_text(f'{data[-1]}', GOLD, 100, 12 + self.option_height*num, self.special_screen, 20)
            

