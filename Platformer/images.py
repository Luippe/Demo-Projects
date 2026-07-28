import pygame
import numpy as np
from pathlib import Path
import display_manager as display

display.initialize()

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = (BASE_DIR / "assets").as_posix()
FONT_PATH = (BASE_DIR / "editundo.ttf").as_posix()

#load needed images
healing_stone = pygame.image.load(f'{ASSETS_DIR}/items/healing_stone.png').convert_alpha()
bullet_blob_img = pygame.image.load(f'{ASSETS_DIR}/bullets/3.png').convert_alpha()
bullet_blob_img = pygame.transform.scale(bullet_blob_img, (15, 15))
exit_img = pygame.image.load(f'{ASSETS_DIR}/2.png').convert_alpha()
money_icon = pygame.image.load(f'{ASSETS_DIR}/coins/3.png').convert_alpha()
money_icon = pygame.transform.scale(money_icon, (50,50))
item_frame = pygame.image.load(f'{ASSETS_DIR}/item_frame.png').convert_alpha()
item_frame = pygame.transform.scale(item_frame, (70,70))
flare_img = pygame.image.load(f'{ASSETS_DIR}/torch/flare.png').convert_alpha()
rock_img = pygame.image.load(f'{ASSETS_DIR}/projectiles/rock.png').convert_alpha()
rock_img = pygame.transform.scale(rock_img, (10,10))
rock_icon = pygame.image.load(f'{ASSETS_DIR}/items/rock.png').convert_alpha()
rock_icon = pygame.transform.scale(rock_icon, (50,50))
particle_img = pygame.image.load(f'{ASSETS_DIR}/particles/0.png').convert_alpha()
particle_img = pygame.transform.scale(particle_img, (15,15))
bamboo_icon = pygame.image.load(f'{ASSETS_DIR}/bamboo/0.png').convert_alpha()
blank_img = pygame.image.load(f'{ASSETS_DIR}/blank.png').convert_alpha()


#load images for upgrade
upgrade = pygame.image.load(f'{ASSETS_DIR}/upgrade/0.png').convert_alpha()


#load images for background
bg1 = pygame.image.load(f'{ASSETS_DIR}/Background3.png').convert_alpha()
bg1 = pygame.transform.scale(bg1, (1600,1100))
bg2 = pygame.image.load(f'{ASSETS_DIR}/Background2.png').convert_alpha()
bg2 = pygame.transform.scale(bg2, (1600,1100))
bg3 = pygame.image.load(f'{ASSETS_DIR}/Background1.png').convert_alpha()
bg3 = pygame.transform.scale(bg3, (1600,1100))
bg4 = pygame.image.load(f'{ASSETS_DIR}/Background4.png').convert_alpha()
bg4 = pygame.transform.scale(bg4, (1600,1100))
bg5 = pygame.image.load(f'{ASSETS_DIR}/background/mountain.png').convert_alpha()
bg5 = pygame.transform.scale(bg5, (1920, 1080))
bg6 = pygame.image.load(f'{ASSETS_DIR}/background/snow_bg.png').convert_alpha()
bg6 = pygame.transform.scale(bg6, (1920, 1080))


#load images for shop
images_item = []
shard_list = []
shop_list = []
shop_keeper_list = []
shop_bar = pygame.image.load(f'{ASSETS_DIR}/shop/page.png').convert_alpha()
shop_bar = pygame.transform.scale(shop_bar, (1000, 1080))
upgrade_shard = pygame.image.load(f'{ASSETS_DIR}/shop/shard0.png').convert_alpha()
paper = pygame.image.load(f'{ASSETS_DIR}/shop/paper0.png').convert_alpha()
paper = pygame.transform.scale(paper, (375, 250))
for num in range(8):
    shop_keeper = pygame.image.load(f'{ASSETS_DIR}/shop/shop_keeper{num}.png').convert_alpha()
    shop_keeper = pygame.transform.scale(shop_keeper, (300, 200))
    shop_keeper_list.append(shop_keeper)
for num in range(2):
    img_shop = pygame.image.load(f'{ASSETS_DIR}/shop/shop{num}.png').convert_alpha()
    img_shop = pygame.transform.scale(img_shop, (300, 200))
    shop_list.append(img_shop)
for num in range(5):
    shard = pygame.image.load(f'{ASSETS_DIR}/shop/shard{num}.png').convert_alpha()
    shard = pygame.transform.scale(shard, (100, 100))
    shard_list.append(shard)
