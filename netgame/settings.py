import netgame_img as img
import pygame
from pygame.locals import *
import time
from functions import draw_text, scale_and_center_word

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (200, 25, 25)
LIGHT_BLUE = (147, 207, 240)
GREEN = (144, 201, 120)
DARK_GREY = (105, 105, 105)
YELLOW = (242,242,73)
LIGHT_GREY = (188, 186, 184)


class Settings:
    def __init__(self,canvas,mini_map):
        self.option_width = 140
        self.option_height = 35
        self.setting_list = img.setting_list
        self.setting_screen = pygame.Surface((512,384))
        self.option_screen = pygame.Surface((480,350))
        self.open_settings = False
        self.clicked = False
        self.curr_tab = 0
        self.scrolly = 0
        self.tot_scroll = 0
        self.swap_keys = False
        self.swap_num = 0
        self.curr_name = 'Game'
        self.game_dict = {'Mini Map': {'Small':3,'Medium':6},
                          'Cursor': {'Default':False, 'Custom':True}}
        self.control_dict = {'Open Settings':K_p,
                             'Open Inventory':K_e,
                             'Interact':K_f,
                             'Change Direction':K_LCTRL,
                             'Toggle Highlight':K_LSHIFT}
        self.other_dict = {'Player Color': {'White':WHITE, 'Light Blue':LIGHT_BLUE, 'Red':RED},
                           'Item Color': {'Yellow':YELLOW, 'Red':RED, 'White':WHITE, 'Light Blue':LIGHT_BLUE},
                           'Full Screen': {'Off':False, 'On':True}}
        self.tab_names = {'Game': self.game_dict,
                          'Control': self.control_dict,
                          'Others': self.other_dict}
        self.tab_keys = list(self.tab_names.keys())
        self.keys = list(self.game_dict.keys())
        self.curr_selected = [0] * len(self.game_dict)
        self.tab_rect_list = [pygame.Rect(96 + 16 + 168*i,96 + 16, 152, 64) for i in range(3)]
        self.option_rect_list = [pygame.Rect(450, 2*96 + 50*i, self.option_width, self.option_height) for i in range(len(self.keys))]
        self.option_region_rect = pygame.Rect(96 + 16,2*96, 480, 272)
        # Create a list that saves the settings
        self.save_options_list = []
        for name in self.tab_names.keys():
            self.save_options_list.append([0] * len(self.tab_names[name]))
        # Draw text onto settings
        self.main_screen = canvas.screen
        self.mini_map = mini_map
        self.canvas = canvas
        self.draw_options()

    def update(self):
        # start = time.time()
        self.setting_screen.fill((0,0,0))
        if self.swap_keys == False:
            self.change_settings()
        else:
            self.change_controls()
        self.draw_settings()
        # end = time.time()
        # print(end - start)

    # Draw the options onto thes settings screen, then draw the settings onto the main screen
    def draw_settings(self):
        self.setting_screen.blit(self.option_screen,(16,96 + self.tot_scroll))
        self.setting_screen.blit(self.setting_list[self.curr_tab],(0,0))
        self.main_screen.blit(self.setting_screen,(96,96))

    # Update the settings if the player changes them
    def change_settings(self):
        x,y = pygame.mouse.get_pos()
        self.tot_scroll += 10*self.scrolly
        # see if player clicks on anything to change the settings
        for num,obj in enumerate(self.option_rect_list):    
            obj.y += 10*self.scrolly
            # If player changes the settings
            if (obj.collidepoint((x,y))) and (self.option_region_rect.collidepoint((x,y))) and (pygame.mouse.get_pressed()[0] == 1) and (self.clicked == False):
                self.clicked = True
                try:
                    name = self.keys[num]
                    self.curr_selected[num] += 1
                    select = self.tab_names[self.curr_name][name].keys()
                    if self.curr_selected[num] >= len(select):
                        self.curr_selected[num] = 0
                except:
                    pass
                # assign values to change the settings
                if self.curr_tab == 0:
                    self.mini_map.scale_by = list(self.tab_names["Game"]["Mini Map"].values())[self.curr_selected[0]]
                    self.canvas.custom_cursor = list(self.tab_names["Game"]["Cursor"].values())[self.curr_selected[1]]
                    pygame.mouse.set_visible(not self.canvas.custom_cursor)
                elif self.curr_tab == 1:
                    self.swap_keys = True
                    self.swap_num = num
                elif self.curr_tab == 2:
                    self.mini_map.player_color = list(self.tab_names["Others"]["Player Color"].values())[self.curr_selected[0]]
                    self.mini_map.item_color = list(self.tab_names["Others"]["Item Color"].values())[self.curr_selected[1]]
                    if num == 2:
                        pygame.display.toggle_fullscreen()
                self.draw_options()
            elif (pygame.mouse.get_pressed()[0] == 0) and (self.clicked == True):
                self.clicked = False
        self.scrolly = 0

        # See which tab the player is currently on
        for num,obj in enumerate(self.tab_rect_list):
            if (obj.collidepoint((x,y))) and (pygame.mouse.get_pressed()[0] == 1) and self.curr_tab != num:
                self.curr_tab = num
                self.tot_scroll = 0
                self.keys = list(self.tab_names[self.tab_keys[num]].keys())
                self.curr_name = self.tab_keys[num]
                self.curr_selected = self.save_options_list[num]
                self.option_rect_list = [pygame.Rect(450, 2*96 + 50*i, self.option_width, self.option_height) for i in range(len(self.keys))]
                self.draw_options()
                
    # Function for changing controls
    def change_controls(self):
        # Check for a key press to assign new controls
        pygame.draw.rect(self.main_screen,RED,(self.option_rect_list[self.swap_num]),5)
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                # Check if there is already an assigned key. if so, do not assign key and give player an error message
                option_values = list(self.tab_names["Control"].values())
                if event.key not in option_values:
                    self.tab_names["Control"][list(self.tab_names["Control"].keys())[self.swap_num]] = event.key
                    self.swap_keys = False
                    self.draw_options()

    # Draw the options onto screen. Only draw when something changes
    def draw_options(self):
        self.option_screen.fill(LIGHT_GREY)
        for num,obj in enumerate(self.option_rect_list[0:len(self.keys)]):
            # Move the settings if we scroll
            pygame.draw.rect(self.option_screen,DARK_GREY,(obj.x - 96 - 16,obj.y - 2*96 - 10*self.tot_scroll, self.option_width, self.option_height))
            name = self.keys[num]
            # Check if we are changing controls or on a different tab
            select = self.tab_names[self.curr_name][name]
            if isinstance(select,int) == True:
                word = pygame.key.name(select)
                center_x,center_y,letter_size = scale_and_center_word(word,280,64)
                draw_text(word,WHITE,obj.x - 96 - 16 + center_x,obj.y - 2*96  - 10*self.tot_scroll,self.option_screen,letter_size)
            else:
                select = list(select.keys())
                center_x,center_y,letter_size = scale_and_center_word(select[self.curr_selected[num]],280,64)
                draw_text(select[self.curr_selected[num]],WHITE,obj.x - 96 - 16 + center_x,obj.y - 2*96 - 10*self.tot_scroll,self.option_screen,letter_size)
            draw_text(name,WHITE,0,obj.y - 2*96 - 10*self.tot_scroll,self.option_screen,40)