import numpy as np
import random
from server_functions import get_item_spawn_chance
from netgame_img import wall_tile_list,test_item_dict,all_obj_img_dict

# Class for randomly generating items in a map  
class ItemGen:
    def __init__(self,map_mat,room_loc):
        self.map_mat = map_mat
        self.room_loc = room_loc
        # Actual number of object is max - 1
        self.max_item_per_room = 5
        self.chance_for_zero_item = 1
        self.max_armor_per_room = 3
        self.chance_for_zero_armor = 1
        self.max_weapon_per_room = 8
        self.chance_for_zero_weapon = 1
        self.item_loc = {'item':[], 'chest':[], 'head':[], 'legs':[], 'weapon':[], 'charm':[]}
        self.armor_type = ['chest','head','legs']
        self.y_num,self.x_num = np.shape(room_loc)[0:2]
        self.generate()

    # Generate items, armor, etc
    def generate(self):
        self.gen_items()
        self.gen_armor()
        self.gen_weapon()

    # Generate items randomly in rooms
    def gen_items(self):
        list_of_num, item_chance = get_item_spawn_chance(self.max_item_per_room, self.chance_for_zero_item)
        # Keep track of all the objects so objects don't overlap one another
        self.obj_only_loc = []
        for j in range(self.y_num):
            for i in range(self.x_num):
                room_rect = list(self.room_loc[j,i])
                # If the room is not 1x1, there is a chance for items to spawn
                if (room_rect[2],room_rect[3]) != (1,1):
                    num_items = np.random.choice(list_of_num, p=item_chance)
                    # Get the items that will spawn in beforehand. numpy library has a function for this. Add one since the size is short 1
                    item_list = list(np.random.randint(low=0,high=len(test_item_dict['item']),size=num_items+1))
                    # Start while loop that keeps running until all items are able to spawn in
                    while num_items >= 0:
                        rand_x = np.random.randint(room_rect[2]) + room_rect[0]
                        rand_y = np.random.randint(room_rect[3]) + room_rect[1]
                        if (self.map_mat[rand_y,rand_x] not in wall_tile_list) and ((rand_x,rand_y) not in self.obj_only_loc):
                            self.item_loc['item'].append((rand_x,rand_y,item_list[num_items]))
                            self.obj_only_loc.append((rand_x,rand_y))
                            num_items -= 1

    # Generate armor randomly in rooms
    def gen_armor(self):
        list_of_num, armor_chance = get_item_spawn_chance(self.max_armor_per_room, self.chance_for_zero_armor)
        for j in range(self.y_num):
            for i in range(self.x_num):
                room_rect = list(self.room_loc[j,i])
                # If the room is not 1x1, there is a chance for items to spawn
                if (room_rect[2],room_rect[3]) != (1,1):
                    num_armor = np.random.choice(list_of_num, p=armor_chance)
                    # Get the armor that will spawn in beforehand. numpy library has a function for this. Add one since the size is short 1
                    armor_list = list(np.random.randint(low=0,high=1,size=num_armor+1))
                    # Get the type of armor as a list as well
                    armor_type_list = [np.random.choice(self.armor_type) for i in range(num_armor+1)]
                    # Start while loop that keeps running until all items are able to spawn in
                    while num_armor >= 0:
                        rand_x = np.random.randint(room_rect[2]) + room_rect[0]
                        rand_y = np.random.randint(room_rect[3]) + room_rect[1]
                        if (self.map_mat[rand_y,rand_x] not in wall_tile_list) and ((rand_x,rand_y) not in self.obj_only_loc):
                            self.item_loc[armor_type_list[num_armor]].append((rand_x,rand_y,armor_list[num_armor]))
                            self.obj_only_loc.append((rand_x,rand_y))
                            num_armor -= 1

    # Generate weapons randomly in rooms
    def gen_weapon(self):
        list_of_num, weapon_chance = get_item_spawn_chance(self.max_weapon_per_room, self.chance_for_zero_weapon)
        for j in range(self.y_num):
            for i in range(self.x_num):
                room_rect = list(self.room_loc[j,i])
                # If the room is not 1x1, there is a chance for items to spawn
                if (room_rect[2],room_rect[3]) != (1,1):
                    num_weapon = np.random.choice(list_of_num, p=weapon_chance)
                    # Get the weapon that will spawn in beforehand. numpy library has a function for this. Add one since the size is short 1
                    # weapon_list = list(np.random.randint(low=0,high=len(all_obj_img_dict['weapon']),size=num_weapon+1))
                    weapon_list = list(np.random.randint(low=0,high=2,size=num_weapon+1))
                    # Start while loop that keeps running until all items are able to spawn in
                    while num_weapon >= 0:
                        rand_x = np.random.randint(room_rect[2]) + room_rect[0]
                        rand_y = np.random.randint(room_rect[3]) + room_rect[1]
                        if (self.map_mat[rand_y,rand_x] not in wall_tile_list) and ((rand_x,rand_y) not in self.obj_only_loc):
                            self.item_loc['weapon'].append((rand_x,rand_y,weapon_list[num_weapon]))
                            self.obj_only_loc.append((rand_x,rand_y))
                            num_weapon -= 1