from math import ceil, floor
from xml.dom.pulldom import parseString
import pygame
import button
import pickle
import menu
import numpy as np
import images as im
import game_over as go
import ice_boss as ib
import platformer_SFX as sfx
import upgrade_animate as upg
from os import path
from pygame.locals import *
import random
import time
import pause
import display_manager as display
import frame_probe as probe

flags = FULLSCREEN | DOUBLEBUF

pygame.init()
clock = pygame.time.Clock()
fps = 60

DATA_DIR = path.join(path.dirname(path.abspath(__file__)), 'assets', 'data')


def get_level_data_path(level_number, layer=''):
    return path.join(DATA_DIR, f'level{level_number}_data{layer}')


#define game variables
side_margin = 3001
lower_margin = 100
tile_size = 50
tile_types = 77
SHOP_TILE = 39
current_tile = 0
GREEN = (144, 201, 120)
LIGHT_BLUE = (147, 207, 240)
DARK_GREEN = (80, 120, 80)
WHITE = (255, 255, 255)
WHITE_BG = (200,200,200)
GREY = (169, 169, 169)
DARK_GREY = (105, 105, 105)
ORANGE = (255, 69, 0)
YELLOW = (220, 220, 0)
BROWN = (139, 69, 19)
dust_color = [DARK_GREY, GREY]
snow_color = [WHITE, LIGHT_BLUE]
dirt_color = [GREEN, BROWN]
RED = (200, 25, 25)
DARK_RED = (150, 25, 25)
BLACK = (0,0,0)
death_particle_color = [ORANGE, RED]
scroll = 0
level = 0
attack_allow = False
scroll_left = False
scroll_right = False
slinging = False
menu_screen = True
show_hitbox = False
show_debug_info = False
scroll_speed = 10
pending_scroll_dx = 0
allow = 0
button_page = 0
grid_allow = 0
melee_allow = 1
particle_list = []
snow_particle_list= []
death_particle_list = []
water_particle_list = []
keys_list = [K_w, K_a, K_s, K_d, K_SPACE, K_e]
particle_allow = 0
attack_cooldown = 0
slinging_timer = 0
screen = display.initialize()
screen_width, screen_height = display.LOGICAL_SIZE
transparent_surface = pygame.Surface((screen_width, screen_height), SRCALPHA)
pygame.display.set_caption('Platformer')
health_bar = im.images_health
game_over_index = 0
lag_counter = 0
lag_time = 0

#make button list
button_list = []
button_col = 0
button_row = 0

#empty tile list
world_data = []
bg_data = []
front_data = []
for row in range(32):
    r = [-1] * 256
    bg_data.append(r)
    world_data.append(r)
    front_data.append(r)


#function to reset level
def reset_level():
    bat_group.empty()
    blob_green_group.empty()
    bullet_group.empty()
    blob_bullet_group.empty()
    GBexplosion_group.empty()
    blob_group.empty()
    icicle_group.empty()
    mounder_group.empty()
    mounder_bullet_group.empty()
    cubeoid_group.empty()
    snow_soldier_group.empty()
    coin_group.empty()
    sling_group.empty()
    spike_group.empty()
    upgrade_group.empty()
    enemy_group.empty()


#draw background depending on the level
def draw_bg():
    screen.fill(GREEN)
    width = im.bg1.get_width()
    if level == 0:
        screen.blit(im.bg1, (-scroll, 0))
        screen.blit(im.bg2, (width - scroll, 0))
    elif level == 1:
        for x in range(5):
            screen.blit(im.bg4, ((x*width) - scroll, 0))
        bg_snow_particle()
    elif level == 2:
        for x in range(4):
            screen.blit(im.bg4, ((x*width) - scroll, 0))
        bg_snow_particle()
    elif level == 3:
        for x in range(4):
            screen.blit(im.bg4, ((x*width) - scroll, 0))
    elif level == 4:
        for x in range(4):
            screen.blit(im.bg3, ((x*width) - scroll, 0))
    elif level == 5:
        for x in range(4):
            screen.blit(im.bg4, ((x*width) - scroll, 0))
        bg_snow_particle()

#create player
class Player():
    def __init__(self,x,y):
        self.images_right = im.images_right
        self.images_left = im.images_left
        self.right_idle = im.right_idle
        self.left_idle = im.left_idle
        self.right_jump = im.right_jump
        self.left_jump = im.left_jump
        self.right_hurt = im.right_hurt
        self.left_hurt = im.left_hurt
        self.index = 0
        self.counter = 0       
        self.image = im.images_right[0]
        self.hitbox = im.roid_hitbox
        self.rect = self.hitbox.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.hitbox.get_width()
        self.height = self.hitbox.get_height()
        self.vel_y = 0
        self.direction = 1
        self.health = 5
        self.max_health = 5
        self.hurt_cooldown = 10
        self.attack_cooldown = 30
        self.allow_jump = 0
        self.jump_height = 0
        self.timer = 0
        self.previous_health = self.health
        self.jumped = False
        self.long_jump = False
        self.allow_long = False
        self.idle = False
        self.in_air = False
        self.wall_latch = False
        self.in_water = False
        self.attack = False
        self.long_jump_reset = True
        self.platform_colliding = False
        self.gb_hurt = True
        self.dash_unlock = False
        self.latch_unlock = False
        self.god_mode = False
        self.particles = []
        self.dash_particles = []
        self.black_particles = []
        self.black_dash_trail = []
        self.black_damage_particles = []
        self.xoffset = 0
        self.yoffset = 0
        self.dust_color_list = dust_color
        self.long_jump_speed = 7
        self.health_index = 0
        self.health_timer = 0
        self.sling_dx = 0
        self.walk_cooldown = 4


    def update(self):
        dx = 0
        dy = 0
        global scroll
        global scroll_left
        global scroll_right
        global scroll_speed
        global pending_scroll_dx
        self.hurt_cooldown += 1
        if self.health > 0:
            #get key press
            key = pygame.key.get_pressed()
            black_random_appear = random.randint(0,15)
            if black_random_appear == 0:
                self.black_particles.append([[self.rect.x + 25, self.rect.y + 30 + random.randint(-20,20)], random.choice([-2-1]) * self.direction, random.choice ([-1.5,-1, 1, 1.5]), random.randint(10, 15)])
            if key[keys_list[1]] and self.wall_latch == False and self.long_jump == False and (self.in_air == True or self.attack == False) and self.hurt_cooldown > 10:
                self.timer = -10
                scroll_right = False
                scroll_left = True
                if self.attack == False:
                    self.direction = -1
            elif key[keys_list[3]] and self.wall_latch == False and self.long_jump == False and (self.in_air == True or self.attack == False) and self.hurt_cooldown > 10:
                self.timer = 10
                scroll_left = False
                scroll_right = True
                if self.attack == False:
                    self.direction = 1
            elif self.attack == True and self.in_air == False:
                self.timer = 0
            if key[keys_list[1]] or key[keys_list[3]]:
                dx += self.timer
                self.idle = False
                self.counter += 1
            else:
                self.timer = 0
                self.counter += 1
                self.idle = True
            self.timer = sorted((-8,self.timer, 8))[1]
            if key[keys_list[4]] == False:
                self.jumped = False
                self.jump_height = 0
            if key[pygame.K_LSHIFT] == False and self.long_jump_reset == True:
                self.allow_long = True
            if key[pygame.K_LSHIFT] and self.long_jump == False and self.allow_long == True and self.attack == False and self.hurt_cooldown > 10 and self.dash_unlock == True:
                self.long_jump = True
                self.long_jump_reset = False
                self.allow_long = False
                self.vel_y = 0
            elif key[keys_list[4]] and self.jumped == False and self.allow_jump <= 1 and self.attack == False and self.hurt_cooldown > 10:
                self.long_jump_speed = 7
                self.wall_latch = False
                self.jumped = True
                self.index = 0
                self.vel_y = -15
                self.allow_jump += 1
                for x in range(0,random.randint(7,9)):
                    if self.long_jump == False and self.in_air == False:
                        self.particles.append([[self.rect.x + random.randint(-10, 10) + self.width/2, self.rect.y + dy + 90], scroll_speed/6, random.randint(-2,-1), random.randint(7, 9), random.randint(0,1)])
                    elif self.in_air == False:
                        self.particles.append([[self.rect.x + random.randint(-10, 10) + self.width/2, self.rect.y + dy + 90], dx/6, random.randint(-2,-1), random.randint(7, 9), random.randint(0,1)])
                self.in_air = True
                self.long_jump = False
            #handle animation
            if self.counter > self.walk_cooldown and self.attack == False and self.hurt_cooldown > 10:
                self.counter = 0
                self.index += 1
            attacks_class.update()
            if self.attack == False and self.hurt_cooldown > 10:
                if self.index >= 6:
                    self.index = 0
                if self.idle == False:
                    direction(self, self.images_right, self.images_left, self.index)
                elif self.idle == True:
                    direction(self, self.right_idle, self.left_idle, self.index)                 
                if self.long_jump == True:
                    dx = int(self.long_jump_speed**2 * self.direction)
                    self.black_dash_trail.append([[self.rect.x - 20 * self.direction, self.rect.y + 30], random.choice([-2-1]) * self.direction, 240, 50, dx])
                    self.long_jump_speed -= 0.5
                    direction(self, self.right_jump, self.left_jump, 4)
                    self.in_air = True
                    if self.long_jump_speed == 1:
                        self.long_jump = False
                        self.long_jump_speed = 7
                elif self.wall_latch == True:
                    self.allow_jump = 1
                    self.vel_y = 0
                    direction(self, self.left_jump, self.right_jump, 7)
                elif self.in_air == True and self.long_jump == False and self.wall_latch == False or (self.vel_y > 0 and self.long_jump == False):
                    self.in_air = True
                    direction(self, self.right_jump, self.left_jump, 0)
                    if 3 <= self.vel_y <= 10:
                        direction(self, self.right_jump, self.left_jump, 3)
                    elif self.vel_y >= 10:
                        direction(self, self.right_jump, self.left_jump, 2)
            if key[keys_list[4]] == True and -5 <= self.jump_height <= 0 and self.jumped == True:
                self.jump_height -= 1
                self.vel_y = -15
            dx += self.sling_dx
            #add gravity
            if self.wall_latch == False and self.long_jump == False:
                self.vel_y += 1
                self.vel_y = sorted([self.vel_y, 20])[0]
                dy += self.vel_y

            #check for collision with enemies
            if pygame.sprite.spritecollideany(self, enemy_group) and self.hurt_cooldown >= 60:
                self.attack = False
                hitbox_group.empty()
                self.xoffset = 0
                self.yoffset = 0
                self.long_jump = False
                self.long_jump_speed = 7
                for enemy in enemy_group:
                    if self.rect.colliderect(enemy):
                        if self.rect.x + (self.width / 2) - enemy.rect.x - (enemy.width / 2) < 0:
                            self.direction = 1
                        elif self.rect.x + (self.width / 2) - enemy.rect.x - (enemy.width / 2) > 0:
                            self.direction = -1
                for num in range(20):
                    angle = np.radians(90 + self.direction*random.randint(50, 130))
                    self.black_damage_particles.append([[self.rect.x + (self.width/2) - 60 * self.direction, self.rect.y - 100*np.sin(angle) + 50], 0, angle, random.randint(10,15), random.randint(90,120)])
                collide_enemy(self)
                if self.gb_hurt == False:
                    self.black_damage_particles.clear()
            if self.hurt_cooldown <= 10:
                #dx = -10 * self.direction
                self.health_timer += 1
                if self.health_timer > 2:
                    self.health_index += 1
                    self.health_timer = 0
                direction(self, self.right_hurt, self.left_hurt, 0)
                health_animation(self)
            else:
                #draw health bar
                for num in range(1,self.max_health + 1):
                    if num <= self.health:
                        screen.blit(health_bar[0], (70 + 65*num, 40))
                    else:
                        pygame.draw.rect(transparent_surface, (100,100,100,200), (80 + 65*num, 50, 60, 60), 0, 15)

            #check for collision with moving platforms
            for platform in moving_plat_class.platform_position:
                #collision in x direction
                if platform[6].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height) and self.wall_latch == False:
                    self.platform_colliding = True
                    if platform[6].x - self.rect.x > 0:
                        dx = platform[6].left - self.rect.right
                    elif platform[6].x - self.rect.x < 0:
                        dx = platform[6].right - self.rect.left
                #collision in y direction
                elif platform[6].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height) and self.wall_latch == False:
                    if self.vel_y >= 0:
                        #check if collision occurs above (falling)
                        dy = platform[6].top - self.rect.bottom
                        self.vel_y = 0
                        grounded(self)
                        dx += platform[2]
                else:
                    self.platform_colliding = False

            for platform in cubeoid_group:
                #collision in x direction
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height) and self.wall_latch == False:
                    self.platform_colliding = True
                    if platform.rect.x - self.rect.x > 0:
                        dx = platform.rect.left - self.rect.right
                    elif platform.rect.x - self.rect.x < 0:
                        dx = platform.rect.right - self.rect.left
                #collision in y direction
                elif platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height) and self.wall_latch == False:
                    if self.vel_y >= 0:
                        #check if collision occurs above (falling)
                        dy = platform.rect.top - self.rect.bottom
                        self.vel_y = 0
                        grounded(self)
                        dx += platform.moving_speed
                else:
                    self.platform_colliding = False

            #check for collision with tiles
            for tile in world.tile_list:
                #collosion in x direction
                if tile[1].colliderect(self.rect.x + 20, self.rect.y + 50, 10, self.height) and self.wall_latch == True:
                    self.wall_latch = False
                elif tile[1].colliderect(self.rect.x + dx + self.direction, self.rect.y + 40, self.width, 20) and self.wall_latch == False and self.long_jump == True:
                    self.wall_latch = True
                    self.long_jump = False
                    self.long_jump_speed = 7
                    self.timer = 0
                    dy = 0
                    if dx > 0:
                        dx = tile[1].left - self.rect.right
                    elif dx < 0:
                        dx = tile[1].right - self.rect.left
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height) and self.wall_latch == False and tile[2] != 68:
                    # print("ASDASd")
                    if dx > 0:
                        dx = tile[1].left - self.rect.right
                    elif dx < 0:
                        dx = tile[1].right - self.rect.left
                    if self.platform_colliding == True:
                        self.health = 0
                #collision in y direction
                elif tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height) and self.wall_latch == False:
                    #check if collision occurs below (jumping)
                    if self.vel_y < 0 and tile[2] != 68:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    #check if collision occurs above (falling)
                    elif self.vel_y >= 0 and tile[1].top >= self.rect.bottom:
                        dy = tile[1].top - self.rect.bottom
                        if self.vel_y >= 12 and self.in_water == False:
                            if tile[2] == 19 or tile[2] == 20 or tile[2] == 21 or tile[2] == 41 or tile[2] == 42 or tile[2] == 47 or tile[2] == 48 or tile[2] == 68:
                                self.dust_color_list = snow_color
                                if tile[2] == 68:
                                    for i in range(0, random.randint(5,10)):
                                        snow_particle_list.append([[tile[1][0] + random.randint(0,120) - scroll_speed, tile[1][1]], random.randint(1,3), random.randint(3,6), random.randint(2,5)])
                            elif tile[2] == 0:
                                self.dust_color_list = dirt_color
                            else:
                                self.dust_color_list = dust_color
                            sfx.land.play()
                            grounded(self)
                            for x in range(0,self.vel_y + random.randint(7,9)):
                                self.particles.append([[self.rect.x + 25, self.rect.y + dy + 90], random.choice([-2,-1,1,2]), random.choice ([-0.5,-0.3,0]), random.randint(7, 9), random.randint(0,1)])
                        grounded(self)
                        self.vel_y = 0

            #update player coordinates and scrolls the map accordingly
            #scroll itself is applied at the end of the frame so every layer
            #drawn this frame uses the same scroll value
            self.rect.y += dy
            if scroll_left == True or scroll_right == True:
                pending_scroll_dx = dx
            self.sling_dx = 0
        elif self.health <= 0:
            game_over_class = go.Game_Over(screen_width, screen_height, self.rect.x, self.rect.y, self.direction)
            game_over_class.update(screen, transparent_surface)

        if self.god_mode:
            self.health = self.max_health

        #draw player onto screen
        if attacks_class.attack_index == 1:
            hitbox_group.update()
        
        screen.blit(self.image, (self.rect.x - self.xoffset - 5,self.rect.y - self.yoffset))
        dust_particle(self)
        #pygame.draw.rect(screen, RED, self.rect, 2)
        if grid_allow == 1:
            pass
            #pygame.draw.rect(screen, RED, (self.rect.x + dx + self.direction, self.rect.y + 40, self.width, 20), 2)
            #pygame.draw.rect(screen, RED, (self.rect.x + dx, self.rect.y + 50,self.width, 10), 2)


