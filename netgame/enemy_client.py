import netgame_img as img
import pygame
tile_size = 64
from functions import random_shake

# Class for mainly drawing enemy and identifying their locations
class Enemy:
    def __init__(self,canvas,network,player,mini_map_class,particles,health_class):
        self.scrollx = 0
        self.scrolly = 0
        self.screen = canvas.screen
        self.enemy_img = img.enemy_img_dict
        self.enemy_pos = {}
        self.enemy_names = []
        self.player = player
        self.mini_map_class = mini_map_class
        self.scroll_velx,self.scroll_vely = (8,8)
        self.shake_list = []
        self.particles = particles
        self.health_class = health_class

    # Draw all enemies. Animate them smoothly
    def draw(self):
        self.mini_map_class.enemy_screen.fill((0,0,0,0))
        for name in self.enemy_names:
            for loc in self.enemy_pos[name]:
                scale = self.mini_map_class.scale
                self.player.other_obj_pos.append([loc[4],loc[5]])
                scrollx, scrolly, prev_scrollx, prev_scrolly, rectx, recty, direction, facing = loc
                if (scrollx,scrolly) != (prev_scrollx, prev_scrolly):
                    loc[2] += self.scroll_velx*direction[0]
                    loc[3] += self.scroll_vely*direction[1]
                else:
                    loc[-2] = loc[-1] 
                pygame.draw.circle(self.mini_map_class.enemy_screen,self.mini_map_class.enemy_color,(scale*(loc[2])//tile_size + scale/2,
                                                                                           scale*(loc[3])//tile_size + scale/2),3)                                                        
                enemy_center = [loc[2] + self.player.scrollx, loc[3] + self.player.scrolly]
                if len(self.shake_list) > 0:
                    for enemy in self.shake_list:
                        if enemy[0] == (loc[2],loc[3]): # If the location matches, shake the enemy on that tile
                            enemy_center[0] += enemy[1][0][0]
                            enemy_center[1] += enemy[1][0][1]
                            enemy[1].pop(0)
                            if enemy[1] == []:  # If the shake ends
                                self.shake_list.remove(enemy)
                        else:   # If there are no enemy on that tile, remove the shake
                            self.shake_list.remove(enemy)    
                        self.screen.blit(self.enemy_img[name][loc[-2]],enemy_center)
                self.screen.blit(self.enemy_img[name][loc[-2]],enemy_center)

    # Take damage for the enemy
    def enemy_take_damage(self,data):
        self.health = []
        for enemy in data:
            damage = enemy[3]
            self.health.append(enemy[2])
            if damage > 0:
                self.shake_list.append([(enemy[0],enemy[1]), random_shake(-20,20,-20,20)])
                self.particles.add_damage_particles(self.player.scrollx + enemy[0],self.player.scrolly + enemy[1])
                self.health_class.get_damage_number_surface(damage, self.player.scrollx + enemy[0], self.player.scrolly + enemy[1])

