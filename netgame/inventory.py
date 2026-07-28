import netgame_img as img
import pygame
from pygame.locals import *
import numpy as np
from items import all_name_dict, all_equippable_stats
from functions import draw_text,index_2d,fit_description_text
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (200, 25, 25)
YELLOW = (230,230,73)
tile_size = 64
w,h=(704,576)

# Create a class to display the inventory
class Inventory:
    def __init__(self, player, canvas, mini_map, control_dict, network, action):
        self.option_width, self.option_height = (120,30)    # Get text size to fit inside options
        self.inv_startx, self.inv_starty = (64,120)  # Get top left corner of the first slot w/respect to the inventory image
        self.inv_num_x, self.inv_num_y = (5,3)
        self.exit_tile = list(range(img.min_exit,img.max_exit_frame))
        self.inv_screen = pygame.Surface((700,500), SRCALPHA)       # Update this screen only if an item is dropped/pickedup to save performance
        self.detail_screen = pygame.Surface((700,500), SRCALPHA)    # Screen for drawing details such as the highlight when hovering over options and items
        self.option_screen = pygame.Surface((128,192), SRCALPHA)    # Open when right clicking an item
        self.description_screen = pygame.Surface((192,192), SRCALPHA)   # Open when opening the details for items
        self.description_img = img.item_description_list
        self.inv_img = img.inventory_list
        self.inv_img_width,self.inv_img_height = (self.inv_img[0].get_width(),self.inv_img[0].get_height())
        self.blit_x,self.blit_y = ((w - self.inv_img_width)//2, (h - self.inv_img_height)//2)
        self.test_item = img.test_item_dict
        self.armor_dict = img.armor_dict
        self.open_option = img.open_option_list
        self.item_select = img.item_select_list
        self.option_select = img.option_select_list
        self.equipment_icon_dict = img.equipment_icon_dict
        self.equipment_fade_dict = img.equipment_fade_dict
        self.option_words = ['Use', 'Equip', 'Drop', 'Give', 'Details']
        self.equip_words = ['Use', 'Unequip', 'Drop', 'Details']
        self.stats_words = ['None']
        self.all_words_dict = {0:self.option_words, 1:self.equip_words, 2:self.stats_words}
        self.tab_names = ['Items', 'Equipment', 'Stats']
        self.control_dict = control_dict
        self.description_screen.blit(self.description_img[0],(0,0))
        self.open_item = None
        self.curr_tab = 0
        self.option_rect = self.open_option[0].get_rect()
        self.description_rect = self.description_img[0].get_rect()
        self.open_inventory = False
        self.held = False
        self.clicked = False    # Sees if player right clicks an object to pull up options
        self.clicked_options = False    # Sees if option should stay opened. Prevents continuous clicks from occuring when opening descriptions
        self.drag_item = False
        self.open_description = False
        self.item_rect = []
        self.item_rect = [[pygame.Rect(self.blit_x + self.inv_startx + (16 + tile_size)*i,
                                      self.blit_y + self.inv_starty + (16 + tile_size)*j,
                                      tile_size,
                                      tile_size)
                                      for i in range(self.inv_num_x)] for j in range(self.inv_num_y)]
        self.tab_rect_list = [pygame.Rect(self.blit_x + 16 + 168*i,self.blit_y + 16, 152, 64) for i in range(3)]
        self.item_list = [[['item',1] for i in range(self.inv_num_x)] for j in range(self.inv_num_y)]
        for num in range(img.num_armor):
            for armor_name in ['head','chest','legs']:
                if (empty_slot := index_2d(self.item_list, ['item',1])) != (None,None):
                    self.item_list[empty_slot[0]][empty_slot[1]] = [armor_name,num]
        self.screen = canvas.screen
        self.canvas = canvas
        self.player = player
        self.action = action
        self.mini_map = mini_map
        self.network = network
        self.exit_loc = None
        self.description_text_size = 20
        self.stat_text_size = 15
        self.all_img_dict = img.all_obj_img_dict
        self.equip_num_x = 5
        self.equip_list = [['head',None],['chest',None],['legs',None],['weapon',None],['head',None]]
        self.equip_keys = ['head','chest','legs','weapon','head']
        self.equip_rect = [pygame.Rect(self.blit_x + self.inv_startx + (16 + tile_size)*i,
                                      self.blit_y + self.inv_starty,
                                      tile_size,
                                      tile_size)
                                      for i in range(self.equip_num_x)]
        self.armor_stat_keys = ['Defense', 'Attack', 'Special']
        self.stats_text = ['Attack', 'Defense']
        self.redraw_option(self.all_words_dict[0])
        self.redraw_inv_screen()

    # Update inventory if the inventory is opened
    def update_inventory(self,tiles_x,tiles_y):
        x,y = pygame.mouse.get_pos()
        self.detail_screen.fill((0,0,0,0))
        self.switch_tabs(x,y)
        if self.curr_tab == 0:
            self.item_functions(x,y)
            if self.clicked == True:
                self.draw_options()
                self.select_item_options(tiles_x,tiles_y,x,y)
        elif self.curr_tab == 1:
            self.equip_functions(x,y)
            if self.clicked == True:
                self.draw_options()
                self.select_equip_options(tiles_x,tiles_y,x,y)
        if self.open_description == True:
            self.draw_description()
        if self.clicked == False:
            self.open_description = False
            self.clicked_options = False
        self.draw_inventory()

    # Draw the inventory onto screen
    def draw_inventory(self):
        self.screen.blit(self.inv_screen,(self.blit_x,self.blit_y))
        self.screen.blit(self.detail_screen,(self.blit_x,self.blit_y))

    # Draw item descriptions
    def draw_description(self):
        # Make sure the description box fits on screen
        if (self.option_rect.x + self.option_rect.width + self.description_rect.width + 96) <= w:
            self.detail_screen.blit(self.description_screen, (self.option_rect.x + self.option_rect.width,self.option_rect.y))
        else:
            self.detail_screen.blit(self.description_screen, (self.option_rect.x - self.description_rect.width,self.option_rect.y))

    # Draw the options onto screen
    def draw_options(self):
        self.detail_screen.blit(self.option_screen, (self.option_rect.x,self.option_rect.y))

    # See which tab the player is currently on. Redraw the options and inventory screen when changing
    def switch_tabs(self,x,y):
        for num,obj in enumerate(self.tab_rect_list):
            if (obj.collidepoint((x,y))) and (pygame.mouse.get_pressed()[0] == 1) and self.curr_tab != num:
                self.curr_tab = num
                self.clicked = False
                self.redraw_option(self.all_words_dict[num])
                self.redraw_inv_screen()

    # If player clicks outside the option rect, close the option
    def clicked_out(self,x,y):
        if (pygame.mouse.get_pressed()[0] == 1) and not self.option_rect.collidepoint((x,y)):
            self.clicked = False

    # Function for managing inventory
    def item_functions(self,x,y):
        for j in range(self.inv_num_y):
            for i in range(self.inv_num_x):
                val = self.item_list[j][i]
                if val[1] != None:
                    if self.item_rect[j][i].collidepoint((x,y)) and self.clicked == False:
                        self.detail_screen.blit(self.item_select[0],(self.inv_startx - 4 + 80*i, self.inv_starty - 4 + 80*j))
                        # Draw name of item when hovering over an item
                        draw_text(all_name_dict[val[0]][val[1]],BLACK,x-self.blit_x,y-self.blit_y-30,self.detail_screen,30)
                        if (pygame.mouse.get_pressed()[2] == 1) and self.clicked == False:
                            self.clicked = True
                            self.item_y,self.item_x = (j,i)
                            self.option_rect.x,self.option_rect.y = (128 + 80*i,120 + 80*j) # Get top left corner of first item slot
                            self.option_rect_list = [pygame.Rect(self.option_rect.x + 4, self.option_rect.y + self.option_height*j + 4, self.option_width, self.option_height) for j in range(len(self.option_words))]

    # Function for managing equippable items
    def equip_functions(self,x,y):
        for i in range(self.equip_num_x):
            val = self.equip_list[i]
            if val[1] != None:
                if self.equip_rect[i].collidepoint((x,y)) and self.clicked == False:
                    self.detail_screen.blit(self.item_select[0],(self.inv_startx - 4 + 80*i, self.inv_starty - 4))
                    # Draw name of equipment when hovering over an equipment
                    draw_text(all_name_dict[val[0]][val[1]],BLACK,x-self.blit_x,y-self.blit_y-30,self.detail_screen,30)
                    if (pygame.mouse.get_pressed()[2] == 1) and self.clicked == False:
                        self.clicked = True
                        self.equipment_x = i
                        self.option_rect.x,self.option_rect.y = (128 + 80*i,120) # Get top left corner of first item slot
                        self.option_rect_list = [pygame.Rect(self.option_rect.x + 4, self.option_rect.y + self.option_height*j + 4, self.option_width, self.option_height) for j in range(len(self.equip_words))]
    
    def stats_functions(self,x,y):
        pass
    
    # Function for when player clicks on item options
    def select_item_options(self,tiles_x,tiles_y,x,y):
        x,y = (x - self.blit_x, y - self.blit_y)
        self.clicked_out(x,y)
        for num, obj in enumerate(self.option_rect_list):
            if obj.collidepoint((x,y)):
                self.detail_screen.blit(self.option_select[0], (obj.x,obj.y))
                # If player clicks on any of the options, do the following
                # Use (num == 0)
                # Equip (num == 1)
                # Drop (num == 2)
                # Give (num == 3)
                # Details (num == 4)
                if (pygame.mouse.get_pressed()[0] == 1) and self.clicked_options == False:
                    self.clicked_options = True
                    if num == 0:
                        self.clicked = False
                    elif num == 1:
                        self.clicked = False
                        if (equip_name := self.item_list[self.item_y][self.item_x][0]) in self.equip_keys:   # Check if it is a equippable item
                            
                            equip_index = [i for i in range(self.equip_num_x) if self.equip_list[i][0] == equip_name][0] # Find the index with correct equipment name
                            if self.equip_list[equip_index][1] == None:   # Equip item
                                self.equip_list[equip_index] = self.item_list[self.item_y][self.item_x]
                                self.item_list[self.item_y][self.item_x] = ['Empty',None]
                            else:   # If there is already an equipped item, swap the item in the inventory with it
                                temp_store = self.item_list[self.item_y][self.item_x]
                                self.item_list[self.item_y][self.item_x] = self.equip_list[equip_index]
                                self.equip_list[equip_index] = temp_store
                            self.update_player_stats()
                            self.redraw_inv_screen()
                    elif num == 2:    # Check if there is already an item or an exit underneath you before dropping it
                        self.drop_obj(tiles_x,tiles_y,self.item_list,self.item_x,self.item_y,['Empty',None])
                    elif num == 3:
                        pass
                    elif num == 4:  # Draw description onto description screen. Make sure the words fit into the screen
                        self.open_description = True
                        self.description_screen.blit(self.description_img[0],(0,0))
                        self.description_screen = fit_description_text(self.item_list[self.item_y][self.item_x], self.description_text_size, self.stat_text_size, self.description_screen, 192 - 5, self.equip_keys)
                elif (pygame.mouse.get_pressed()[0] == 0) and self.open_description == True:
                    self.clicked_options = False

    # Function for when player clicks on equipment options
    def select_equip_options(self,tiles_x,tiles_y,x,y):
        x,y = (x - self.blit_x, y - self.blit_y)
        self.clicked_out(x,y)
        for num, obj in enumerate(self.option_rect_list):
            if obj.collidepoint((x,y)):
                self.detail_screen.blit(self.option_select[0], (obj.x,obj.y))
                # If player clicks on any of the options, do the following
                # Use (num == 0)
                # Unequip (num == 1)
                # Drop (num == 2)
                # Details (num == 3)
                if (pygame.mouse.get_pressed()[0] == 1) and self.clicked_options == False:
                    self.clicked_options = True
                    if num == 0:
                        self.clicked = False
                    elif num == 1:
                        self.clicked = False
                        if (empty_slot := index_2d(self.item_list, ['Empty',None])) != (None,None):
                            val = self.equip_list[self.equipment_x]
                            self.item_list[empty_slot[0]][empty_slot[1]] = [val[0],val[1]]
                            self.equip_list[self.equipment_x][1] = None
                            self.update_player_stats()
                            self.redraw_inv_screen()
                    elif num == 2:
                        self.drop_obj(tiles_x,tiles_y,self.equip_list,self.equipment_x,None,None)
                    elif num == 3:
                        self.open_description = True
                        self.description_screen.blit(self.description_img[0],(0,0))
                        self.description_screen = fit_description_text(self.equip_list[self.equipment_x], self.description_text_size, self.stat_text_size, self.description_screen, 192 - 5, self.equip_keys)
                elif (pygame.mouse.get_pressed()[0] == 0) and self.open_description == True:
                    self.clicked_options = False

    # Drop whatever object you selected
    def drop_obj(self,tiles_x,tiles_y,mat,i,j,replace):
        check_obj_mat = [obj[0:2] for sublist in list(self.canvas.item_loc.values()) for obj in sublist]  # Get the location of all the items
        if ((tiles_x,tiles_y) not in check_obj_mat) and ((tiles_y,tiles_x) not in self.exit_loc):
            self.clicked = False
            if j == None: # If the given matrix is 1D (equipment tab)
                val = mat[i]
            else:   # If the given matrix is 2D (item tab)
                val = mat[j][i]
            data = {"type":val[0],"id":self.network.id,val[0]:[tiles_x,tiles_y,val[1]]}
            self.network.item_change = data
            if j == None: # If the given matrix is 1D (equipment tab)
                mat[i][1] = replace
            else:   # If the given matrix is 2D (item tab)
                mat[j][i] = replace
            self.redraw_inv_screen()

    # Check if player has picked up and item
    def check_pickup(self,tiles_x,tiles_y):
        # Pickup item when key Interact key is pressed. picked up items appear in inventory, filling up from top left
        for obj_type in self.canvas.item_loc.keys():
            for loc in self.canvas.item_loc[obj_type]:
                if [tiles_x,tiles_y] == [loc[0],loc[1]]:
                    if (empty_slot := index_2d(self.item_list, ['Empty',None])) != (None,None):   # Find an empty spot to put the item in
                        data = {"type":obj_type,"id":self.network.id,obj_type:[tiles_x,tiles_y,loc[2]]} # Send object data to server
                        self.item_list[empty_slot[0]][empty_slot[1]] = [obj_type, loc[2]]
                        self.network.item_change = data
                        self.redraw_inv_screen()
                        return True
        return False

    # Draw text and option onto screen beforehand
    def redraw_option(self,words):
        self.option_screen.blit(self.open_option[0],(0,0))
        for num in range(len(words)):
            draw_text(words[num], WHITE, 10, 10 + self.option_height*num, self.option_screen, 30)

    # Redraw the inventory when it updates
    def redraw_inv_screen(self):
        self.inv_screen.blit(self.inv_img[self.curr_tab],(0,0))
        if self.curr_tab == 0:
            for j in range(self.inv_num_y):
                for i in range(self.inv_num_x):
                    val = self.item_list[j][i]
                    if val != ['Empty',None]:
                        self.inv_screen.blit(self.all_img_dict[val[0]][val[1]],(self.inv_startx + (16 + tile_size)*i,self.inv_starty + (16 + tile_size)*j))
        elif self.curr_tab == 1:
            for num, val in enumerate(self.equip_list):
                if val[1] != None:
                    self.inv_screen.blit(self.all_img_dict[val[0]][val[1]], (self.inv_startx + (16 + tile_size)*num, self.inv_starty))
        elif self.curr_tab == 2:
            for num, text in enumerate(self.stats_text):
                if text == 'Attack':
                    draw_text(text + f': {self.player.base_attack + self.player.attack}', WHITE, 100, 100 + 30*num, self.inv_screen, 30)
                elif text == 'Defense':
                    draw_text(text + f': {self.player.base_defense + self.player.defense}', WHITE, 100, 100 + 30*num, self.inv_screen, 30)
    
    # Update player stats when changing equipments
    def update_player_stats(self):
        self.player.attack = 0
        self.player.defense = 0
        self.action.attack_linear = [[(1,0)]]
        self.action.attack_diag = [[(1,-1)]]
        self.action.special_data_list = []
        for val in self.equip_list:
            if val[1] != None:
                stat_dict = all_equippable_stats[val[0]][val[1]]
                self.player.attack += stat_dict['Attack']
                self.player.defense += stat_dict['Defense']
                if val[0] == 'weapon':  # If the equipment is a weapon
                    self.action.attack_linear = stat_dict['Area Linear']
                    self.action.attack_diag = stat_dict['Area Diag']
                    self.action.max_damage_delay = stat_dict['delay']
                if stat_dict['Special'] != None:    # If there is a special attribute to the equipment. [name, img, special type, special data, cooldown, max cooldown]
                    self.action.special_data_list.append([all_name_dict[val[0]][val[1]],self.equipment_icon_dict[val[0]][val[1]],self.equipment_fade_dict[val[0]][val[1]],stat_dict['Special'],stat_dict['Special Data'],stat_dict['Special CD'],stat_dict['Special CD']])
        self.action.redraw_special()
