import pygame
import pickle
from os import path
from pygame.locals import *
import images as im
import numpy as np
import random
import display_manager as display
clock = pygame.time.Clock()
fps = 60
tile_size = 50
run = True
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (144, 201, 120)
points = []

font = pygame.font.SysFont('Futura', 50)
def draw_text(text, font, text_col, x, y, surface):
    img = font.render(text, True, text_col)
    surface.blit(img, (x, y))


#draw menu screen
def draw_menu(menu_data, screen):
    row_count = 0
    for y, row in enumerate(menu_data):
        col_count = 0
        for x, tile in enumerate(row):
            if tile >= 0 and tile != 12:
                screen.blit(im.menu_img_list[tile], (x * tile_size, y * tile_size))
            col_count += 1
        row_count += 1


#draw and update particle effects
def particle_effects(surface, mob):
    for particle in mob.leaf_list:
        particle[6] += np.pi/100
        points = []
        if np.cos(particle[6]) < 0 and particle[8] == -1:
            particle[8] = 1
            for num in range(0,6):
                particle[num][0] *= -1
        elif np.cos(particle[6]) > 0 and particle[8] == 1:
            particle[8] = -1
            for num in range(0,6):
                particle[num][0] *= -1
        for num in range(0,6):
            particle[num][1] += particle[11]
            points.append([particle[7] + particle[num][0] + particle[9]*np.sin(particle[6]), particle[num][1]])
        pygame.draw.polygon(surface, particle[10], points)
    for particle in mob.hover_particles:
        particle[3] -= 1
        particle[0][0] += particle[1]*np.cos(particle[2])
        particle[0][1] -= particle[1]*np.sin(particle[2])
        pygame.draw.rect(mob.surface, WHITE, (particle[0][0], particle[0][1], 5, 5))
        if particle[3] <= 0:
            mob.hover_particles.remove(particle)
    for particle in mob.snow_list:
        particle[0][1] += particle[3]
        particle[1] -= 0.02*particle[2]
        if particle[1] <= 1:
            mob.snow_list.remove(particle)
        pygame.draw.circle(surface, WHITE, [int(particle[0][0]), int(particle[0][1])], particle[4])


#class for menu screen
class Menu():
    def __init__(self, surface, transparent_surface, world_data):
        self.bg = im.bg5
        self.menu_data = world_data
        self.start_list = im.start_list
        self.surface = surface
        self.transparent_surface = transparent_surface
        self.transparent_surface.set_alpha(120)
        self.hover = False
        self.hover_particles = []
        self.leaf_list = []
        self.snow_list = []
        self.start_zoom = 0
        self.transition_timer = 0
        self.click = False
        self.transition = False
        self.snow = True
        self.run = True
        pygame.mixer.music.load(f'{im.ASSETS_DIR}/sfx/BGM.wav')
        pygame.mixer.music.play(-1)

    #draw and update the menu screen
    def update(self):
        while self.run:
            # self.run = False
            clock.tick(fps)
            self.surface.blit(self.bg, (0,0))
            self.transparent_surface.fill((0,0,0,0))
            draw_menu(self.menu_data, self.surface)
            if self.snow == True:
                random_appear = random.randint(0,20)
                if random_appear == 0:
                    snow_x = random.randint(0,1920)
                    # start position, life span, decay speed, falling speed, radius
                    self.snow_list.append([[snow_x, 0], random.randint(5, 10), random.randint(1,3), random.randint(1,3), random.randint(1,3)])
            elif self.snow == False:
                random_appear = random.randint(0,100)
                if random_appear == 0:
                    leaf_x = random.randint(0,1920)
                    rand_angle = random.randint(0,90)*np.pi/180
                    self.leaf_list.append([[10*np.sin(rand_angle), -10*np.cos(rand_angle)],
                                            [4*np.cos(np.pi/4 - rand_angle), -4*np.sin(np.pi/4 - rand_angle)],
                                            [4*np.cos(np.pi/4 + rand_angle), 4*np.sin(np.pi/4 + rand_angle)],
                                            [-8*np.sin(rand_angle), 8*np.cos(rand_angle)],
                                            [-4*np.cos(np.pi/4 - rand_angle), 4*np.sin(np.pi/4 - rand_angle)],
                                            [-4*np.cos(np.pi/4 + rand_angle), -4*np.sin(np.pi/4 + rand_angle)],
                                            random.randint(0,10), leaf_x, 1, random.randint(50,100), random.choice([(97, 138, 61), (144, 201, 120), (151, 88, 12)]), random.randint(1,3)])
            particle_effects(self.surface, self)
            pos = display.get_mouse_pos()
            x = pos[0]
            y = pos[1]
            if 573 < x < 879 and 560 < y < 680 and self.transition == False:
                self.start_zoom += 1
                self.transparent_surface.set_alpha(120 + 15*self.start_zoom)
                if self.start_zoom >= 10:
                    self.start_zoom = 9
                self.transparent_surface.blit(self.start_list[self.start_zoom], (500 - 2*self.start_zoom, 400 - 2*self.start_zoom))
                draw_text('Start', pygame.font.SysFont('Futura', 50 + self.start_zoom), BLACK, 680 - (self.start_zoom/2), 610 - (self.start_zoom/2), self.transparent_surface)                 
                if self.hover == False:
                    for num in range(random.randint(10,20)):
                        self.hover_particles.append([[726, 620], random.randint(3,5), random.randint(0,360)*np.pi/180, random.randint(50,100)])
                    self.hover = True
                elif pygame.mouse.get_pressed()[0] == 1 and self.click == False:
                    self.click = True
            elif self.transition == False:
                self.transparent_surface.set_alpha(120)
                self.hover = False
                self.start_zoom = 0
                self.transparent_surface.blit(self.start_list[0], (500,400))
                draw_text('Start', font, BLACK, 680, 610, self.transparent_surface)
            if pygame.mouse.get_pressed()[0] == 0 and self.click == True:
                self.transition = True
            if self.transition == True:
                pygame.mixer.music.fadeout(1000)
                self.surface.blit(self.start_list[self.start_zoom], (500 - 2*self.start_zoom, 400 - 2*self.start_zoom))
                draw_text('Start', pygame.font.SysFont('Futura', 50 + self.start_zoom), BLACK, 680 - (self.start_zoom/2), 610 - (self.start_zoom/2), self.surface)
                self.transition_timer += 2
                pygame.draw.rect(self.transparent_surface, (0, 0, 0, self.transition_timer), (0, 0, 1920, 1080))
                if self.transition_timer >= 254:
                    break
            self.surface.blit(self.transparent_surface, (0,0))
            # draw_text(f'FPS: {"{:.3f}".format(clock.get_fps())}', font, WHITE, 1700, 50, self.surface)
            for event in pygame.event.get():
                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
            display.present(self.surface)