for num in range(3):
    img_item = pygame.image.load(f'{ASSETS_DIR}/shop/{num}.png').convert_alpha()
    if num == 1 or num == 2:
        img_item = pygame.transform.scale(img_item, (60,96))
    images_item.append(img_item)
shard_transform_list = []
for num in range(10):
    img = pygame.transform.scale(upgrade_shard, (100 + 4*num, 100 + 4*num))
    shard_transform_list.append(img)

#load upgrades for the roid
upgrade_list = []
for num in range(1,3):
    img_upg = pygame.image.load(f'{ASSETS_DIR}/upgrade/{num}.png').convert_alpha()
    img_upg = pygame.transform.scale(img_upg, (30,48))
    upgrade_list.append(img_upg)

upgrade_stand = pygame.image.load(f'{ASSETS_DIR}/upgrade/0.png').convert_alpha()

#load images for menu screen
menu_img_list = []
for x in range(60):
    img = pygame.image.load(f'{ASSETS_DIR}/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (50,50))
    menu_img_list.append(img)


#hitbox for the roid
roid_hitbox = pygame.image.load(f'{ASSETS_DIR}/player/0.png').convert_alpha()
roid_hitbox = pygame.transform.scale(roid_hitbox, (50,90))


#load images for start button
start = pygame.image.load(f'{ASSETS_DIR}/background/start.png').convert_alpha()
start_dark = pygame.image.load(f'{ASSETS_DIR}/shop/start_dark.png').convert_alpha()
start_list = []
for num in range(10):
    img = pygame.transform.scale(start, (450 + 4*num, 450 + 4*num))
    start_list.append(img)


#load images for health bar
images_health = []
for num in range(0,4):
    health_bar = pygame.image.load(f'{ASSETS_DIR}/health_bar/health_bar{num}.png').convert_alpha()
    health_bar = pygame.transform.scale(health_bar, (80,80))
    images_health.append(health_bar)


#load images for potions
images_potion = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
for i in range(0,4):
    for j in range(0,3):
        potion_img = pygame.image.load(f'{ASSETS_DIR}/items/potion{i}-{j}.png').convert_alpha()
        potion_img = pygame.transform.scale(potion_img, (150,150))
        images_potion[i][j] = potion_img


#load images for player
images_right = []
images_left = []
for num in range(0,6):
    img_right = pygame.image.load(f'{ASSETS_DIR}/player_run/player{num}.png').convert_alpha()
    img_right = pygame.transform.scale(img_right, (60,96))
    img_left = pygame.transform.flip(img_right, True, False)
    images_right.append(img_right)
    images_left.append(img_left)

right_idle = []
left_idle = []
for num in range(0,6):
    img_right = pygame.image.load(f'{ASSETS_DIR}/player/{num}.png').convert_alpha()
    img_right = pygame.transform.scale(img_right, (60,96))
    img_left = pygame.transform.flip(img_right, True, False)
    right_idle.append(img_right)
    left_idle.append(img_left)

right_jump = []
left_jump = []
for num in range(0,9):
    img_right = pygame.image.load(f'{ASSETS_DIR}/player_jump/{num}.png').convert_alpha()
    img_right = pygame.transform.scale(img_right, (60,100))
    img_left = pygame.transform.flip(img_right, True, False)
    if num == 7:
        img_right = pygame.image.load(f'{ASSETS_DIR}/player_jump/7.png').convert_alpha()
        img_right = pygame.transform.scale(img_right, (60,100))
        img_left = pygame.transform.flip(img_right, True, False)
    right_jump.append(img_right)
    left_jump.append(img_left)

right_attack = []
left_attack = []
for num in range(0,4):
    img_right = pygame.image.load(f'{ASSETS_DIR}/player_attack/idle{num}.png').convert_alpha()
    img_right = pygame.transform.scale(img_right, (285,265))
    img_left = pygame.transform.flip(img_right, True, False)
    right_attack.append(img_right)
    left_attack.append(img_left)

up_attack_right = []
up_attack_left = []
for num in range(0, 3):
    img_right = pygame.image.load(f'{ASSETS_DIR}/player_attack/up_attack{num}.png').convert_alpha()
    img_right = pygame.transform.scale(img_right, (190,305))
    img_left = pygame.transform.flip(img_right, True, False)
    up_attack_right.append(img_right)
    up_attack_left.append(img_left)


up_air_right = []
up_air_left = []
for num in range(0, 3):
    img_right = pygame.image.load(f'{ASSETS_DIR}/player_attack/up_air{num}.png').convert_alpha()
    img_right = pygame.transform.scale(img_right, (190,305))
    img_left = pygame.transform.flip(img_right, True, False)
    up_air_right.append(img_right)
    up_air_left.append(img_left)


down_air_right = []
down_air_left = []
for num in range(0, 3):
    img_right = pygame.image.load(f'{ASSETS_DIR}/player_attack/down_air{num}.png').convert_alpha()
    img_right = pygame.transform.scale(img_right, (190,305))
    img_left = pygame.transform.flip(img_right, True, False)
    down_air_right.append(img_right)
    down_air_left.append(img_left)


right_forward_air = []
left_forward_air = []
for num in range(0,4):
    img_right = pygame.image.load(f'{ASSETS_DIR}/player_attack/forward_air{num}.png').convert_alpha()
    img_right = pygame.transform.scale(img_right, (290,270))
    img_left = pygame.transform.flip(img_right, True, False)
    right_forward_air.append(img_right)
    left_forward_air.append(img_left)

right_hurt = []
left_hurt = []
hurt_right = pygame.image.load(f'{ASSETS_DIR}/player_hurt/0.png').convert_alpha()
hurt_right = pygame.transform.scale(hurt_right, (60,96))
hurt_left = pygame.transform.flip(hurt_right, True, False)
right_hurt.append(hurt_right)
left_hurt.append(hurt_left)

#load images for spirit
images_spirit = pygame.image.load(f'{ASSETS_DIR}/Spirit/0.png').convert_alpha()
images_spirit_origin = pygame.image.load(f'{ASSETS_DIR}/Spirit/1.png').convert_alpha()


#load images for coins
image_coins = []
for num in range(0,3):
    img = pygame.image.load(f'{ASSETS_DIR}/coins/{num}.png').convert_alpha()
    img = pygame.transform.scale(img, (30, 30))
    image_coins.append(img)


#load images for icicles
icicle_hitbox = pygame.transform.scale(blank_img, (50,70))
images_icicle = []
images_break = []
for num in range(0,12):
    img = pygame.image.load(f'{ASSETS_DIR}/icicle/{num}.png').convert_alpha()
    img = pygame.transform.scale(img, (100,100))
    images_icicle.append(img)
for num in range(13, 19):
    img = pygame.image.load(f'{ASSETS_DIR}/icicle/{num}.png').convert_alpha()
    img = pygame.transform.scale(img, (100,100))
    images_break.append(img)
ice_break = pygame.image.load(f'{ASSETS_DIR}/icicle/19.png').convert_alpha()
ice_break = pygame.transform.scale(ice_break, (50,50))
images_break.append(ice_break)


#load images for blob
gb_hitbox = pygame.transform.scale(blank_img, (100,80))
images_blob_left = []
images_blob_right = []
for num in range(0,9):
    img_left = pygame.image.load(f'{ASSETS_DIR}/blob/{num}.png').convert_alpha()
    img_left = pygame.transform.scale(img_left, (100,100))
    img_right = pygame.transform.flip(img_left, True, False)
    images_blob_left.append(img_left)
    images_blob_right.append(img_right)
for num in range(9, 12):
    img_left = pygame.image.load(f'{ASSETS_DIR}/blob/{num}.png').convert_alpha()
    img_left = pygame.transform.scale(img_left, (100,200))
    img_right = pygame.transform.flip(img_left, True, False)
    images_blob_left.append(img_left)
    images_blob_right.append(img_right)


#load images for bats
images_bat = []
for num in range(0,9):
    img = pygame.image.load(f'{ASSETS_DIR}/bat/{num}.png').convert_alpha()
    img_bat = pygame.transform.scale(img, (80,80))
    images_bat.append(img_bat)


#load images for green blob
blob_hitbox = pygame.transform.scale(blank_img, (50,100))
images_gb_left = []
images_gb_right = []
for num in range(0,7):
    hurt_right = pygame.image.load(f'{ASSETS_DIR}/green_blob/{num}.png').convert_alpha()
    hurt_right = pygame.transform.scale(hurt_right, (100,100))
    hurt_left = pygame.transform.flip(hurt_right, True, False)
    images_gb_left.append(hurt_left)
    images_gb_right.append(hurt_right)


#load images for green blob explosion
gb_explosion = []
for num in range(9,12):
    explosion = pygame.image.load(f'{ASSETS_DIR}/green_blob/{num}.png').convert_alpha()
    explosion = pygame.transform.scale(explosion, (200,200))
    gb_explosion.append(explosion)


#load images for snow mounder
sm_hitbox = pygame.transform.scale(blank_img, (90,50))
images_sm_left = []
images_sm_right = []
for num in range(0,10):
    img_right = pygame.image.load(f'{ASSETS_DIR}/snow mounder/{num}.png').convert_alpha()
    img_right = pygame.transform.scale(img_right, (100,100))
    img_left = pygame.transform.flip(img_right, True, False)
    images_sm_right.append(img_right)
    images_sm_left.append(img_left)


#load images for snow mounder's bullet
sm_bullet_hitbox = pygame.transform.scale(blank_img, (20,20))
bullet_mounder = pygame.image.load(f'{ASSETS_DIR}/projectiles/1.png').convert_alpha()


#load image for snow mounder's hat
sm_hat = pygame.image.load(f'{ASSETS_DIR}/snow mounder/hat.png').convert_alpha()

#load image for ice_spike
ice_spike = pygame.image.load(f'{ASSETS_DIR}/ice_tile/spike0.png').convert_alpha()

#load images for cubeoid
images_cubeoid_left = []
images_cubeoid_right = []
cubeoid_hitbox = pygame.transform.scale(blank_img, (100,100))
for num in range(0,25):
    img_left = pygame.image.load(f'{ASSETS_DIR}/cubeoid/{num}.png').convert_alpha()
    img_left = pygame.transform.scale(img_left, (200,200))
    img_right = pygame.transform.flip(img_left, True, False)
    if num == 23:
        img_left = pygame.image.load(f'{ASSETS_DIR}/cubeoid/23.png').convert_alpha()
        img_left = pygame.transform.scale(img_left, (100,100))
        img_right = pygame.transform.flip(img_left, True, False)
    images_cubeoid_right.append(img_right)
    images_cubeoid_left.append(img_left)


#load images for snow soldier
ss_hitbox = pygame.transform.scale(blank_img, (80,85))
images_ss_left = []
images_ss_right = []
for num in range(0,11):
    img_left = pygame.image.load(f'{ASSETS_DIR}/snow_soldier/{num}.png').convert_alpha()
    img_left = pygame.transform.scale(img_left, (140,140))
    img_right = pygame.transform.flip(img_left, True, False)
    images_ss_right.append(img_right)
    images_ss_left.append(img_left)


#load images for torch
images_torch = []
for num in range(3,5):
        img_torch = pygame.image.load(f'{ASSETS_DIR}/torch/{num}.png').convert_alpha()
        img_torch = pygame.transform.scale(img_torch, (50,50))
        images_torch.append(img_torch)


#load images for melee hitbox
hitbox_img = []
hitbox = pygame.transform.scale(blank_img, (120,75))
hitbox_img.append(hitbox)


#dust particles
dust = []
for num in range(1,3):
    dust_img = pygame.image.load(f'{ASSETS_DIR}/particles/{num}.png').convert_alpha()
    dust_img = pygame.transform.scale(dust_img, (20,20))
    dust.append(dust_img)


#load images for slash effects for enemies
images_slash = []
for num in range(0,2):
    slash_img = pygame.image.load(f'{ASSETS_DIR}/enemy_damage_effect/{num}.png').convert_alpha()
    images_slash.append(slash_img)

#load images for sling shot
images_crystal = []
images_crystal_active = []
for num in range(0,4):
    crystal = pygame.image.load(f'{ASSETS_DIR}/sling/{num}.png').convert_alpha()
    images_crystal.append(crystal)
for num in range(4,8):
    crystal = pygame.image.load(f'{ASSETS_DIR}/sling/{num}.png').convert_alpha()
    images_crystal_active.append(crystal)

ice_boss_hitbox = pygame.transform.scale(blank_img, (80,85))
ice_boss = pygame.image.load(f'{ASSETS_DIR}/boss/0.png').convert_alpha()
ice_arm = pygame.image.load(f'{ASSETS_DIR}/boss/1.png').convert_alpha()

#load images for pause menu
images_pause = []
for num in range(0,1):
    pause_img = pygame.image.load(f'{ASSETS_DIR}/pause/{num}.png').convert_alpha()
    images_pause.append(pause_img)