#detects enemy collision
def collide_enemy(mob):
    mob.previous_health = mob.health
    mob.health_index = 0
    mob.health_timer = 0
    if pygame.sprite.spritecollideany(mob, blob_green_group) and mob.gb_hurt == True:
        mob.health -= 1
    elif pygame.sprite.spritecollideany(mob, blob_group) or pygame.sprite.spritecollideany(mob, mounder_group) or pygame.sprite.spritecollide(mob, blob_bullet_group, True) or pygame.sprite.spritecollide(mob, mounder_bullet_group, True):
        mob.health -= 1
    elif pygame.sprite.spritecollideany(mob, icicle_group) or pygame.sprite.spritecollideany(mob, snow_soldier_group):
        mob.health -= 1
    elif pygame.sprite.spritecollide(mob, bat_group, True):
        mob.health -= 2
    elif pygame.sprite.spritecollideany(mob, GBexplosion_group):
        mob.health -= 3
    elif pygame.sprite.spritecollideany(mob, spike_group):
        mob.health -= 1
    if mob.previous_health > mob.health:
        mob.hurt_cooldown = 1
        mob.random_direction_x = random.choice([-10, 10])
        mob.random_direction_y = random.choice([-10, 10])

        
#animates heatlh bar when taking damage
def health_animation(mob):
    for num in range(1, mob.max_health + 1):
        if num > mob.previous_health:
            pygame.draw.rect(transparent_surface, (100,100,100,200), (80 + 65*num, 50, 60, 60), 0, 15)
    for num in range(1, mob.previous_health + 1):
        if num <= mob.health:
            screen.blit(health_bar[0], (70 + 65*num + mob.random_direction_x*np.sin(2*mob.hurt_cooldown*np.pi/5), 40 + mob.random_direction_y*np.sin(2*mob.hurt_cooldown*np.pi/5)))
        else:
            screen.blit(health_bar[mob.health_index], (70 + 65*num, 40))


#check if bg tiles exists
def bg_tiles():
    liquid = motion()
    bg_torch = torch()
    return liquid, bg_torch

#mob active only on screen
MOB_ACTIVE_MARGIN = 250
RECT_ACTIVE_MARGIN = 200
def mob_is_active(mob):
    return (
        mob.rect.right >= -MOB_ACTIVE_MARGIN
        and mob.rect.left <= screen_width + MOB_ACTIVE_MARGIN
        and mob.rect.bottom >= -MOB_ACTIVE_MARGIN
        and mob.rect.top <= screen_height + MOB_ACTIVE_MARGIN
    )
def rect_is_active(rect):
    return (
        rect.right >= -RECT_ACTIVE_MARGIN
        and rect.left <= screen_width + RECT_ACTIVE_MARGIN
        and rect.bottom >= -RECT_ACTIVE_MARGIN
        and rect.top <= screen_height + RECT_ACTIVE_MARGIN
    )

#store tiles in a list
img_list = []
for x in range(tile_types):
    img = pygame.image.load(f'{im.ASSETS_DIR}/{x}.png').convert_alpha()
    if x != 68 and x != 73 and x != 74:
        img = pygame.transform.scale(img, (tile_size, tile_size))
    elif x == 68:
        img = pygame.transform.scale(img, (120, 80))
    elif x == 73:
        img = pygame.transform.scale(img, (160, 160))
    elif x == 74:
        img = pygame.transform.scale(img, (150, 100))
    img_list.append(img)


#creates world
class World():
    def __init__(self, data):
        self.tile_list = []
        self.torch_position = []
        self.snow_particle_position = []
        self.blocker_list = []
        self.grass_position = []
        self.platform_position = []
        self.shop_position = None
        self.ice_boss_class = ib.Ice_Boss(0,0, screen)
        row_count = 0
        for y,row in enumerate(world_data):
            col_count = 0
            for x,tile in enumerate(row):
                if tile == 13:
                    bat = Bat(col_count * tile_size - scroll, row_count * tile_size)
                    enemy_group.add(bat)
                    bat_group.add(bat)
                elif tile == 8:
                    sm = SnowMounder(col_count * tile_size - scroll, row_count * tile_size)
                    enemy_group.add(sm)
                    mounder_group.add(sm)
                elif tile == 15:
                    blob = Blob(col_count * tile_size - scroll, row_count * tile_size)
                    enemy_group.add(blob)
                    blob_group.add(blob)
                elif tile == 16:
                    gb = GB(col_count * tile_size - scroll, row_count * tile_size - 30)
                    enemy_group.add(gb)
                    blob_green_group.add(gb)
                elif tile == 18:
                    icicle = Ice(col_count * tile_size - scroll, row_count * tile_size)
                    enemy_group.add(icicle)
                    icicle_group.add(icicle)
                elif tile == 25:
                    self.torch_position.append([col_count * tile_size, row_count * tile_size])
                elif tile == 28 or tile == 36 or tile == 37 or tile == 38:
                    self.snow_particle_position.append([col_count * tile_size - scroll, row_count * tile_size])
                elif tile == SHOP_TILE and self.shop_position is None:
                    self.shop_position = (col_count * tile_size, row_count * tile_size)
                elif tile == 52:
                    cube = Cubeoid(col_count * tile_size - scroll, row_count * tile_size - 50)
                    cubeoid_group.add(cube)
                elif tile == 60:
                    ss = Snow_Soldier(col_count * tile_size - scroll, row_count * tile_size - 35)
                    enemy_group.add(ss)
                    snow_soldier_group.add(ss)
                elif tile == 61:
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size - scroll
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect, tile)
                    self.blocker_list.append(tile)
                elif tile == 62:
                    self.ice_boss_class = ib.Ice_Boss(col_count * tile_size - scroll, row_count * tile_size, screen)
                    for num in range(-2,3):
                        if num != 0:
                            arms = ib.Ice_Boss_Arm(col_count * tile_size - scroll + 200 * num, row_count * tile_size + 50*abs(num) - 100, screen, abs(num) * 0.5)
                            ice_arms_group.add(arms)
                elif tile == 64:
                    sling = Sling(col_count * tile_size - scroll, row_count * tile_size)
                    sling_group.add(sling)
                elif tile == 66:
                    i_spike = Ispike(col_count * tile_size - scroll, row_count * tile_size)
                    spike_group.add(i_spike)
                    enemy_group.add(i_spike)
                elif tile == 67:
                    up = upgrade_unlock(col_count * tile_size - scroll, row_count * tile_size)
                    upgrade_group.add(up)
                elif tile == 73:
                    self.platform_position.append([col_count * tile_size, row_count * tile_size, 0, 1, 0, img_list[tile], img_list[tile].get_rect(), tile, 0])
                elif tile == 74:
                    self.platform_position.append([col_count * tile_size, row_count * tile_size, 0, 1, 0, img_list[tile], img_list[tile].get_rect(), tile, 0])
                elif tile == 75:
                    self.grass_position.append([col_count * tile_size, row_count * tile_size])
                col_count += 1
            row_count += 1
        if self.shop_position is None and level == 0:
            self.shop_position = (1500, 700)
        row_count = 0

    def refresh_grass_positions(self):
        self.grass_position = [
            [x * tile_size, y * tile_size]
            for y, row in enumerate(world_data)
            for x, tile in enumerate(row)
            if tile == 75
        ]

    def refresh_torch_positions(self):
        self.torch_position = [
            [x * tile_size, y * tile_size]
            for y, row in enumerate(world_data)
            for x, tile in enumerate(row)
            if tile == 25
        ]

    def draw(self):
        self.tile_list = []
        self.blocker_list = []
        world_data_copy = []

        collision_buffer_tiles = 7
        first_col = max(0, floor(scroll / tile_size) - collision_buffer_tiles)
        last_col = min(
            len(world_data[0]),
            ceil((scroll + screen_width) / tile_size) + collision_buffer_tiles
        )

        world_data_copy = [row[first_col:last_col] for row in world_data]

        # world_data_copy = [i[int(scroll/50):int((scroll/50) + 47)] for i in world_data]
        row_count = 0
        for y, row in enumerate(world_data_copy):
            # col_count = int(scroll/50)
            col_count = first_col
            for x, tile in enumerate(row):
                if tile == SHOP_TILE:
                    if melee_allow == 0 and grid_allow == 1:
                        screen.blit(img_list[tile], (col_count * tile_size - scroll, row_count * tile_size))
                elif tile >= 0 and tile != 1 and tile != 2 and tile != 3 and tile != 5 and tile != 7 and tile != 8 and tile != 9 and tile != 11 and tile != 13 and tile != 15 and tile != 16 and tile != 17 and tile != 18 and tile != 22 and tile != 25 and tile != 40 and tile != 52 and tile != 54 and tile != 60 and tile != 62 and tile != 64 and tile != 66 and tile != 67 and tile != 69 and tile != 71 and tile != 72 and tile != 73 and tile != 74 and tile != 75:
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size - scroll
                    img_rect.y = row_count * tile_size
                    if tile != 12 and tile != 61 and tile != 68:
                        screen.blit(img_list[tile], (img_rect.x, img_rect.y))
                        tile = (img, img_rect, tile)
                        self.tile_list.append(tile)
                    elif tile == 61:
                        if melee_allow == 0:
                            screen.blit(img_list[tile], (img_rect.x, img_rect.y))
                        tile = (img, img_rect, tile)
                        self.blocker_list.append(tile)
                    elif tile == 68:
                        img_rect = img_list[tile].get_rect()
                        img_rect.x = col_count * tile_size - scroll + 30
                        img_rect.y = row_count * tile_size  
                        screen.blit(img_list[tile], (img_rect.x, img_rect.y))
                        tile = (img, img_rect, tile)
                        self.tile_list.append(tile)
                col_count += 1
            row_count += 1
        row_count = 0
        for y, row in enumerate(bg_data):
            col_count = 0
            for x, tile in enumerate(row):
                if tile >= 0:
                    screen.blit(img_list[tile],  (x * tile_size - scroll, y * tile_size))
                col_count += 1
            row_count += 1


#function to draw front surface
def draw_front():
    row_count = 0
    for y, row in enumerate(front_data):
        col_count = 0
        for x, tile in enumerate(row):
            if tile == 1 or tile == 2 or tile == 3 or tile == 5:
                screen.blit(img_list[tile],  (x * tile_size - scroll, y * tile_size))
            col_count += 1
        row_count += 1


