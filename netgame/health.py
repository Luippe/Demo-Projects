import pygame
from pygame.locals import *
from functions import *
import netgame_img as img
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (200, 25, 25)
GREEN = (144, 201, 120)
DARK_GREY = (105, 105, 105)
YELLOW = (242,242,73)
GREEN = (144, 201, 120)
LIGHT_BLUE = (147, 207, 240)
ORANGE = (255, 69, 0)
GOLD = (255,215,0)
DARKNESS = (30,30,30)

# Define global variables used throughout the class
tile_size = 64
center = (320, 256)

# Class for displaying health
class Health:
    def __init__(self,player,canvas,network):
        self.health_width,self.health_height = (100,30)
        self.icon_health_width,self.icon_health_height = (100,5)
        self.health_screen = pygame.Surface((self.health_width,self.health_height))
        self.health_text_screen = pygame.Surface((150,self.health_height), SRCALPHA)
        self.damage_surface_list = []
        self.border_thickness = 2
        self.main_screen = canvas.screen
        self.network = network
        self.player = player
        self.curr_health = self.player.curr_health
        self.max_health = self.player.max_health
        self.health_text_screen.fill((0,0,0,0))
        draw_text(f'{self.curr_health}/{self.max_health}',WHITE,0,0,self.health_text_screen,30)
        self.health_screen.fill(RED)
        pygame.draw.rect(self.health_screen,GREEN,(0,0,self.curr_health,self.health_height))
        pygame.draw.rect(self.health_screen,WHITE,(0,0,self.health_width,self.health_height),self.border_thickness)

    # Main function that updates this class
    def update(self):
        self.draw_damage_num()
        self.draw_health()
        self.draw_other_health()

    # Draw your own health bar on screen, as well as the texts
    def draw_health(self):
        self.main_screen.blit(self.health_text_screen,(170,10))
        self.main_screen.blit(self.health_screen,(300,10))

    # Get text surface for displaying damage on screen
    def get_damage_number_surface(self,damage,damage_x,damage_y,offset=(0,0)):
        font = pygame.font.Font(open_file_in_same_directory('editundo.ttf'), 30)
        text_surf = font.render(f'{damage}', True, (255,25,25,255))
        self.damage_surface_list.append([text_surf, center_text_x(text_surf, damage_x + offset[0] + (tile_size/2)), (damage_y + offset[1] + tile_size/2), 255, 0])

    # Draw the damage text onto screen. Add a fade
    def draw_damage_num(self):
        for text_surf in self.damage_surface_list:
            text_surf[3] -= 5
            text_surf[4] += 2
            if text_surf[3] >= 0:
                text_surf[0].set_alpha(text_surf[3])
                self.main_screen.blit(text_surf[0],(text_surf[1],text_surf[2] - text_surf[4]))
            else:
                self.damage_surface_list.remove(text_surf)

    # Redraw health bar when taking damage
    def redraw_health(self):
        self.health_screen.fill(RED)
        self.health_text_screen.fill((0,0,0,0))
        draw_text(f'{self.player.curr_health}/{self.player.max_health}',WHITE,0,0,self.health_text_screen,30)
        pygame.draw.rect(self.health_screen,GREEN,(0,0,self.player.curr_health,self.health_height))
        pygame.draw.rect(self.health_screen,WHITE,(0,0,self.health_width,self.health_height),self.border_thickness)

    # Draw health bar for other players
    def draw_other_health(self):
        other_players = [n for n in self.network.player_dict if n != self.player] # Get player dict for other players
        for num, players in enumerate(other_players):
            if ((self.player.in_room_loc == players.in_room_loc) and (self.player.in_room_loc != (None,None))) or (self.player.ready_check == True and players.ready_check == True): # For other players, get their health if in same room
                max_health = players.max_health
                curr_health = players.curr_health
                pygame.draw.rect(self.main_screen,RED,(10,100+50*num,self.icon_health_width,self.icon_health_height))
                pygame.draw.rect(self.main_screen,GREEN,(10,100+50*num,curr_health*self.icon_health_width/max_health,self.icon_health_height))
                self.main_screen.blit(img.player_icon_list[players.id],(10,80+50*num))