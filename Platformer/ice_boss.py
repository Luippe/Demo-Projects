import pygame
import images as im
import numpy as np
from os import path
from pygame.locals import *

class Ice_Boss():
    def __init__(self, x, y, surface):
        self.hitbox = im.ice_boss_hitbox
        self.image = im.ice_boss
        self.surface = surface
        self.rect = self.hitbox.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.hitbox.get_width()
        self.height = self.hitbox.get_height()
        self.timer = 0

    def update(self):
        self.timer += 0.05
        self.surface.blit(self.image, (self.rect.x, self.rect.y + 10 * np.sin(self.timer)))

class Ice_Boss_Arm(pygame.sprite.Sprite):
    def __init__(self, x, y, surface, timer):
        pygame.sprite.Sprite.__init__(self)
        self.image = im.ice_arm
        self.hitbox = im.ice_boss_hitbox
        self.surface = surface
        self.rect = self.hitbox.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.timer = timer
    
    def update(self):
        self.timer += 0.05
        self.surface.blit(self.image, (self.rect.x, self.rect.y + 30 * np.sin(self.timer)))