#function for outputting text onto the screen
font = pygame.font.Font(im.FONT_PATH, 50)
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


#draws the white lines
def draw_grid():
    for c in range(128):
        pygame.draw.line(screen, WHITE, (c * tile_size - scroll, 0), (c * tile_size - scroll, screen_height))
    for c in range(21):
        pygame.draw.line(screen, WHITE, (0, c * tile_size), (screen_width, c * tile_size))


#create image for mob based on the direction they are facing
def direction(mob, right_img, left_img, index):
    if mob.direction == 1:
        mob.image = right_img[index]
    elif mob.direction == -1:
        mob.image = left_img[index]


#define when player is grounded
def grounded(mob):
    mob.wall_latch = False
    mob.allow_jump = 0
    mob.in_water = False
    mob.in_air = False
    mob.long_jump_reset = True


#walking and landing particle effects
def dust_particle(mob):
    for particle in mob.black_dash_trail:
        particle[2] -= 10
        pygame.draw.rect(transparent_surface, (0,0,0,particle[2]), [int(particle[0][0]), int(particle[0][1]), 50, 50])
        particle = particle_scrolling(particle)
        if particle[2] <= 1:
            mob.black_dash_trail.remove(particle)
    for particle in mob.black_particles:
        particle[0][0] += particle[1]/3
        particle[0][1] -= particle[2]
        particle[3] -= 0.5
        pygame.draw.rect(transparent_surface, BLACK, [int(particle[0][0]), int(particle[0][1]), 5, 5])
        particle = particle_scrolling(particle)
        if particle[3] <= 1:
            mob.black_particles.remove(particle)
    for particle in mob.particles:
        particle[0][0] += particle[3]*particle[1]/2
        particle[0][1] += particle[3]*particle[2]/5
        particle[3] -= 0.5
        pygame.draw.circle(screen, mob.dust_color_list[particle[4]], [int(particle[0][0]), int(particle[0][1])], particle[3])
        particle = particle_scrolling(particle)
        if particle[3] <= 1:
            mob.particles.remove(particle)
    for particle in mob.black_damage_particles:
        particle[1] += 6
        particle[0][0] += (particle[4] - particle[1])*np.cos(particle[2])/5
        particle[0][1] -= (particle[4] - particle[1])*np.sin(particle[2])/5
        points = [[particle[0][0] - (particle[4] - particle[1])*np.cos(np.pi/2 - particle[2])/particle[3], particle[0][1] - (particle[4] - particle[1])*np.sin(np.pi/2 - particle[2])/particle[3]],
                  [particle[0][0] + (particle[4] - particle[1])*np.cos(particle[2])/particle[3], particle[0][1] - (particle[4] - particle[1])*np.sin(particle[2])/particle[3]],
                  [particle[0][0] + (particle[4] - particle[1])*np.cos(np.pi/2 - particle[2])/particle[3], particle[0][1] + (particle[4] - particle[1])*np.sin(np.pi/2 - particle[2])/particle[3]],
                  [particle[0][0] - (particle[4] - particle[1])*np.cos(particle[2]), particle[0][1] + (particle[4] - particle[1])*np.sin(particle[2])]]
        pygame.draw.polygon(screen, BLACK, points)
        particle = particle_scrolling(particle)
        if particle[1] > particle[4]:
            mob.black_damage_particles.remove(particle)


#draw particles for sling
def sling_particle(mob):
    for particle in mob.activate_particle_list:
        particle[3] -= 1
        particle[0][0] += particle[1]*np.cos(particle[2])
        particle[0][1] -= particle[1]*np.sin(particle[2])
        particle = particle_scrolling(particle)
        pygame.draw.circle(transparent_surface, (147,207,240, 120), (particle[0][0], particle[0][1]), particle[4])
        if particle[3] <= 0:
            mob.activate_particle_list.remove(particle)


#draw particles for health potion
def healing_particles(particle_allow):
    if particle_allow == 1:
        particle_allow = 0
        random_amount = random.randint(5,8)
        for x in range(0,random_amount):
            randx = random.randint(0,45)
            randy = random.randint(0,90)
            particle_list.append([[player.rect.x + randx, player.rect.y + randy], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 6), random.randint(-250,250)])
    for particle in particle_list:
        particle[0][1] += -1
        particle[2] -= 0.1
        screen.blit(im.particle_img, (400 + particle[3], int(particle[0][1]) - 810))
        screen.blit(im.particle_img, ([int(particle[0][0]), int(particle[0][1])]))
        if particle[2] <= 1:
            particle_list.remove(particle)
    return particle_allow


#draw snow particles for the background
def bg_snow_particle():
    for tile in world.snow_particle_position:
        randx = random.randint(0,45)
        random_appear = random.randint(0,20)
        if random_appear == 0:
            snow_particle_list.append([[tile[0] + randx - scroll, tile[1] + 50], random.randint(1, 3), random.randint(1,3), random.randint(1,3)])
    for particle in snow_particle_list:
        particle[0][1] += particle[3]
        particle[1] -= 0.02*particle[2]
        if particle[1] <= 1:
            snow_particle_list.remove(particle)
        particle = particle_scrolling(particle)
        pygame.draw.circle(screen, WHITE_BG, [int(particle[0][0]), int(particle[0][1])], particle[1])


#draw particles for shop and upgrade
def upgrade_particle(mob):
    for particle in mob.shard_particles:
        particle[3] -= 1
        particle[0][0] += particle[1]*np.cos(particle[2])
        particle[0][1] -= particle[1]*np.sin(particle[2])
        pygame.draw.rect(screen, WHITE, (particle[0][0], particle[0][1], 2, 2))
        particle = particle_scrolling(particle)
        if particle[3] <= 1:
            mob.shard_particles.remove(particle)


#determine each mob's money drop chance
def coin_chance(gold, silver, bronze, random_drop,random_chance,rx,ry):
    for x in range(0, random_drop):
        random_coin = random.randint(0,random_chance)
        if random_coin == gold:
            coins = Coin(rx + tile_size/2, ry + tile_size/2, 100)
        elif random_coin <= silver:
            coins = Coin(rx + tile_size/2, ry + tile_size/2, 50)
        elif random_coin <= bronze:
            coins = Coin(rx + tile_size/2, ry + tile_size/2, 10)
        coin_group.add(coins)


#class for when enemies take damage and show health bar
class damage_health():
    def __init__(self, length, max_health, bullet_dmg, melee_dmg, GBexplosion_dmg):
        self.slash_img = np.copy(im.images_slash)
        self.rect = self.slash_img[0].get_rect()
        self.bullet_dmg = bullet_dmg
        self.melee_dmg = melee_dmg
        self.GBexplosion_dmg = GBexplosion_dmg
        self.length = length
        self.max_health = max_health
        self.health_timer = 0
        self.direction_list = [-5, 5]
        self.random_direction_x = 0
        self.random_direction_y = 0
        self.store_health = self.max_health
        self.effect_index = 0
        self.dmg_particle_list = []

    def update(self, mob, rx, ry, x_offset, y_offset, health, hurt_cooldown):
        if (pygame.sprite.spritecollideany(mob, bullet_group) or pygame.sprite.spritecollideany(mob, hitbox_group) or pygame.sprite.spritecollideany(mob, GBexplosion_group)) and hurt_cooldown >= 15 and mob.dmg_allow == 0:
            self.random_direction_x = random.choice(self.direction_list)
            self.random_direction_y = random.choice(self.direction_list)
            x_neg = -10
            x_pos = 10
            y_neg = 0
            y_pos = 10
            if pygame.sprite.spritecollide(mob, bullet_group, True) and hurt_cooldown >= 5 and self.bullet_dmg > 0:
                mob.dmg_allow = 1
                mob.health -= self.bullet_dmg
                self.store_health = health
                mob.hurt_cooldown = 0
            elif pygame.sprite.spritecollideany(mob, hitbox_group) and hurt_cooldown >= 15 and self.melee_dmg != 0:
                sfx.enemy_hurt_list[random.randint(0,1)].play()
                for num in range(0,2):
                    if rx - player.rect.x == 0:
                        self.slash_img[num] = pygame.transform.rotate(self.slash_img[num], 90)
                    else:
                        self.slash_img[num] = pygame.transform.rotate(self.slash_img[num], (180 / np.pi) * np.arctan((player.rect.y - ry)/(rx - player.rect.x)))
                self.rect = self.slash_img[0].get_rect()
                mob.dmg_allow = 1
                mob.health -= self.melee_dmg
                self.store_health = health
                mob.hurt_cooldown = 0
            elif pygame.sprite.spritecollideany(mob, GBexplosion_group) and hurt_cooldown >= 50 and self.GBexplosion_dmg != 0:
                mob.dmg_allow = 1
                mob.health -= self.GBexplosion_dmg
                self.store_health = health
                mob.hurt_cooldown = 0
            if (rx - player.rect.x + 25) != 0 and mob.dmg_allow == 1:
                if -np.pi/4 <= np.arctan((player.rect.y - ry + 45)/(rx-player.rect.x + 25)) <= np.pi/4 and rx - player.rect.x > 0:
                    x_neg = 5
                    x_pos = 15
                elif -np.pi/4 <= np.arctan((player.rect.y - ry + 45)/(rx-player.rect.x + 25)) <= np.pi/4 and rx - player.rect.x <= 0:
                    x_neg = -15
                    x_pos = -5
                elif player.rect.y - ry > 0:
                    y_neg = 5
                    y_pos = 15
                elif player.rect.y - ry <= 0:
                    y_neg = -15
                    y_pos = -5
            if mob.dmg_allow == 1:
                mob.dmg_allow = 0
                random_amount = random.randint(4,6)
                for x in range(0,random_amount):
                    randx = random.randint(0,round(mob.width/3))
                    randy = random.randint(0,round(mob.height/3))
                    self.dmg_particle_list.append([[rx + mob.width/3 +randx, ry + mob.height/3 +randy], random.randint(13, 15), random.randint(x_neg,x_pos), random.randint(y_neg,y_pos), 1])
        for particle in self.dmg_particle_list:
            particle[4] += 1
            particle[0][0] += particle[2]
            particle[0][1] -= particle[3] - particle[4]**2/80
            particle[1] -= 0.3
            particle = particle_scrolling(particle)
            if particle[1] <= 1:
                self.dmg_particle_list.remove(particle)
            pygame.draw.circle(screen, RED, [int(particle[0][0]), int(particle[0][1])], particle[1])

        #draw health bar
        if mob.hurt_cooldown < 6:
            transparent_surface.blit(self.slash_img[self.effect_index], (rx - self.rect.center[0] + (mob.width / 2), ry - self.rect.center[1] + (mob.height / 2)))
            if mob.hurt_cooldown > 2:
                self.effect_index = 1
        elif mob.hurt_cooldown == 6:
            self.effect_index = 0
            self.slash_img = np.copy(im.images_slash)
        if mob.hurt_cooldown < 10 and mob.health > 0 and mob.health != self.max_health:
            pygame.draw.rect(screen, RED, (rx + x_offset + self.random_direction_x*np.sin(2*hurt_cooldown*np.pi/5), ry - y_offset + self.random_direction_y*np.sin(2*hurt_cooldown*np.pi/5), self.length, 7), 0, 5)
            pygame.draw.rect(screen, WHITE, (rx + x_offset + self.random_direction_x*np.sin(2*hurt_cooldown*np.pi/5), ry - y_offset + self.random_direction_y*np.sin(2*hurt_cooldown*np.pi/5), (self.length / self.max_health) * self.store_health, 7), 0, 5)
            pygame.draw.rect(screen, GREEN, (rx + x_offset + self.random_direction_x*np.sin(2*hurt_cooldown*np.pi/5), ry - y_offset + self.random_direction_y*np.sin(2*hurt_cooldown*np.pi/5), (self.length / self.max_health) * mob.health, 7), 0, 5)
            self.health_timer = 1
        elif mob.health > 0 and abs(mob.rect.x - player.rect.x) <= 500 or self.health_timer > 0:
            pygame.draw.rect(screen, RED, (rx + x_offset, ry - y_offset, self.length, 7), 0, 5)
            if self.health_timer > 0:
                self.health_timer += 1
                pygame.draw.rect(screen, WHITE, (rx + x_offset, ry - y_offset, (self.length / self.max_health) * self.store_health, 7), 0, 5)
                pygame.draw.rect(screen, GREEN, (rx + x_offset, ry - y_offset, (self.length / self.max_health) * health, 7), 0, 5)
                if self.health_timer > 15:
                    self.health_timer = 0
                elif self.health_timer > 5:
                    self.store_health = (health + self.store_health) / 2
            pygame.draw.rect(screen, GREEN, (rx + x_offset, ry - y_offset, (self.length / self.max_health) * mob.health, 7), 0, 5)


