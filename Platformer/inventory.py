import pygame
from os import path
from pygame.locals import *
import display_manager as display

TBLACK = (0,0,0,180)

class Inventory():
    def __init__(self, screen_width, screen_height, primary_surface, surface):
        self.timer = 0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.run = True
        pygame.draw.rect(surface, TBLACK, (0, 0, self.screen_width, self.screen_height))
        primary_surface.blit(surface, (0 ,0))

    def update(self, primary_surface, surface):
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    self.run = False
            display.present(primary_surface)
