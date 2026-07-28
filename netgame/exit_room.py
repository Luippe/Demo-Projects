import pygame
from pygame.locals import *
import random
import netgame_img as img
from functions import draw_text
BLACK = (0,0,0)
WHITE = (255,255,255)
LIGHT_BLUE = (147, 207, 240)

tile_size = 64
# Class for when exiting a room
class ExitRoom:
    def __init__(self,canvas,settings,network,w,h):
        self.exit_tile = list(range(img.min_exit,img.max_exit_frame))
        self.network = network
        self.map_mat = canvas.map_mat
        self.control_dict = settings.control_dict
        self.transition = False
        self.show_level = False
        self.exiting_animation = False
        self.fade_screen = pygame.Surface((w,h),SRCALPHA)
        self.timer = 0
        self.fade_max = 255
        self.black_screen_max = 500
        self.canvas = canvas
        self.level = 0
        self.map_reset = False
        self.particle_list = []
        self.particle_vel = [-4,4]
        self.particle_life = [20,30]
        self.got_on = False

    # Update the exit
    def update(self,tiles_x,tiles_y,center):
        keys = pygame.key.get_pressed()
        # If player interacts with the exit, fade screen to black and move onto next floor
        if self.map_mat[tiles_y,tiles_x] in self.exit_tile: # Add particles when player goes on exit tile [[x location, y location], x velocity, y velocity, life span]
            if self.got_on == False:
                [self.particle_list.append([[center[0] + tile_size/2, center[1] + tile_size/2],
                                            random.randint(self.particle_vel[0],self.particle_vel[1]),
                                            random.randint(self.particle_vel[0],self.particle_vel[1]),
                                            random.randint(self.particle_life[0],self.particle_life[1])]) for i in range(15)]
                self.got_on = True
            if keys[self.control_dict["Interact"]]:
                self.transition = True
                self.exiting_animation = True
        elif self.got_on == True:
            self.got_on = False
        if self.exiting_animation == True:
            self.fade_screen.fill((0,0,0,0))
            self.timer += 3
        if self.transition == True:
            print(self.timer)
            self.fade_screen.fill((0,0,0,self.timer))
            # Once the screen fades to black, show the next level onto screen while loading for a new map
            if self.timer >= self.fade_max:
                self.timer = 0
                self.transition = False
                self.show_level = True
                self.network.get_map = True
                self.level += 1
        elif self.show_level == True:
            self.fade_screen.fill((0,0,0,255))
            draw_text(f"Floor {self.level}",WHITE,100,100,self.fade_screen,50)
            if self.timer >= self.black_screen_max:
                self.timer = 0
                self.show_level = False
                self.exiting_animation = False
                self.fade_screen.fill((0,0,0,0))
        self.canvas.screen.blit(self.fade_screen,(0,0))
        self.show_particles()
        
    # Create particle effects when player goes onto the exit tile
    def show_particles(self):
        # print(self.particle_list)
        for particle in self.particle_list:
            particle[0][0] += particle[1]
            particle[0][1] -= particle[2]
            particle[3] -= 1
            pygame.draw.rect(self.canvas.screen, LIGHT_BLUE, [int(particle[0][0]), int(particle[0][1]), 5, 5])
            if particle[3] <= 0:
                self.particle_list.remove(particle)
