import netgame_img as img
import pygame
tile_size = 64
from functions import random_shake

# Class for drawing and animating the enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self,name,enemy_id):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.id = enemy_id
        self.enemy_img = img.enemy_img_dict