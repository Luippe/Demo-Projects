import pygame
import random
from pygame.locals import *
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (200,25,25)
DARK_RED = (100,0,0)
YELLOW = (242,242,73)
GREY = (67,67,67)
LIGHT_BLUE = (147,207,240)
GOLD = (255,215,0)

tile_size = 64
w,h=(704,576)
center = (320, 256)

class ActionParticles:
    def __init__(self,player,canvas):
        self.damage_particle_list = []
        self.player = player
        self.main_screen = canvas.screen
        dmg_min_vel = 2
        dmg_max_vel = 6
        self.damage_tiles = []
        self.damage_particle_list = []
        self.damage_particle_vel = [i for i in range(-dmg_max_vel,dmg_max_vel+1) if (i >= dmg_min_vel) or (i <= -dmg_min_vel)]
        self.damage_particle_life = (5,15)
        self.particle_screen = pygame.Surface((w,h), SRCALPHA)
        self.special_img_data = None

    # Create particle effects when player gets damaged. Offset = center for player, and is (0,0) for enemy
    def add_damage_particles(self,damage_x,damage_y,offset=(0,0)):
        [self.damage_particle_list.append([[damage_x + offset[0] + (tile_size/2), damage_y + offset[1] + (tile_size/2)],
                                            random.choice(self.damage_particle_vel),
                                            random.choice(self.damage_particle_vel),
                                            random.randint(self.damage_particle_life[0],self.damage_particle_life[1]),
                                            random.choice([RED,DARK_RED])]) for i in range(15)]
        
       
    # If an enemy or ally is hit, show damage particles
    def draw_damage_particles(self):
        if len(self.damage_particle_list) > 0:
            self.particle_screen.fill((0,0,0,0))  
            for particle in self.damage_particle_list:
                particle[0][0] += particle[1]
                particle[0][1] -= particle[2]
                particle[3] -= 1
                if particle[3] <= 0:
                    self.damage_particle_list.remove(particle)
                pygame.draw.rect(self.particle_screen, particle[4], [int(particle[0][0]), int(particle[0][1]), 5, 5])
            self.main_screen.blit(self.particle_screen,(0,0))

    # Show tiles in which the damage is being done on
    def draw_damage_tiles(self):
        if len(self.damage_tiles) > 0:
            self.particle_screen.fill((0,0,0,0))  
            for tile in self.damage_tiles:
                tile[2] -= 10
                if tile[2] <= 0:
                    self.damage_tiles.remove(tile)  
                    continue    # If tile[2] goes below 0, we can't draw it so continue
                pygame.draw.rect(self.particle_screen, (255,215,0,tile[2]), [tile[0], tile[1], tile_size, tile_size])
            self.main_screen.blit(self.particle_screen,(0,0))

    # Draw the equipment when its special move is used
    def special_img_fade(self):
        if self.special_img_data != None:
            self.special_img_data[1] -= 1
            if self.special_img_data[1] <= 0:
                self.special_img_data[0].fill((255,255,255,240),None,pygame.BLEND_RGBA_MULT)
            self.main_screen.blit(self.special_img_data[0], (center[0] + 16, center[1] + 16))
            if self.special_img_data[1] == -30:
                self.special_img_data = None
            