#physics for liquid
class motion():
    def __init__(self):
        self.fluid_collide = -1
        self.fluid_move = 0
        self.fluid = 0
        self.amplitude = 0
        self.fluid_length = 0
        self.rectangle = []
        self.height = []
        self.length = [0]
        row_count = 0
        previous_column = 0
        for y,row in enumerate(world_data):
            col_count = 0
            for x,tile in enumerate(row):
                if tile == 17:
                    if col_count - previous_column >= 2:
                        self.fluid += 1
                        self.length.append(0)
                    for i in range(5):
                        self.fluid_length += 1
                        self.length[self.fluid] = self.fluid_length
                        add = [col_count * tile_size + 10*i - scroll, row_count * tile_size, 1000, self.fluid]
                        self.height.append(row_count * tile_size)
                        self.rectangle.append(add)
                        previous_column = col_count
                col_count += 1
            row_count += 1
    
    def update(self, potion):
        for move in range(len(self.rectangle)):
            self.rectangle[move][1] =  self.height[move] + -5*np.exp(self.rectangle[move][2] / -30) * np.cos(np.pi * self.rectangle[move][2] / 10)
            self.rectangle[move][2] += 1
            fluid = pygame.Rect(self.rectangle[move][0], self.rectangle[move][1], 10,3)
            key = pygame.key.get_pressed()
            if fluid.colliderect(player) and player.vel_y != 0:
                self.amplitude = abs(player.vel_y)
                player.in_water = True
                self.fluid = self.rectangle[move][3]
                self.fluid_collide = move
                self.fluid_move = 0
            elif key[keys_list[5]] and fluid.colliderect(player):
                player.health = player.max_health
                player.previous_health = player.health
                potion_class.uses_left = potion_class.potion_max
                potion_class.potion = 0
                potion = 0
            if scroll_left == True or scroll_right == True:
                self.rectangle[move][0] -= scroll_speed
            pygame.draw.rect(transparent_surface, (144,201,120,180), (self.rectangle[move][0], self.rectangle[move][1] + 3, 10, 47 - self.rectangle[move][1] + self.height[move]))
            pygame.draw.rect(screen, DARK_GREEN, (self.rectangle[move][0], 40 + self.height[move], 10, 10))
        if self.fluid_collide != -1:
            move_left = self.fluid_collide - self.fluid_move
            move_right = self.fluid_collide + self.fluid_move
            move_amount = (move_left - self.fluid_collide)**2 / 30
            if move_left >= self.length[self.fluid - 1]:
                self.rectangle[move_left][2] = move_amount - self.amplitude
            if move_right <= self.length[self.fluid] - 1:
                self.rectangle[move_right][2] = move_amount - self.amplitude
            self.fluid_move += 1
        return potion


#particles for when mobs die
class death_particle:
    death_particle_list = []
    def __init__(self, death_x, death_y, width, height):
        death_particle_direction_x = [-20,-15,-10,-5,0,5,10,15,20]
        death_particle_direction_y = [-20,-15,-10,-5,0,5,10,15,20]
        if death_x > 0:
            for num in range(8):
                direction_x = random.choice(death_particle_direction_x)
                direction_y = random.choice(death_particle_direction_y)
                death_particle_direction_x.remove(direction_x)
                death_particle_direction_y.remove(direction_y)
                death_particle_list.append([[death_x + (width/2) + direction_x, death_y + (height/2) + direction_y], random.randint(-5,5), random.randint(-5,5), 30, random.randint(0,1), 1])

    #animation for death particles and mana particles
    def update(self):
        for particle in death_particle_list:
            particle[5] += 0.2
            particle[0][0] += 2*particle[1]/particle[5]
            particle[0][1] += particle[2] - particle[5]
            particle[3] -= 1
            particle = particle_scrolling(particle)
            if particle[3] <= 1:
                death_particle_list.remove(particle)
            pygame.draw.circle(screen, death_particle_color[particle[4]], [int(particle[0][0]), int(particle[0][1])], particle[3])


#moves the mobs according to the screen
def scrolling(mob):
    if scroll_left == True or scroll_right == True:
        mob.rect.x -= scroll_speed


#detects if player goes up or down a level
def exit(index, current_lvl):
    if player.rect.y < 0 and current_lvl == 1:
        player.rect.y = 800
        index = 2
    elif player.rect.y < 0 and current_lvl == 3:
        index = 1
    elif player.rect.y > 1020 and current_lvl == 1:
        player.rect.y = 100
        index = 3
    elif player.rect.y > 1020 and current_lvl == 2:
        player.rect.y = 100
        index = 1
    return index


#collision for moving mobs
def moving_collision(mob, collision_tiles):
    for tile in collision_tiles:
        if tile[1].colliderect(mob.rect.x + mob.dx, mob.rect.y, mob.width, mob.height):
            if mob.hurt_cooldown > 10:
                mob.direction *= -1
            if mob.dx > 0:
                mob.dx = tile[1].left - mob.rect.right
            elif mob.dx < 0:
                mob.dx = tile[1].right - mob.rect.left

#turnaround when moving mobs are at the edge of cliff
# def edge_turnaround(mob, ):


#moves the particles according to the screen
def particle_scrolling(particle):
    if scroll_left == True or scroll_right == True:
        particle[0][0] -= scroll_speed
    return particle


for i in range(len(img_list)):
    image = img_list[i]
    preview_scale = min(1, 50 / image.get_width(), 50 / image.get_height())
    tile_button = button.Button(screen_width - (75 * button_col) - 100, 75 * button_row + 50, img_list[i], preview_scale)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0
    if button_row > 13:
        button_row = 0



#class to choose the attack animation
class attacks():
    def __init__(self):
        self.in_air = player.in_air
        self.attack_counter = -3
        self.attack_index = 0
        self.right_attack = im.right_attack
        self.left_attack = im.left_attack
        self.right_forward_air = im.right_forward_air
        self.left_forward_air = im.left_forward_air
        self.up_attack_right = im.up_attack_right
        self.up_attack_left = im.up_attack_left
        self.up_air_right = im.up_air_right
        self.up_air_left = im.up_air_left

        self.hitbox_direction = 0
        self.random_attack = random.choice([1,3])


    def get_hitbox_direction(self):
        key = pygame.key.get_pressed()
        if key[K_w]:
            self.hitbox_direction = 3
            if player.direction == 1:
                player.xoffset = 55
                player.yoffset = 102
            elif player.direction == -1:
                player.xoffset = 70
                player.yoffset = 102
        elif key[K_d] or player.direction == 1:
            player.direction = 1
            player.xoffset = 95
            player.yoffset = 83
            self.hitbox_direction = 1
        elif key[K_a] or player.direction == -1:
            player.direction = -1
            player.xoffset = 130
            player.yoffset = 83
            self.hitbox_direction = 2
        if player.in_air == True:
            player.yoffset = 90
            if self.hitbox_direction == 1:
                self.hitbox_direction = 5
                player.xoffset = 120
            elif self.hitbox_direction == 2:
                self.hitbox_direction = 6
                player.xoffset = 110
            elif self.hitbox_direction == 3:
                self.hitbox_direction = 7
                player.yoffset = 110
        return self.hitbox_direction
    
    #update attack animations
    def update(self):
        if player.attack == True:
            self.in_air = player.in_air
            self.attack_counter += 1
            if self.in_air == False:
                if self.attack_counter >= 4 and self.attack_index == 0:
                    self.attack_index += 1
                    self.attack_counter = 0
                if self.hitbox_direction == 1 or self.hitbox_direction == 2:
                    if self.attack_index == 1:
                        direction(player, self.right_attack, self.left_attack, self.random_attack)
                    else:
                        direction(player, self.right_attack, self.left_attack, self.attack_index)
                elif self.hitbox_direction == 3:
                    direction(player, self.up_attack_right, self.up_attack_left, self.attack_index)
                if self.attack_counter >= 5 and self.attack_index == 1:
                    self.attack_index += 1
                    self.attack_counter = 0
                elif self.attack_counter >= 3 and self.attack_index == 2:
                    player.attack = False
                    self.attack_index = 0
                    player.xoffset = 0
                    player.yoffset = 0
            elif self.in_air == True:
                if self.attack_counter >= 4 and self.attack_index == 0:
                    self.attack_index += 1
                    self.attack_counter = 0
                if self.hitbox_direction == 5 or self.hitbox_direction == 6:
                    if self.attack_index == 1:
                        direction(player, self.right_forward_air, self.left_forward_air, self.random_attack)
                    else:
                        direction(player, self.right_forward_air, self.left_forward_air, self.attack_index)
                elif self.hitbox_direction == 7:
                    direction(player, self.up_air_right, self.up_air_left, self.attack_index)
                if self.attack_counter >= 4 and self.attack_index == 1:
                    self.attack_index += 1
                    self.attack_counter = 0
                elif (self.attack_counter >= 2 and self.attack_index == 2) or player.in_air == False:
                    hitbox_group.empty()
                    player.attack = False
                    self.attack_index = 0
                    player.xoffset = 0
                    player.yoffset = 0


#class for animating coins
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        self.image_coins = im.image_coins
        self.random_coin = type
        pygame.sprite.Sprite.__init__(self)   
        self.image = self.image_coins[int(self.random_coin/50)]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rand_speed = random.randint(10,20)
        self.rand_angle = random.randint(0,360) * np.pi / 180
        self.activate = 0
        self.timer = random.randint(0, 360)
        self.realy = self.rect.y
        self.buffer = 0
    
    def update(self):
        scrolling(self)
        #coin movement
        self.buffer += 1
        if self.activate == 0:
            self.rand_speed -= 1
            self.rect.x += self.rand_speed * np.cos(self.rand_angle)
            self.rect.y += self.rand_speed * np.sin(self.rand_angle)
            if self.rand_speed == 0:
                self.activate = 1
                self.realy = self.rect.y
        elif self.activate == 1:
            self.realy -= np.sin(self.timer * np.pi / 180)
            self.rect.y = self.realy
            self.timer += 4
        if self.activate == 2:
            self.rect.x -= 19*(self.rect.x - player.rect.x)/np.sqrt((self.rect.x - player.rect.x)**2 + (player.rect.y - self.rect.y)**2)
            self.rect.y += 19*(player.rect.y - self.rect.y + 20)/np.sqrt((self.rect.x - player.rect.x)**2 + (player.rect.y - self.rect.y)**2)
        elif abs(self.rect.x - player.rect.x) <= 200 and abs(self.rect.y - player.rect.y) <= 200 and self.buffer >= 50:
            self.activate = 2
        if self.rect.colliderect(player):
            coin_animate_class.coin_delay += self.random_coin
            self.kill()
        screen.blit(self.image, (self.rect.x, self.rect.y))


#class for coin animation and keeps track of coins owned
class Coin_Animate():
    def __init__(self):
        self.coin_prev = 0
        self.coin_delay = 0
        self.coin_timer = 0
        self.coin_own = 0
        self.decay = False
        self.decay_timer = 0
        self.decay_y = 0
    
    #draw text and update particles for coin
    def update(self):
        if self.coin_prev != self.coin_delay:
            self.coin_prev = self.coin_delay
            self.coin_timer = 0
        if self.decay == False and self.coin_timer >= 100:
            self.coin_timer = 0
            self.coin_own += self.coin_delay
            self.coin_delay = 0
            self.decay = True
        elif self.decay == True:
            self.decay_timer += 3
            self.decay_y += -10 + self.decay_timer
            if self.decay_y >= 10:
                self.decay_timer = 0
                self.decay_y = 0
                self.decay = False
        if self.coin_prev > 0:
            self.coin_timer += 1
            draw_text(f'+{self.coin_prev}', font, WHITE, 100, 180)
        draw_text(f'{self.coin_own}', font, WHITE, 100, 210 + self.decay_y)
        screen.blit(im.money_icon, (50, 200))


