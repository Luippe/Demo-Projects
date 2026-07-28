import pygame
from os import path
from pygame.locals import *
import random
import numpy as np
import display_manager as display

BLACK = (0,0,0)
WHITE = (255,255,255)

#function to draw text onto screen
def draw_text(text, font, text_col, x, y, surface, alpha_val):
    img = font.render(text, True, text_col)
    img.set_alpha(alpha_val)
    surface.blit(img, (x, y))


#function to update particles
def particle_effects(selected_surface, mob):
    for particle in mob.spread_particles:
        pygame.draw.rect(selected_surface, BLACK, (particle[0][0], particle[0][1], 5, 5))
        if particle[3] >= 0:
            particle[3] -= 1
            particle[0][0] += particle[1]*np.cos(particle[2])
            particle[0][1] -= particle[1]*np.sin(particle[2])
        elif particle[3] < 0:
            mob.spiral_particles.append([[particle[0][0], particle[0][1]], particle[1], particle[2], [particle[0][0], particle[0][1]], (particle[0][0] - mob.player_x - 25)/2, (particle[0][1] - mob.player_y - 30)/2, np.sqrt((particle[0][0] - mob.player_x - 25)**2 + (particle[0][1] - mob.player_y - 30)**2)/2, 100])
            mob.spread_particles.remove(particle)
    for particle in mob.spiral_particles:
        pygame.draw.circle(selected_surface, BLACK, (particle[0][0], particle[0][1]), 10)
        mob.trail_particles.append([[particle[0][0], particle[0][1]], 255, 10])
        if mob.spiral == True:
            particle[0][0] = (particle[3][0] - particle[4]) - particle[6] * np.cos(particle[2] + np.pi)
            particle[0][1] = (particle[3][1] - particle[5]) + particle[6] * np.sin(particle[2] + np.pi)
            particle[2] += 0.02
            if mob.time >= 260:
                mob.spiral_particles.remove(particle)
    for particle in mob.trail_particles:
        pygame.draw.circle(selected_surface, (0,0,0,particle[1]), (particle[0][0], particle[0][1]), particle[2])
        particle[2] -= 0.2
        particle[1] -= 5
        if particle[1] < 0 or mob.time >= 260:
            mob.trail_particles.remove(particle)
            

#class to animate upgrade particles
class Upgrade_Animation():
    def __init__(self, screen_width, screen_height, x, y, transparent_surface, screen, ability_num):
        self.font = pygame.font.SysFont('Futura', 50)
        self.transparent_surface = transparent_surface
        self.ability_num = ability_num
        self.surface_copy = screen.copy()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player_x = x
        self.player_y = y
        self.spiral = False
        self.run = True
        self.time = 0
        self.dimming = 255
        self.tutorial = False
        self.spread_particles = []
        self.spiral_particles = []
        self.trail_particles = []
        for num in range(random.randint(20,30)):
            self.spread_particles.append([[self.player_x + 25, self.player_y + 30], random.randint(10,15), random.randint(0,360)*np.pi/180, random.randint(20,50)])
        

    def update(self, surface):
        while self.run:
            self.transparent_surface.fill((0,0,0,0))
            surface.blit(self.surface_copy, (0,0))
            particle_effects(self.transparent_surface, self)
            if len(self.spread_particles) == 0:
                self.time += 1
                if self.time >= 100:
                    self.spiral = True
            if len(self.spiral_particles) == 0 and self.spiral == True:
                self.dimming -= 10
                if self.dimming <= 10:
                    self.spiral = False
                    self.tutorial = True
                else:
                    self.transparent_surface.fill((0,0,0,self.dimming))
            if self.tutorial == True:
                if self.ability_num == 0:
                    draw_text('Press Left Shift to Dash', self.font, BLACK, self.screen_width / 2 - 100, self.screen_height / 2, self.transparent_surface, 120)
            surface.blit(self.transparent_surface, (0,0))
            for event in pygame.event.get():
                if event.type == pygame.KEYUP and event.key == pygame.K_LSHIFT:
                    self.run = False
            display.present(surface)
        
