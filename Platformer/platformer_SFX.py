import pygame
from pygame.locals import *
from pathlib import Path

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

SFX_DIR = (Path(__file__).resolve().parent / "assets" / "sfx").as_posix()

#SFX for when roid attacks
slash1 = pygame.mixer.Sound(f'{SFX_DIR}/slash1.wav')
slash2 = pygame.mixer.Sound(f'{SFX_DIR}/slash2.wav')
slash1.set_volume(0.8)
slash2.set_volume(0.8)
slash_list = [slash1, slash2]

#SFX for when roid lands
land = pygame.mixer.Sound(f'{SFX_DIR}/land.wav')
land.set_volume(0.2)

#BGM
bgm = pygame.mixer.Sound(f'{SFX_DIR}/BGM.wav')
bgm.set_volume(0.5)

#SFX for when roid slings
sling = pygame.mixer.Sound(f'{SFX_DIR}/Sling.wav')

#SFX for when buying
paper_list = []
for num in range(0,3):
    paper = pygame.mixer.Sound(f'{SFX_DIR}/paper{num}.wav')
    paper_list.append(paper)

enemy_hurt_list = []
for num in range(0,2):
    hurt = pygame.mixer.Sound(f'{SFX_DIR}/enemy_hurt{num}.wav')
    enemy_hurt_list.append(hurt)