#class for icicle
class Ice(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.images_icicle = im.images_icicle
        self.images_break = im.images_break
        self.hitbox = im.icicle_hitbox
        self.index = 0
        pygame.sprite.Sprite.__init__(self)
        self.image = self.images_icicle[self.index]
        self.rect = self.hitbox.get_rect()
        self.width = self.hitbox.get_width()
        self.height = self.hitbox.get_height()
        self.rect.x = x
        self.rect.y = y
        self.x_original = self.rect.x
        self.move_counter = 0
        self.animation_cooldown = 10
        self.activate = 0
        self.time = 0

    #update the icicle's postition and animation    
    def update(self):
        scrolling(self)
        if abs(player.rect.x - self.rect.x - (self.width / 2)) < 1200:
            self.move_counter += 1
            if abs(self.rect.x - player.rect.x) <= 100 and self.activate != 2:
                self.activate = 1
            elif self.move_counter > self.animation_cooldown and self.activate != 2:
                self.move_counter = 0
                self.index += 1
                if self.index >= len(self.images_icicle):
                    self.index = 0
                self.image = self.images_icicle[self.index]
            for tile in world.tile_list:
                #check if icicle has collided with tile
                if tile[1].colliderect(self.rect) and self.activate == 1:
                    self.activate = 2
                    self.y_break = self.rect.y
                    self.rect = self.images_break[0].get_rect()
                    self.width = self.images_break[0].get_width()
                    self.height = self.images_break[0].get_height()
                    self.index = 0
            if self.activate == 1 or self.activate == 0:
                screen.blit(self.image, (self.rect.x - 23, self.rect.y))
            if self.activate == 1:
                self.time += 1
                self.rect.y += (self.time)**2/100
            elif self.activate == 2:
                self.rect.x = self.x_original - scroll - 25
                self.rect.y = self.y_break - 30
                if self.index < len(self.images_break) - 1:
                    self.image = self.images_break[self.index]
                    self.index += 1
                else:
                    self.kill()
                screen.blit(self.image, (self.rect.x, self.rect.y - 10))


#class for ice spikes
class Ispike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = im.ice_spike
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        scrolling(self)
        screen.blit(self.image, (self.rect.x, self.rect.y))


#class for blob
class Blob(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.images_left = im.images_blob_left
        self.images_right = im.images_blob_right
        self.hitbox = im.blob_hitbox
        self.damage_health_class = damage_health(100,20,1,8,15)
        self.image = self.images_right[self.index]
        self.rect = self.hitbox.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.hitbox.get_width()
        self.height = self.hitbox.get_height()
        self.move_counter = 0
        self.animation_cooldown = 10
        self.direction = -1
        self.health = 20
        self.random_drop = random.randint(10,15)
        self.hurt_cooldown = 15
        self.dmg_allow = 0
        
    #updates the blob's position, direction, and animation
    def update(self):
        scrolling(self)
        if abs(player.rect.x - self.rect.x - (self.width / 2)) < 1100:
            self.move_counter += 1
            self.hurt_cooldown += 1
            self.damage_health_class.update(self,self.rect.x,self.rect.y, -25, 20, self.health,self.hurt_cooldown)
            if self.health <= 0:
                death_particle(self.rect.x,self.rect.y, self.width, self.height)
                coin_chance(0,4,10,self.random_drop,10,self.rect.x,self.rect.y)
                self.kill()
            if self.move_counter > self.animation_cooldown:
                self.move_counter = 0
                self.index += 1
                if self.index == 6:
                    blob_bullet = Bullet_blob(self.rect.x + 30 * self.direction + 25, self.rect.y + tile_size + 14, self.direction)
                    enemy_group.add(blob_bullet)
                    blob_bullet_group.add(blob_bullet)
                elif self.index >= len(self.images_left):
                    self.index = 0
            if self.rect.x - player.rect.x >= 0:
                self.image = self.images_left[self.index]
                self.direction = -1
            elif self.rect.x - player.rect.x < 0:
                self.image = self.images_right[self.index]
                self.direction = 1
        screen.blit(self.image, (self.rect.x - 30 + 5 * (self.direction + 1), self.rect.y - 8))


#class for Bat
class Bat(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.damage_health_class = damage_health(50,10,1,5,10)
        self.images_bat = im.images_bat
        self.index = 0
        self.image = self.images_bat[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.health = 10
        self.activate = 0
        self.animation_cooldown = 5
        self.counter = 0
        self.random_drop = random.randint(1,3)
        self.hurt_cooldown = 15
        self.dmg_allow = 0
        self.attack_cooldown = 0
        self.theta = 0
        self.fraction = 0

    #updates the bat's position, flying direction, and animation
    def update(self):
        self.hurt_cooldown += 1
        scrolling(self)
        if self.health <= 0:
            coin_chance(-1,1,5,self.random_drop,5,self.rect.x,self.rect.y)
            self.kill() 
        if self.activate != 0:
            self.fraction = self.rect.x - player.rect.x
            self.attack_cooldown += 1
            self.counter += 1
            self.damage_health_class.update(self, self.rect.x, self.rect.y, 0, 10, self.health, self.hurt_cooldown)
            if self.fraction != 0:
                self.theta = abs(np.arctan((player.rect.y - self.rect.y)/(self.rect.x - player.rect.x)))
            else:
                self.fraction = 1
            if self.counter >= self.animation_cooldown:
                self.index += 1
                self.counter = 0
            if self.index >= 4:
                self.index = 0
            if self.activate == 1 and self.hurt_cooldown > 10:
                self.rect.x -= 2*(self.rect.x - player.rect.x)/100 + 9*(self.rect.x - player.rect.x)/np.sqrt((self.rect.x - player.rect.x)**2 + (player.rect.y - self.rect.y)**2)
                self.rect.y += 5*np.sin(self.attack_cooldown*np.pi/60) + 9*(player.rect.y - self.rect.y + 20)/np.sqrt((self.rect.x - player.rect.x)**2 + (player.rect.y - self.rect.y)**2)
                self.image = self.images_bat[self.index + 5]
            elif self.activate == -1 and self.hurt_cooldown > 10:
                self.rect.x -= (self.rect.x - player.rect.x + ((player.rect.x - self.rect.x)/abs(self.fraction))*200*np.cos(self.theta))/20
                self.rect.y += (player.rect.y - self.rect.y - 200*np.sin(self.theta))/20
                self.image = self.images_bat[self.index]
            if self.attack_cooldown >= 120:
                self.attack_cooldown = 0
                self.activate *= -1
        elif abs(self.rect.x - player.rect.x) <= 500:
            self.activate = -1
        else:
            self.image = self.images_bat[4]
        if self.hurt_cooldown <= 10:
            self.rect.x -= (10*np.cos(self.theta) - self.hurt_cooldown**2/50) * (player.rect.x - self.rect.x)/abs(player.rect.x - self.rect.x)
            self.rect.y -= (10*np.sin(self.theta) - self.hurt_cooldown**2/50) * (player.rect.y - self.rect.y)/abs(player.rect.y - self.rect.y)


#class for Green Blob
class GB(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.index = 0
        self.images_left = im.images_gb_left
        self.images_right = im.images_gb_right
        self.hitbox = im.gb_hitbox
        pygame.sprite.Sprite.__init__(self)
        self.damage_health_class = damage_health(100, 20, 0,10,0)
        self.image = self.images_left[self.index]
        self.rect = self.hitbox.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.hitbox.get_width()
        self.height = self.hitbox.get_height()
        self.direction = 1
        self.animation_cooldown = 10
        self.move_counter = 0
        self.health = 20
        self.random_drop = random.randint(10,15)
        self.hurt_cooldown = 15
        self.activate = 0
        self.throw = 0
        self.xinit = 0
        self.yinit = 0
        self.timer = 0
        self.dmg_allow = 0
        self.dx = 0

    #updates the green blob's position, direction, and animation
    def update(self):
        scrolling(self)

        if not mob_is_active(self):
            return
        
        self.dx = 0
        self.move_counter += 1
        self.hurt_cooldown += 1
        if abs(self.rect.x - player.rect.x) <= 1100:
            self.damage_health_class.update(self,self.rect.x,self.rect.y, 0, 10, self.health,self.hurt_cooldown)
        if self.health <= 0:
            player.gb_hurt = False
            key = pygame.key.get_pressed()
            direction(self, self.images_right, self.images_left, 6)
            self.activate = 1
            self.timer += 1
            if 0 < self.timer <= 20 or 40 <= self.timer <= 60 or 80 <= self.timer <= 100 or 120 <= self.timer < 140:
                direction(self, self.images_right, self.images_left, 5)
            elif self.timer == 140:
                explosion = GBexplosion(self.rect.x - 50, self.rect.y - 50)
                enemy_group.add(explosion)
                GBexplosion_group.add(explosion)
                self.throw = 3
                coin_chance(-1,1,5,self.random_drop,5,self.rect.x,self.rect.y)
                player.gb_hurt = True
                self.kill()
            if (key[keys_list[5]] and abs((player.rect.x + 25)  - self.rect.x - (self.width/2)) < 120 and self.throw == 0) or self.throw == 2:
                self.throw = 2
                self.rect.x = player.rect.x - 25
                self.rect.y = player.rect.y - 100
                pos = display.get_mouse_pos()
                #get mouse position
                x = pos[0]
                y = pos[1]
                if (
                    pos[0] < screen_width
                    and pos[1] < screen_height
                    and pygame.mouse.get_pressed()[2] == 1
                ):
                    self.throw = 1
                    self.move_counter = 0
                    if x - player.rect.x == 0:
                        self.xinit = 0
                        self.yinit = 10
                    elif x - player.rect.x < 0:
                        self.xinit = -np.cos(np.arctan((player.rect.y - y)/(x - player.rect.x))) *10
                        self.yinit = -np.sin(np.arctan((player.rect.y - y)/(x - player.rect.x))) *10
                    else:
                        self.xinit = np.cos(np.arctan((player.rect.y - y)/(x - player.rect.x))) *10
                        self.yinit = np.sin(np.arctan((player.rect.y - y)/(x - player.rect.x))) *10
            elif self.throw == 1:
                self.rect.x += 2*self.xinit
                self.rect.y -= 2*self.yinit - self.move_counter**2/110

        #update gb's animation and movement while idleing
        elif self.health > 0:
            if self.move_counter > self.animation_cooldown and self.activate == 0:
                self.index += 1
                self.move_counter = 0
                if self.index >= 4:
                    self.index = 0
                direction(self, self.images_right, self.images_left, self.index)
            if self.activate == 0:
                if self.hurt_cooldown > 10:
                    self.dx -= self.direction
                elif self.hurt_cooldown <= 10:
                    self.dx -= (10 - self.hurt_cooldown**2/50) * (player.rect.x - self.rect.x)/abs(player.rect.x - self.rect.x)
                    direction(self, self.images_right, self.images_left, 4)
            moving_collision(self, world.tile_list)
            moving_collision(self, world.blocker_list)
            self.rect.x += self.dx
        #pygame.draw.rect(screen, RED, (self.rect), 2)
        screen.blit(self.image, (self.rect.x, self.rect.y - 20))


#class for snow mounder
class SnowMounder(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images_right = im.images_sm_right
        self.images_left = im.images_sm_left
        self.hat = im.sm_hat
        self.hitbox = im.sm_hitbox
        self.index = 0
        self.damage_health_class = damage_health(100,15,1,5,0)
        self.image = self.hitbox
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.animation_cooldown = 8
        self.health = 15
        self.random_drop = random.randint(8,12)
        self.hurt_cooldown = 15
        self.move_counter = 0
        self.direction = 1
        self.dmg_allow = 0

    #update snow mounder's direction, animation, and health
    def update(self):
        scrolling(self)
        if abs(player.rect.x - self.rect.x - (self.width / 2)) < 1100:
            self.move_counter += 1
            self.hurt_cooldown += 1
            if self.health <= 0:
                coin_chance(0,3,8,self.random_drop,8,self.rect.x,self.rect.y)
                self.kill()
            if self.move_counter > self.animation_cooldown:
                self.move_counter = 0
                self.index += 1
                if self.index == 7:
                    mounder_bullet = Bullet_Mounder(self.rect.x + tile_size/2, self.rect.y, self.direction)
                    enemy_group.add(mounder_bullet)
                    mounder_bullet_group.add(mounder_bullet)
                elif self.index >= len(self.images_left):
                    self.index = 0
            if self.rect.x - player.rect.x <= 0:
                self.image = self.images_left[self.index]
                if self.direction == 1:
                    self.direction *= -1
                    self.offset = 1
            else:
                self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.direction *= -1
                    self.offset = 3
            self.damage_health_class.update(self, self.rect.x, self.rect.y, 0, 20, self.health, self.hurt_cooldown)
        screen.blit(self.image, (self.rect.x, self.rect.y - 45))


#class for cubeoid
class Cubeoid(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images_right = im.images_cubeoid_right
        self.images_left = im.images_cubeoid_left
        self.index = 0
        self.image = self.images_right[23]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.animation_cooldown = 8
        self.move_counter = 0
        self.direction = 1
        self.activate = 0
        self.xoffset = 50
        self.yoffset = 65
        self.moving_speed = 0
        self.slide_particles = []
        self.slide_particle_counter = 0

    #update the cubeoid's position, animation, and health
    def update(self):
        self.move_counter += 1
        scrolling(self)

        if not mob_is_active(self):
            return
    
        #if player is near, starting sliding
        if self.activate == 1:
            self.moving_speed = 5 * self.direction
            direction(self, self.images_right, self.images_left, 23)
            self.xoffset = 0
            self.yoffset = 0
            self.rect.x += 5 * self.direction
            self.slide_particle_counter += 1 
            if self.slide_particle_counter > 3:
                self.slide_particle_counter = 0
                for i in range(random.randint(1,3)):
                    self.slide_particles.append([[self.rect.x, self.rect.y], random.randint(4,6), random.randint(2,4), random.randint(3,6), self.direction])
            for particle in self.slide_particles:
                particle[0][0] -= particle[1]*particle[4]
                particle[0][1] -= particle[2]
                particle[3] -= 1
                particle = particle_scrolling(particle)
                pygame.draw.rect(screen, LIGHT_BLUE, (particle[0][0] + 50 - 35*particle[4], particle[0][1] + 100, 3, 3))
                if particle[3] < 0:
                    self.slide_particles.remove(particle)
        #if player is not near, do idle walk
        elif self.activate == 0:
            direction(self, self.images_right, self.images_left, self.index)
            if self.move_counter > self.animation_cooldown:
                self.move_counter = 0
                self.index += 1
                if 3 <= self.index <= 5 or 15 <= self.index <=16:
                    self.rect.x += 5 * self.direction
                elif self.index >= 23:
                    self.index = 0
            if abs(self.rect.x - player.rect.x) <= 300:
                self.activate = 2
                self.move_counter = 0
        #if player gets in range, prepare to slide
        elif self.activate == 2:
            if 0 <= self.move_counter <= 13:
                direction(self, self.images_right, self.images_left, 5)
            elif 13 < self.move_counter <= 26:
                direction(self, self.images_right, self.images_left, 24)
            elif self.move_counter > 26:
                self.activate = 1
        #pygame.draw.rect(screen, RED, (self.rect.x + 5*self.direction, self.rect.y, self.width, self.height), 2)
        #pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y, self.width, self.height), 2)
        #if collided with tile, turn around
        for tile in world.tile_list + world.blocker_list:
            if tile[1].colliderect(self.rect.x + 5*self.direction, self.rect.y, self.width, self.height):
                self.direction *= -1
                break
        screen.blit(self.image, (self.rect.x - self.xoffset, self.rect.y - self.yoffset))


#class for snow soldier
class Snow_Soldier(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images_right = im.images_ss_right
        self.images_left = im.images_ss_left
        self.hitbox = im.ss_hitbox
        self.index = 0
        self.damage_health_class = damage_health(100,15,1,5,0)
        self.random_drop = random.randint(10,15)
        self.image = self.hitbox
        self.rect = self.hitbox.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = -1
        self.animation_cooldown = 8
        self.hurt_cooldown = 15
        self.move_counter = 0
        self.health = 15
        self.x_offset = -50
        self.dmg_allow = 0
        self.activate = 0
        self.dx = 0
        self.running = 1
        self.chase_dead_zone = 10

    def update(self):
        scrolling(self)

        if not mob_is_active(self):
            return
    
        self.dx = 0
        self.hurt_cooldown += 1
        self.move_counter += 1
        self.damage_health_class.update(self, self.rect.x - 10, self.rect.y, 0, 15, self.health, self.hurt_cooldown)
        if self.move_counter >= self.animation_cooldown:
            self.index += 1
            self.move_counter = 0
            if self.index >= 7 and self.activate >= 0:
                self.index = 0
            elif self.index >= 11 and self.activate == -1:
                self.activate = 2
                self.index = 0
                self.animation_cooldown = 8
        elif self.hurt_cooldown > 10 and self.activate >= 0:
            should_move = True
            if self.activate == 2:
                self.running = 3
                horizontal_distance = player.rect.centerx - self.rect.centerx
                if horizontal_distance > self.chase_dead_zone:
                    self.direction = 1
                elif horizontal_distance < -self.chase_dead_zone:
                    self.direction = -1
                else:
                    should_move = False
            if self.direction == 1:
                self.x_offset = 0
            elif self.direction == -1:
                self.x_offset = -50
            if should_move:
                self.dx += 2*self.direction*self.running
            direction(self, self.images_right, self.images_left, self.index)
        elif self.hurt_cooldown <= 10:
            self.dx -= (10 - self.hurt_cooldown**2/50) * (player.rect.x - self.rect.x)/abs(player.rect.x - self.rect.x)
            direction(self, self.images_right, self.images_left, 7)
        elif self.activate == -1 and self.index < 11:
            self.animation_cooldown = 5
            self.x_offset = -40 + 11 * (1 + self.direction)
            direction(self, self.images_right, self.images_left, self.index)
        moving_collision(self, world.tile_list)
        moving_collision(self, world.blocker_list)
        if self.health <= 0:
            coin_chance(-1, 1, 5, self.random_drop, 5 ,self.rect.x, self.rect.y)
            self.kill()
        if (
            abs(self.rect.x - player.rect.x) <= 200
            and player.rect.bottom <= self.rect.bottom
            and self.activate == 0
        ):
            self.activate = -1
            self.index = 7
            self.move_counter = 0
        self.rect.x += self.dx
        #pygame.draw.rect(screen, RED, (self.rect), 2)
        screen.blit(self.image, (self.rect.x + self.x_offset, self.rect.y - 55))


#create bullet class for blob
class Bullet_blob(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = im.bullet_blob_img
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction
        self.rect.center = (x,y)
        self.counter = 0
        self.rand = random.randint(3,8)

    def update(self):
        #move bullet
        rand_spawn = random.randint(0,2)
        if rand_spawn == 0:
            snow_particle_list.append([[self.rect.x + (self.width/2), self.rect.y + (self.height/2)], random.randint(1, 3), random.randint(1,3), random.randint(1,3)])
        self.rect.x += (self.direction * self.rand) 
        self.counter += 1
        self.rect.y += (self.counter**2)/50
        #check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > screen_width:
            self.kill()
            #check if bullet has collided with tile
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect):
                self.kill()
        scrolling(self)


#create bullet class for snow mounder
class Bullet_Mounder(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = im.bullet_mounder
        self.hitbox = im.sm_bullet_hitbox
        self.rect = self.hitbox.get_rect()
        self.width = self.hitbox.get_width()
        self.height = self.hitbox.get_height()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        self.speed = 10
        self.lifetime = 100
        self.position = pygame.math.Vector2(self.rect.topleft)
        trajectory = pygame.math.Vector2(
            player.rect.centerx - self.rect.centerx,
            player.rect.centery - self.rect.centery
        )
        if trajectory.length_squared() == 0:
            trajectory.x = -self.direction
        self.velocity = trajectory.normalize() * self.speed
        if self.direction == -1:
            self.image = pygame.transform.flip(im.bullet_mounder, True, False)
    
    def update(self):
        # Follow the trajectory captured when the snowball was thrown.
        self.position += self.velocity
        if scroll_left == True or scroll_right == True:
            self.position.x -= scroll_speed
        self.rect.topleft = (round(self.position.x), round(self.position.y))
        self.lifetime -= 1
        if self.rect.right < 0 or self.rect.left > screen_width or self.lifetime <= 0:
            self.kill()
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect):
                self.kill()
        screen.blit(self.image, (self.rect.x - 15, self.rect.y - 15))


#create torch class
class torch():
    def __init__(self):
        self.animation_cooldown = 8
        self.images_torch = im.images_torch
        self.reset()

    def reset(self):
        self.index = 0
        self.move_counter = 0
        self.particles = []
        self.torch_position = world.torch_position

    def update(self):
        viewport = screen.get_rect()
        visible_torches = []
        for torch_position in self.torch_position:
            draw_position = (torch_position[0] - scroll, torch_position[1])
            torch_rect = self.images_torch[self.index].get_rect(topleft=draw_position)
            if torch_rect.colliderect(viewport):
                visible_torches.append(draw_position)

        if visible_torches:
            self.move_counter += 1
            if self.move_counter > self.animation_cooldown:
                self.move_counter = 0
                self.index = (self.index + 1) % len(self.images_torch)

            for draw_position in visible_torches:
                screen.blit(self.images_torch[self.index], draw_position)
                if random.randint(0,3) == 0:
                    self.particles.append([
                        [draw_position[0] + 16 + random.randint(0,10), draw_position[1] + 5],
                        [random.randint(0, 20) / 10 - 1, -2],
                        random.randint(4, 6),
                        255
                    ])

        for particle in self.particles[:]:
            particle[0][1] -= 1
            particle[2] -= 0.1
            particle[3] -= 5
            particle_scrolling(particle)
            if viewport.collidepoint(particle[0]):
                pygame.draw.rect(
                    transparent_surface,
                    (0,0,0,particle[3]),
                    [int(particle[0][0]), int(particle[0][1]), 5,5]
                )
            if particle[2] <= 1:
                self.particles.remove(particle)


#create class to make hitbox
class HB(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.hitbox_img = im.hitbox
        self.image = self.hitbox_img
        self.hitbox_delay = 0
        self.hitbox_direction = attacks_class.get_hitbox_direction()
        if self.hitbox_direction == 2:
            self.image = pygame.transform.flip(self.hitbox_img, True, False)
        elif self.hitbox_direction == 3:
            self.image = pygame.transform.scale(self.hitbox_img, (100, 100))
        elif self.hitbox_direction == 4:
            self.image = pygame.transform.rotate(self.hitbox_img, -90)
        elif self.hitbox_direction == 5:
            self.image = pygame.transform.scale(self.hitbox_img, (120, 75))
        elif self.hitbox_direction == 6:
            self.image = pygame.transform.scale(self.hitbox_img, (120, 75))
        elif self.hitbox_direction == 7:
            self.image = pygame.transform.scale(self.hitbox_img, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if player.in_air == False:
            self.hitbox_delay += 1
            if self.hitbox_direction == 1:
                self.rect.x = player.rect.x + 60
                self.rect.y = player.rect.y + 10
            elif self.hitbox_direction == 2:
                self.rect.x = player.rect.x - 130
                self.rect.y = player.rect.y + 10
            elif self.hitbox_direction == 3:
                self.rect.center = (player.rect.x + 30,player.rect.y - 60)
            elif self.hitbox_direction == 4:
                self.rect.center = (player.rect.x + 20,player.rect.y + 150)
        elif player.in_air == True:
            self.hitbox_delay += 1
            if self.hitbox_direction == 5:
                self.rect.x = player.rect.x + 50
                self.rect.y = player.rect.y + 10
            elif self.hitbox_direction == 6:
                self.rect.x = player.rect.x - 120
                self.rect.y = player.rect.y + 10
            elif self.hitbox_direction == 7:
                self.rect.center = (player.rect.x + 30,player.rect.y - 50)
        #pygame.draw.rect(screen, WHITE, self.rect, 2)
        if self.hitbox_delay >= 4:
            self.kill()


#Explosion for green blob
class GBexplosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.index = 0
        self.counter = 0
        self.animation_cooldown = 5
        pygame.sprite.Sprite.__init__(self)
        self.GB_explosion = im.gb_explosion
        self.image = self.GB_explosion[self.index]
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.counter += 1
        if self.counter > self.animation_cooldown:
            self.index += 1
            self.counter = 0
            if self.index >= 3:
                self.index = 0
                self.kill()
        self.image = self.GB_explosion[self.index]
        scrolling(self)


#create class for sling shot
class Sling(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = im.images_crystal
        self.image_unactive = im.images_crystal
        self.image_active = im.images_crystal_active
        self.rect = self.image[0].get_rect()
        self.width = self.image[0].get_width()
        self.height = self.image[0].get_height()
        self.rect.x = x
        self.rect.y = y
        self.slinging = False
        self.index = 0
        self.timer = 7
        self.crystal_timer = 0
        self.sling_angle = 0
        self.animation_cooldown = 8
        self.direction = 1
        self.proximity = False
        self.use_cooldown = 0
        self.activate_particle_list = []

    def update(self):
        scrolling(self)
        self.crystal_timer += 1
        self.use_cooldown += 1
        if self.crystal_timer >= self.animation_cooldown:
            self.crystal_timer = 0
            self.index += 1
            if self.index >= 4:
                self.index = 0
        if self.proximity == True:
            self.image = self.image_active
            if self.rect.x + 50 - player.rect.x  - player.width/2 > 0:
                pre_angle = np.arctan((player.rect.y + player.height/2 - self.rect.y - 50) / (self.rect.x + 50 - player.rect.x - player.width/2))
                self.sling_angle = round(4*pre_angle/np.pi) * np.pi/4
                self.direction = 1
            elif self.rect.x + 50 - player.rect.x  - player.width/2 < 0:
                self.direction = -1
                pre_angle = np.arctan((player.rect.y + player.height/2 - self.rect.y - 50) / (player.rect.x + player.width/2 - self.rect.x - 50))
                self.sling_angle = round(4*pre_angle/np.pi) * np.pi/4
            elif self.rect.x + 50 - player.rect.x  - player.width/2 == 0:
                self.sling_angle = np.pi/2
            pygame.draw.circle(screen, RED, (self.rect.x + 50 + self.direction*50*np.cos(self.sling_angle), self.rect.y + 50 - 50*np.sin(self.sling_angle)), 5)
        else:
            self.image = self.image_unactive
        if self.slinging == True:
            if self.timer == 7:
                player.vel_y = int(-35 * np.sin(self.sling_angle))
            self.timer -= 0.3
            if self.timer < 1:
                self.timer = 0
            player.sling_dx += int(self.timer**2 * self.direction * np.cos(self.sling_angle))
            if self.timer <= 0:
                self.timer = 7
                player.sling_dx = 0
                self.slinging = False
        sling_particle(self)
        #pygame.draw.rect(screen, RED, self.rect, 2)
        screen.blit(self.image[self.index], (self.rect.x, self.rect.y))


#create class for falling platforms
class MovingPlatform():
    def __init__(self):
        self.platform_position = world.platform_position
        for loc in self.platform_position:
            if loc[7] == 73:
                loc[6].x = loc[0] - scroll - 5
                loc[6].y = loc[1]
            else:
                loc[6].x = loc[0] - scroll
                loc[6].y = loc[1]


    #animate and move platforms
    def update(self):

        self.platform_position = world.platform_position
        for loc in self.platform_position:
            
            if scroll_left == True or scroll_right == True:
                loc[6].x -= scroll_speed

            if not rect_is_active(loc[6]):
                continue

            if loc[8] == 0:
                if loc[7] != 52:
                    loc[4] += 1
                    if loc[7] == 73:
                        loc[3] = loc[4]
                    if loc[7] == 74:
                        loc[3] = loc[4]
                    loc[6].x += loc[2]
                    loc[6].y += loc[3]
                for tile in world.tile_list:
                    if tile[1].colliderect(loc[6].x + loc[2], loc[6].y, loc[6].width, loc[6].height):
                        pass
                    elif tile[1].colliderect(loc[6].x, loc[6].y + loc[3], loc[6].width, loc[6].height):
                        if loc[7] == 73 or loc[7] == 74:
                            loc[6].y -= loc[6].bottom - tile[1].top
                            loc[8] = 1
            screen.blit(loc[5], (loc[6].x, loc[6].y))
            pygame.draw.rect(screen, RED, (loc[6]), 2)


#create class for damage object
class DamageObj():
    def __init__(self):
        pass


#create class for shop
class Shop():
    def __init__(self, x, y):
        self.image = im.shop_list
        self.shard_transform_list = im.shard_transform_list
        self.coin = im.money_icon
        self.bar = im.shop_bar
        self.shard_list = im.shard_list
        self.shop_keeper_list = im.shop_keeper_list
        self.rect = self.image[0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.allow = True
        self.shine_allow = False
        self.enter_shop = False
        self.collide_shop = False
        self.catalog_timer = 14
        self.indicator_timer = 10
        self.shop_timer = 0
        self.keeper_timer = 0
        self.keeper_animation = 0
        self.animation_timer = 0
        self.shine_timer = 0
        self.shine_animation = 0
        self.rand_x = 0
        self.rand_y = 0
        self.catalog_x = 0
        self.able_click = 0
        self.plus_list = []
        self.info_list = []
        self.new_shard = []
        self.shard_particles = []
        self.val_list = [0,0,0]
        self.prev_val = [0,0,0]
        self.price_list = [100,200,300,400,'-']
        self.info_word = [" Increase Attack Speed", "   Increase Potion Use", "    Increase Health"]
        for num in range(3):
            plus_rect = pygame.Rect((1706, 276 + 150*num), (60, 60))
            info_rect = pygame.Rect((1070, 250 + 150*num), (110, 110))
            self.plus_list.append([plus_rect, 0])
            self.info_list.append([info_rect, 0, 11])

    #open shop and change upgrades
    def update(self, position):
        self.rect.topleft = (position[0] - scroll, position[1])
        self.shop_timer += 0.05
        self.keeper_timer += 1
        if self.shop_timer > 2:
            self.shop_timer = 0
        if self.keeper_timer >= 500:
            self.keeper_animation += 0.1
            if self.keeper_animation >= 8:
                self.keeper_timer= 0
                self.keeper_animation = 0
            screen.blit(self.shop_keeper_list[int(self.keeper_animation)], (self.rect.x, self.rect.y))
        else:
            screen.blit(self.shop_keeper_list[int(self.shop_timer)], (self.rect.x, self.rect.y))
        screen.blit(self.image[int(self.shop_timer)], (self.rect.x, self.rect.y))
        
        #check if user right clicks when close to shop
        if self.rect.colliderect(player):
            self.collide_shop = True
            self.indicator_timer -= 1
            self.indicator_timer = sorted([0, self.indicator_timer])[1]
            draw_text("Shop", pygame.font.Font(im.FONT_PATH, 80), YELLOW, self.rect.x + 65, self.rect.y - 100 - self.indicator_timer**2)
            draw_text(f"Press [{pygame.key.name(keys_list[5])}]", pygame.font.Font(im.FONT_PATH, 30), WHITE, self.rect.x + 85, self.rect.y - 25 - self.indicator_timer**2)
            if self.enter_shop == True and self.allow == True:
                sfx.paper_list[random.randint(0,2)].play()
                self.animation_timer = 0
                self.able_click = 0
                self.catalog_timer = 14
                self.catalog_x = 0
                self.allow = False
        else:
            self.allow = False
            self.enter_shop = False
            self.collide_shop = False
            self.indicator_timer = 10
            self.catalog_timer = 14
            self.catalog_x = 0
        #if user decides to shop, pull up the catalog
        if self.enter_shop == True:
            mouse_rect = pygame.Rect(pos[0],pos[1],5,5)
            self.able_click += 1
            self.catalog_timer -= 1
            self.animation_timer += 1
            if self.catalog_timer <= 0:
                self.catalog_timer = 0
            self.catalog_x += self.catalog_timer**2
            pygame.draw.rect(screen, GREY, (1739 - self.catalog_x, 0, 700, 800))
            screen.blit(self.bar, (1739 - self.catalog_x, 0))
            upgrade_particle(self)
            draw_text("UPGRADES", pygame.font.Font(im.FONT_PATH, 150), YELLOW, 1930 - self.catalog_x, 30 + 10*np.sin(np.pi*self.animation_timer/100))
            #show cost of each upgrade and takes care of transactions
            for num, tile in enumerate(self.info_list):
                if tile[0].colliderect(mouse_rect):
                    pygame.draw.rect(screen, GREY, (pos[0] - 400, pos[1] - 50, 350, 50), 0, 8)
                    draw_text(f"{self.info_word[num]}", pygame.font.Font(im.FONT_PATH, 30), BLACK, pos[0] - 400, pos[1] - 40)
            #keeps track of coin shine animation
            self.shine_timer += 1
            if self.shine_timer >= 100:
                self.shine_allow = True
                self.shine_timer = 0
            if self.shine_allow == True:
                self.shine_animation += 0.15
                if self.shine_animation > 5:
                    self.shine_allow = False
                    self.shine_animation = 0
            #draw coins
            for num, val in enumerate(self.prev_val):
                for i in range(val):
                    screen.blit(self.shard_list[int(self.shine_animation)], (2034 + 75*i - self.catalog_x, 255 + 150*num))
            #buy upgrade if player has enough coins
            for num, tile in enumerate(self.plus_list):
                if tile[0].colliderect(mouse_rect) and pygame.mouse.get_pressed()[0] == 1 and self.able_click >= 20 and self.val_list[num] < 4:
                    if coin_animate_class.coin_own >= self.price_list[num]:
                        self.val_list[num] += 1
                        coin_animate_class.coin_own -= self.price_list[num]
                        self.new_shard.append([num, self.val_list[num], 9])
                        self.able_click = 0
                        if num == 0:
                            player.attack_cooldown -= 5
                        elif num == 2:
                            player.max_health += 1
                    else:
                        self.plus_list[num][1] = 10
                        self.rand_x = random.randint(-10,10)
                        self.rand_y = random.randint(-10,10)
                if self.plus_list[num][1] > 0:
                    self.plus_list[num][1] -= 0.8
                    screen.blit(self.coin, (1546 + self.rand_x*np.sin(2*self.plus_list[num][1]*np.pi/5), 280 + 150*num + self.rand_y*np.sin(2*self.plus_list[num][1]*np.pi/5)))
                    draw_text(f'{self.price_list[self.prev_val[num]]}', font, RED, 1596 + self.rand_x*np.sin(2*self.plus_list[num][1]*np.pi/5), 285 + 150*num + self.rand_y*np.sin(2*self.plus_list[num][1]*np.pi/5))
                else:
                    screen.blit(self.coin, (2365 - self.catalog_x, 280 + 150*num))
                    draw_text(f'{self.price_list[self.prev_val[num]]}', font, WHITE, 2415 - self.catalog_x, 285 + 150*num)
                #pygame.draw.rect(screen, RED, self.info_list[num], 5)

            #animate upgrade shard
            for num, val in enumerate(self.new_shard):
                screen.blit(self.shard_transform_list[round(val[2])], (1140 + 75*val[1], 255 + 150*val[0]))
                val[2] -= 0.7
                if val[2] < 0:
                    for i in range(random.randint(10,20)):
                        self.shard_particles.append([[1180 + 75*val[1], 310 + 150*val[0]], random.randint(3,6), random.randint(0,360)*np.pi/180, random.randint(10,30)])
                    self.prev_val = self.val_list.copy()
                    self.new_shard = []
            pygame.draw.rect(screen, WHITE, mouse_rect)


#create class for potion
class Potion():
    def __init__(self):
        self.image = im.images_potion
        self.amount_heal = 1
        self.potion_max = 2
        self.uses_left = self.potion_max
        self.potion = 0
        self.heal = False
        self.animation_cooldown = 8
        self.counter = 0
        self.index = 0

    #animate the potion icon and update the player's health
    def update(self):
        self.counter += 1
        if self.counter >= self.animation_cooldown:
            self.index += 1
            self.counter = 0
            if self.index >= 3:
                self.index = 0
        screen.blit(self.image[self.potion][self.index], (10,30))
        if self.heal == True:
            if player.health < player.max_health:
                if player.health >= player.max_health - self.amount_heal:
                    player.previous_health = player.max_health
                    player.health = player.max_health
                else:
                    player.previous_health += self.amount_heal
                    player.health += self.amount_heal
                if self.uses_left <= self.potion_max:
                    self.potion += 1
                else:
                    self.potion = 3
            self.heal = False


#create class for unlocking abilities
class upgrade_unlock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = im.upgrade_stand
        self.upg_list = im.upgrade_list
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = x
        self.rect.y = y
        self.time = 0
        self.points = [[-1,-1,-1], [-1,-1,1], [-1,1,1], [-1,1,-1], [1,-1,-1], [1,-1,1], [1,1,1], [1,1,-1]]
        self.lines = []
        self.vertx = 0
        self.verty = 0
        self.random_part = random.randint(10,15)
        self.part_list = []
        self.upgrade_list = [player.dash_unlock]
        for num in range(self.random_part):
            self.part_list.append([self.rect.x, self.rect.y, random.randint(10,15), random.randint(10,15), random.randint(10,50), random.randint(10,50), random.randint(0,50)])


    def update(self):
        scrolling(self)
        self.time += 1
        self.lines = []
        key = pygame.key.get_pressed()
        for point in self.points:
            #self.vertx = point[0]*(np.cos(np.pi*self.time/50)**2 - np.sin(np.pi*self.time/50)**3) + 0.5*(point[2] - point[1] + point[2]*np.sin(np.pi*self.time/50))*np.sin(np.pi*self.time/25)
            #self.verty = 0.5*point[0]*np.sin(np.pi*self.time/25) + (point[2] + point[0]*np.cos(np.pi*self.time/50))*np.sin(np.pi*self.time/50)**2 + (point[1] - point[2]*np.sin(np.pi*self.time/50))*np.cos(np.pi*self.time/50)**2
            self.vertx = 20*(point[0]*np.cos(np.pi*self.time/100) + point[2]*np.sin(np.pi*self.time/100)) + self.rect.x + (self.width/2)
            self.verty = 20*(point[1]*np.cos(np.pi*self.time/100) + point[0]*np.sin(np.pi*self.time/100)**2 - 0.5*point[2]*np.sin(np.pi*self.time/50)) + self.rect.y + 30*np.sin(np.pi*self.time/100) + 10
            self.lines.append([self.vertx, self.verty])
            #pygame.draw.circle(screen, BLACK, (self.vertx, self.verty), 5)

        pygame.draw.lines(screen, BLACK, True, [(self.lines[0][0], self.lines[0][1]), (self.lines[1][0], self.lines[1][1]), (self.lines[2][0], self.lines[2][1]), (self.lines[3][0], self.lines[3][1])], 3)
        pygame.draw.lines(screen, BLACK, True, [(self.lines[4][0], self.lines[4][1]), (self.lines[5][0], self.lines[5][1]), (self.lines[6][0], self.lines[6][1]), (self.lines[7][0], self.lines[7][1])], 3)
        pygame.draw.line(screen, BLACK, (self.lines[0][0], self.lines[0][1]), (self.lines[4][0], self.lines[4][1]), 3)
        pygame.draw.line(screen, BLACK, (self.lines[1][0], self.lines[1][1]), (self.lines[5][0], self.lines[5][1]), 3)
        pygame.draw.line(screen, BLACK, (self.lines[2][0], self.lines[2][1]), (self.lines[6][0], self.lines[6][1]), 3)
        pygame.draw.line(screen, BLACK, (self.lines[3][0], self.lines[3][1]), (self.lines[7][0], self.lines[7][1]), 3)
        for particle in self.part_list:
            pygame.draw.rect(screen, BLACK, (self.rect.x + 50 + particle[2]*np.cos(np.pi*self.time/particle[4]), self.rect.y + 10 + particle[3]*np.sin(np.pi*self.time/particle[5]) + 30*np.sin(np.pi*self.time/100), 5, 5))
        for index, num in enumerate(upgrade_group):
            if num.rect.colliderect(player) and key[keys_list[5]]:
                if index == 0:
                    player.dash_unlock = True
                upg_animate_class = upg.Upgrade_Animation(screen_width, screen_height, player.rect.x, player.rect.y, transparent_surface, screen, index)
                upg_animate_class.update(screen)


#create class for grass
class Grass():
    def __init__(self):
        self.grass_color = [GREEN, DARK_GREEN]
        self.reset()

    def reset(self):
        self.grass_position = world.grass_position
        self.grass_list = []
        self.collision_list = []
        self.grass_particles = []
        for loc in self.grass_position:
            for i in range(random.randint(8,12)):
                self.image = pygame.image.load(f'{im.ASSETS_DIR}/grass/{random.randint(1,3)}.png').convert_alpha()
                self.grass_list.append([loc[0] + random.randint(0,50), loc[1], self.image, self.image, 0, 0, random.randint(0,360), self.image.get_rect()])


    #animate the grass by rotating the grass image around the base
    def update(self):
        for data in self.grass_list:
            if abs(data[7].x - player.rect.x - 25) < 1050:
                data[6] += 2
                data[4] += (data[5] - data[4])/4
                data[7] = data[2].get_rect()
                data[7].center = (data[0] - scroll, data[1] + 50)
                screen.blit(data[2], data[7])
                if data[7].colliderect(player.rect):
                    data[2] = pygame.transform.rotate(data[3], data[4])
                    if data[7].center[0] > player.rect.center[0]:
                        data[5] = -80 + 1.5*(data[7].center[0] - player.rect.center[0])
                    elif data[7].center[0] < player.rect.center[0]:
                        data[5] = 80 + 1.5*(data[7].center[0] - player.rect.center[0])
                else:
                    data[5] = 0
                    data[2] = pygame.transform.rotate(data[3], data[4] + 10*np.sin(data[6]*np.pi/180))
                if len(hitbox_group) > 0:
                    if data[7].colliderect(hitbox_group.sprites()[0]):
                        for i in range(random.randint(2,5)):
                            self.grass_particles.append([[data[0] - scroll + 25, data[1] + 25], random.randint(-3,3), random.randint(0,10), random.randint(10,30), 0, random.choice(self.grass_color)])
                        self.grass_list.remove(data)

            else:
                data[7].center = (data[0] + 25 - scroll, data[1] + 50)
        for particle in self.grass_particles:
            particle[3] -= 1
            particle[4] += 0.5
            particle[0][0] += particle[1]
            particle[0][1] -= particle[2] - particle[4]
            pygame.draw.rect(screen, particle[5], (particle[0][0], particle[0][1], 4, 4))
            particle = particle_scrolling(particle)
            if particle[3] <= 1:
                self.grass_particles.remove(particle)


def reset_grass():
    world.refresh_grass_positions()
    grass_class.reset()


def reset_torches():
    world.refresh_torch_positions()
    bg_torch.reset()


def draw_page_one():
    for i in range(0, 42):
        if button_list[i].draw(screen):
            return i
def draw_page_two():
    for i in range(42, 77):
        if button_list[i].draw(screen):
            return i + 42
          
#types of groups and initialize classes
player = Player(screen_width/2 - scroll, screen_height - 300)
shop_class = Shop(1500 - scroll,700)
coin_animate_class = Coin_Animate()
potion_class = Potion()
dp_class = death_particle(-500,500, 100,100)
blocker_group = pygame.sprite.Group()
hitbox_group = pygame.sprite.Group()
GBexplosion_group = pygame.sprite.Group()
bat_group = pygame.sprite.Group()
blob_green_group = pygame.sprite.Group()
cubeoid_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
blob_bullet_group = pygame.sprite.Group()
mounder_bullet_group = pygame.sprite.Group()
blob_group = pygame.sprite.Group()
icicle_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
mounder_group = pygame.sprite.Group()
snow_soldier_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
attacks_class = attacks()
sling_group = pygame.sprite.Group()
ice_arms_group = pygame.sprite.Group()
spike_group = pygame.sprite.Group()
upgrade_group = pygame.sprite.Group()


#load in level data and create world
if menu_screen == True:
    menu_data_path = path.join(DATA_DIR, 'menu1_data')
    if path.exists(menu_data_path):
        pickle_in = open(menu_data_path, 'rb')
        world_data = pickle.load(pickle_in)
        menu_class = menu.Menu(screen, transparent_surface, world_data)
    menu_class.update()
if path.exists(get_level_data_path(level)):
    pickle_in = open(get_level_data_path(level), 'rb')
    world_data = pickle.load(pickle_in)
    scroll = 0
if path.exists(get_level_data_path(level, '_bg')):
    pickle_in_bg = open(get_level_data_path(level, '_bg'), 'rb')
    bg_data = pickle.load(pickle_in_bg)
if path.exists(get_level_data_path(level, '_front')):
    pickle_in_front = open(get_level_data_path(level, '_front'), 'rb')
    front_data = pickle.load(pickle_in_front)


world = World(world_data)
grass_class = Grass()
moving_plat_class = MovingPlatform()
liquid, bg_torch = bg_tiles()

run = True
while run:
    if fps >= 60:
        clock.tick_busy_loop(fps)
    else:
        clock.tick(fps)
    probe.begin()
    transparent_surface.fill((0,0,0,0))
    start = time.time()
    probe.mark('bg')
    draw_bg()
    probe.mark('world')
    world.draw()
    probe.mark('platforms')
    moving_plat_class.update()
    bg_torch.update()

    #draw grid when t button is pressed
    if grid_allow == 1:
        draw_grid()
        pygame.draw.rect(screen, GREEN, (screen_width - 300, 0, side_margin, screen_height))
        #choose a tile
        if button_page == 0:
            for i in range(0, 42):
                if button_list[i].draw(screen):
                    current_tile = i
        elif button_page == 1:
            for i in range(42, 77):
                if button_list[i].draw(screen):
                    current_tile = i
    probe.mark('enemies')
    bat_group.update()
    bat_group.draw(screen)
    GBexplosion_group.update()
    GBexplosion_group.draw(screen)
    blob_green_group.update()
    blob_group.update()
    mounder_group.update()
    mounder_bullet_group.update()
    cubeoid_group.update()
    snow_soldier_group.update()
    bullet_group.update()
    bullet_group.draw(screen)
    blob_bullet_group.update()
    blob_bullet_group.draw(screen)
    icicle_group.update()
    spike_group.update()
    sling_group.update()
    dp_class.update()
    potion_class.potion = liquid.update(potion_class.potion)
    if world.shop_position is not None:
        shop_class.update(world.shop_position)
    else:
        shop_class.enter_shop = False
        shop_class.collide_shop = False
        shop_class.allow = True
    probe.mark('player')
    player.update()
    probe.mark('front')
    grass_class.update()
    draw_front()
    probe.mark('rest')
    coin_group.update()
    coin_animate_class.update()
    game_over_index = exit(game_over_index, level)
    particle_allow = healing_particles(particle_allow)
    potion_class.update()
    upgrade_group.update()

    #world.ice_boss_class.update()
    #ice_arms_group.update()
    probe.mark('overlay')
    screen.blit(transparent_surface, (0 ,0))


    #text showing current level
    if show_debug_info:
        draw_text(f'Level: {level}', font, WHITE, 1650, 0)
        draw_text(f'FPS: {"{:.3f}".format(clock.get_fps())}', font, WHITE, 1650, 50)
    pos = display.get_mouse_pos()
    #get mouse position
    x = (pos[0] + scroll)//tile_size
    y = (pos[1])//tile_size
    attack_allow += 1
    #check that the coordinates are within the tile area
    if melee_allow == 0:
        if pos[0] < screen_width - 300 and pos[1] < screen_height:
            if pygame.mouse.get_pressed()[0] == 1:
                if world_data[y][x] != current_tile or bg_data[y][x] != current_tile:
                    if current_tile == 12:
                        bg_data[y][x] = -1
                        world_data[y][x] = -1
                        front_data[y][x] = -1
                    if current_tile == 1 or current_tile == 2 or current_tile == 3 or current_tile == 5:
                        front_data[y][x] = current_tile
                    elif current_tile == 54 or current_tile == 22 or current_tile == 11 or current_tile == 7 or current_tile == 9 or current_tile == 63 or current_tile == 65 or current_tile == 69 or current_tile == 71 or current_tile == 72 or current_tile == 76:
                        bg_data[y][x] = current_tile
                    else:
                        world_data[y][x] = current_tile
    elif melee_allow == 1:
        if pos[0] < screen_width and pos[1] < screen_height and attack_allow >= player.attack_cooldown and player.hurt_cooldown >= 15:
            if pygame.mouse.get_pressed()[0] == 1 and len(hitbox_group) == 0 and allow == 0 and player.long_jump == False:
                attacks_class.get_hitbox_direction()
                sfx.slash_list[random.randint(0,1)].play()
                hitbox = HB(0,-200)
                hitbox_group.add(hitbox)
                player.attack = True
                allow = 1
                attack_allow = 0
            elif pygame.mouse.get_pressed()[0] == 0 and pygame.mouse.get_pressed()[2] == 0:
                allow = 0
            for crystal in sling_group:
                if np.sqrt((player.rect.x + player.width/2 - crystal.rect.x - 50)**2 + (player.rect.y + player.height/2 - crystal.rect.y - 50)**2) < 250 and crystal.use_cooldown > 50:
                    crystal.proximity = True
                    if pygame.mouse.get_pressed()[2] == 1 and allow == 0:
                        crystal.use_cooldown = 0
                        player.in_air = True
                        crystal.slinging = True
                        sfx.sling.play()
                        for num in range(random.randint(10,15)):
                            crystal.activate_particle_list.append([[crystal.rect.x + 50, crystal.rect.y + 50], random.randint(5,10), random.randint(0,360)*np.pi/180, random.randint(10,20), random.randint(1,5)])
                        allow = 1
                else:
                    crystal.proximity = False

    #check the game_over variable
    if game_over_index >= 0:
        level = game_over_index
        reset_level()
        #load in level data and create world
        if path.exists(get_level_data_path(level)):
            pickle_in = open(get_level_data_path(level), 'rb')
            world_data = pickle.load(pickle_in)
            world.__init__(level)
            reset_grass()
            moving_plat_class.__init__()
            liquid = motion()
            reset_torches()
        if path.exists(get_level_data_path(level, '_bg')):
            pickle_in_bg = open(get_level_data_path(level, '_bg'), 'rb')
            bg_data = pickle.load(pickle_in_bg)
        if path.exists(get_level_data_path(level, '_front')):
            pickle_in_front = open(get_level_data_path(level, '_front'), 'rb')
            front_data = pickle.load(pickle_in_front)
            pickle_in_front.close()
        game_over_index = -1
    
    for event in pygame.event.get():
        #keyboard presses
        if event.type == pygame.KEYDOWN:
            button_col = 0
            button_row = 0
            if event.key == pygame.K_UP:
                level += 1
                if level > 5:
                    level = 5
                scroll = 0
                pending_scroll_dx = 0
                reset_level()
                #load in level data and create world
                if path.exists(get_level_data_path(level)):
                    pickle_in = open(get_level_data_path(level), 'rb')
                    world_data = pickle.load(pickle_in)
                    pickle_in_bg = open(get_level_data_path(level, '_bg'), 'rb')
                    bg_data = pickle.load(pickle_in_bg)
                    pickle_in_bg.close()
                if path.exists(get_level_data_path(level, '_front')):
                    pickle_in_front = open(get_level_data_path(level, '_front'), 'rb')
                    front_data = pickle.load(pickle_in_front)
                    pickle_in_front.close()
                world.__init__(level)
                reset_grass()
                reset_torches()
                liquid = motion()
                moving_plat_class.__init__()
            elif event.key == pygame.K_DOWN:
                level -= 1
                if level < 0:
                    level = 0
                scroll = 0
                pending_scroll_dx = 0
                reset_level()
                #load in level data and create world
                if path.exists(get_level_data_path(level)):
                    pickle_in = open(get_level_data_path(level), 'rb')
                    world_data = pickle.load(pickle_in)
                    pickle_in_bg = open(get_level_data_path(level, '_bg'), 'rb')
                    bg_data = pickle.load(pickle_in_bg)
                    pickle_in_bg.close()
                    pickle_in_front = open(get_level_data_path(level, '_front'), 'rb')
                    front_data = pickle.load(pickle_in_front)
                    pickle_in_front.close()
                    world.__init__(level)
                    reset_grass()
                    reset_torches()
                    liquid = motion()
                    moving_plat_class.__init__()
            elif event.key == pygame.K_t:
                if grid_allow == 0:
                    grid_allow = 1
                else:
                    grid_allow = 0
            elif event.key == pygame.K_h:
                show_hitbox = not show_hitbox
            elif event.key == pygame.K_g:
                player.god_mode = not player.god_mode
            elif event.key == pygame.K_F3:
                show_debug_info = not show_debug_info
            elif event.key == pygame.K_BACKQUOTE:
                melee_allow += 1
                if melee_allow >= 2:
                    melee_allow = 0
            elif event.key == pygame.K_r and potion_class.potion <= 2 and player.health < player.max_health:
                potion_class.heal = True
            elif event.key == pygame.K_RIGHT:
                button_page = 1
            elif event.key == pygame.K_LEFT:
                button_page = 0
            elif event.key == pygame.K_x:
                #save world data
                pickle_out = open(get_level_data_path(level), 'wb')
                pickle.dump(world_data, pickle_out)
                pickle_out.close()
                pickle_out_bg = open(get_level_data_path(level, '_bg'), 'wb')
                pickle.dump(bg_data, pickle_out_bg)
                pickle_out_bg.close()
                pickle_out_front = open(get_level_data_path(level, '_front'), 'wb')
                pickle.dump(front_data, pickle_out_front)
                pickle_out_front.close()
                reset_grass()
                reset_torches()
            elif event.key == pygame.K_z:
                #load world data
                if path.exists(get_level_data_path(level)):
                    scroll = 0
                    pending_scroll_dx = 0
                    pickle_in = open(get_level_data_path(level), 'rb')
                    reset_level()
                    world_data = pickle.load(pickle_in)
                    world.__init__(level)
                    player = Player(screen_width/2 - scroll, screen_height -400)
                    liquid = motion()
                    pickle_in.close()
                    pickle_in_bg = open(get_level_data_path(level, '_bg'), 'rb')
                    bg_data = pickle.load(pickle_in_bg)
                    pickle_in_bg.close()
                    pickle_in_front = open(get_level_data_path(level, '_front'), 'rb')
                    front_data = pickle.load(pickle_in_front)
                    pickle_in_front.close()
                    reset_grass()
                    reset_torches()
                    moving_plat_class.__init__()
                    shop_class.enter_shop = False
                    shop_class.collide_shop = False
                    shop_class.allow = True
            elif event.key == pygame.K_l:
                fps = 10
            elif event.key == pygame.K_k:
                fps = 60
            elif event.key == pygame.K_c:
                pause_class = pause.Pause(screen, keys_list)
                key_list = pause_class.update()
            elif event.key == pygame.K_ESCAPE:
                run = False
            elif event.key == keys_list[5] and shop_class.collide_shop == True:
                if shop_class.enter_shop == True:
                    shop_class.enter_shop = False
                    shop_class.allow = True
                else:
                    shop_class.enter_shop = True
        if event.type == pygame.KEYUP:
            pass
    if level == 0:
        end = time.time()
        #print(end - start)
        lag_time += end - start
        lag_counter += 1

    if show_hitbox:
        pygame.draw.rect(screen, (0, 255, 0), player.rect, 2)
        for enemy in enemy_group:
            pygame.draw.rect(screen, (255, 255, 0), enemy.rect, 2)
        for hitbox in hitbox_group:
            pygame.draw.rect(screen, (255, 0, 0), hitbox.rect, 2)

    probe.mark('present')
    display.present(screen)
    probe.end_frame(scroll)

    #advance the camera only once the whole frame has been drawn
    scroll += pending_scroll_dx
    scroll_speed = pending_scroll_dx
    pending_scroll_dx = 0
# print("Average FPS Is: ")
# print(lag_counter / lag_time)
probe.report(tile_size)
pygame.quit()
