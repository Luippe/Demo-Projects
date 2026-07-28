import numpy as np
import pickle
import random
import time
import itertools
from scipy.ndimage import label
import netgame_img as img
from item_gen import ItemGen
from server_functions import *
from enemy_functions import *
import asyncio
import pygame
from concurrent.futures import ThreadPoolExecutor
from game_enemy import Enemy
import object_matrix as om
from multiprocessing import Queue

tile_size = 64
center = (320, 256)
map_x,map_y = (112,64)


def matprint(mat, fmt="g"):
    col_maxes = [max([len(("{:"+fmt+"}").format(x)) for x in col]) for col in mat.T]
    for x in mat:
        for i, y in enumerate(x):
            print(("{:"+str(col_maxes[i])+fmt+"}").format(y), end="")
        print("")

# Class that has all the changeable parameters
class RandAlgorithm():
    def __init__(self):
        self.min_roomx = 3
        self.max_roomx = 4
        self.min_roomy = 2
        self.max_roomy = 3
        self.n = np.random.randint(self.min_roomx,self.max_roomx+1)
        self.m = np.random.randint(self.min_roomy,self.max_roomy+1)

# Class for randomly generating a traversable map
class MapGen():
    def __init__(self):
        rand_class = RandAlgorithm()
        self.m,self.n = (rand_class.m,rand_class.n)
        start = time.time()
        self.num_dead_end,self.max_dead_end,self.min_dead_end = get_dead_end_vars()
        self.line_min_gap,self.max_pathx_remove,self.max_pathy_remove = get_path_vars()
        self.min_height,self.min_width,self.room_min_gap,self.max_dummy_rooms = get_room_vars()
        self.wall_mat = 0
        self.left_wall = 1
        self.right_wall = 2
        self.bot_wall = 3
        self.top_wall = 4
        self.se_wall = 5
        self.sw_wall = 6
        self.ne_wall = 7
        self.nw_wall = 8
        self.path_vert = 9
        self.path_horz = 10
        self.top_corner = 11
        self.bot_corner = 12
        self.left_corner = 13
        self.right_corner = 14
        self.inner_mat = 15
        self.exit_tile = 18
        self.entrance_tile = 38
        self.map_mat = np.zeros((map_y,map_x), dtype=np.int8)
        self.bound = -1
        self.map_mat[0,:] = self.top_wall
        self.map_mat[-1,:] = self.bot_wall
        self.map_mat[:,0] = self.left_wall
        self.map_mat[:,-1] = self.right_wall
        self.chance_direc = 15
        self.spawn_list = []
        self.random_loc = []
        self.wall_loc = []
        self.entrance_dict = {}     # Location of entrance {(room x, room y):[(tile x, tile y),...]}
        self.entrance_block = []    # Location of tiles that are in front of the entrance. Spawning enemies and objects cannot block the entrance.
        self.stone_wall_num = [self.left_wall,self.right_wall,self.bot_wall,self.top_wall]
        self.stop_end = [self.inner_mat] + self.stone_wall_num
        self.gen_map(self.m,self.n)
        self.dead_end()
        self.set_walls()
        self.get_entrance(self.m,self.n)
        place_object(om.exit_obj,self.room_loc,self.map_mat,self.inner_mat,self.entrance_block)
        place_object(om.shrine_obj,self.room_loc,self.map_mat,self.inner_mat,self.entrance_block)
        # Set the floor to random floor tiles. Do this step last.
        num_ones = self.map_mat[self.map_mat == self.inner_mat]
        self.map_mat[self.map_mat == self.inner_mat] = random.choices(range(img.min_floor,img.max_floor), k=len(num_ones))
        end = time.time()
        # print(end-start)

    # Generate Map
    def gen_map(self,m,n):
        rand_list = []
        region_x = map_x//n - 2*self.room_min_gap
        region_y = map_y//m - 2*self.room_min_gap
        #determine number of 1x1 rooms. Max number of dummy rooms we can have is max_dummy_rooms - 1
        dummy_num = np.random.randint(self.max_dummy_rooms)
        room_x = np.random.randint(self.min_width,region_x,size=(m,n))
        room_y = np.random.randint(self.min_height,region_y,size=(m,n))
        # Find a room to spawn into
        spawn_i = np.random.randint(n)
        spawn_j = np.random.randint(m)
        self.spawn_room = (spawn_i,spawn_j)
        # Replace random rooms with dummy rooms with size 1x1
        while len(rand_list) < dummy_num:
            rand_i = np.random.randint(n)
            rand_j = np.random.randint(m)
            if [rand_i,rand_j] not in rand_list and [rand_i,rand_j] != [spawn_i,spawn_j]:
                rand_list.append([rand_i,rand_j])
                room_x[rand_j,rand_i] = 1
                room_y[rand_j,rand_i] = 1
        high_x = region_x - room_x
        high_y = region_y - room_y
        loc_x = np.random.randint(0,high_x)
        loc_y = np.random.randint(0,high_y)
        #put the rooms into their respective locations
        for j in range(m):
            for i in range(n):
                loc_x[j,i] += (region_x + 2*self.room_min_gap)*i + self.room_min_gap
                loc_y[j,i] += (region_y + 2*self.room_min_gap)*j + self.room_min_gap
                #replace map matrix with physical rooms
                x1 = loc_x[j,i]
                y1 = loc_y[j,i]
                x2 = room_x[j,i] + x1
                y2 = room_y[j,i] + y1
                height = range(y1,y2)
                width = range(x1,x2)
                #get location of all the walls (x,y,direc)
                left_loc = list(zip([x1] * len(height),height,[(-1,0)] * len(height)))
                right_loc = list(zip([x2] * len(height),height, [(1,0)] * len(height)))
                bot_loc = list(zip(width,[y2] * len(width),[(0,1)] * len(width)))
                top_loc = list(zip(width,[y1] * len(width), [(0,-1)] * len(width)))
                self.wall_loc += left_loc + right_loc + bot_loc + top_loc
                self.map_mat[y1:y2,x1:x2] = self.inner_mat
        self.spawn_list = [loc_x[spawn_j,spawn_i],loc_y[spawn_j,spawn_i],room_x[spawn_j,spawn_i],room_y[spawn_j,spawn_i]]
        self.spawn_room = (spawn_i,spawn_j)
        self.right_face = loc_x + room_x
        self.bot_face = loc_y + room_y
        self.left_face = loc_x
        self.top_face = loc_y
        self.room_loc = np.dstack((loc_x,loc_y,room_x,room_y))
        #create a backup of map_mat and wall_loc just in case if the removed path causes a break
        self.wall_loc_backup = self.wall_loc[:]
        self.map_mat_backup = np.copy(self.map_mat)
        #if there is a break in the map, create new path until it eventually works out
        self.check_connection(m,n)

    # Generate paths
    def path_gen(self,m,n):
        # Set 2 points between each adjacent room, and draw a straight line that connects the two
        dist_x = self.left_face[:,1:] - self.right_face[:,:-1] - self.line_min_gap
        dist_y = self.top_face[1:,:] - self.bot_face[:-1,:] - self.line_min_gap
        rand_distx = np.random.randint(self.line_min_gap,dist_x) + self.right_face[:,:-1]
        rand_disty = np.random.randint(self.line_min_gap,dist_y) + self.bot_face[:-1,:]
        room_height = self.bot_face - self.top_face
        room_width = self.right_face - self.left_face
        # Create random paths to remove from the map. separate horizontal and vertical paths
        x_coord,y_coord = (range(n),range(m))
        possible_xcoord = list(itertools.product(x_coord[0:-1],y_coord))
        possible_ycoord = list(itertools.product(x_coord,y_coord[0:-1]))
        num_remove_x = random.randint(0,self.max_pathx_remove)
        num_remove_y = random.randint(0,self.max_pathy_remove)
        remove_ycoord = random.sample(possible_ycoord,num_remove_y)
        remove_xcoord = random.sample(possible_xcoord,num_remove_x)
        # Create paths and do not make paths that were selected above
        for j in range(m):
            for i in range(n):
                right_rand = None
                bot_rand = None
                if (i,j) not in remove_xcoord:
                    right_rand = np.random.randint(room_height[j,i]) + self.top_face[j,i]
                if (i,j) not in remove_ycoord:
                    bot_rand = np.random.randint(room_width[j,i]) + self.left_face[j,i]
                try:
                    # Check if right_rand, left_rand, and rand_distx is 1D array
                    if (i+1 < n):
                        left_rand = np.random.randint(room_height[j,i+1]) + self.top_face[j,i+1]
                        sorted_pos = sorted([left_rand, right_rand])
                        # Two colinear lines
                        self.map_mat[right_rand, self.right_face[j,i]:rand_distx[j,i]] = self.inner_mat
                        self.map_mat[left_rand, rand_distx[j,i]:self.left_face[j,i+1]] = self.inner_mat
                        # One connector line
                        self.map_mat[sorted_pos[0]:sorted_pos[1]+1,rand_distx[j,i]] = self.inner_mat
                        # Remove adjacent walls from potential dead end locations
                        for offset in [-1,0,1]:
                            if (self.left_face[j,i+1], left_rand + offset, (-1,0)) in self.wall_loc:
                                self.wall_loc.remove((self.left_face[j,i+1], left_rand + offset, (-1,0)))
                            if (self.right_face[j,i], right_rand + offset, (1,0)) in self.wall_loc:
                                self.wall_loc.remove((self.right_face[j,i], right_rand + offset, (1,0)))
                except Exception as error:
                    pass
                try:
                    #Check if bot_rand, top_rand, and rand_disty is 1D array
                    if (j+1 < m):
                        top_rand = np.random.randint(room_width[j+1,i]) + self.left_face[j+1,i]
                        sorted_pos = sorted([top_rand, bot_rand])
                        # Two colinear lines
                        self.map_mat[self.bot_face[j,i]:rand_disty[j,i], bot_rand] = self.inner_mat
                        self.map_mat[rand_disty[j,i]:self.top_face[j+1,i], top_rand] = self.inner_mat
                        # One connector line
                        self.map_mat[rand_disty[j,i],sorted_pos[0]:sorted_pos[1]+1] = self.inner_mat
                        # Remove adjacent walls from potential dead end locations
                        for offset in [-1,0,1]:
                            if (top_rand + offset, self.top_face[j+1,i], (0,-1)) in self.wall_loc:
                                self.wall_loc.remove((top_rand + offset, self.top_face[j+1,i], (0,-1)))
                            if (bot_rand + offset, self.bot_face[j,i], (0,1)) in self.wall_loc:
                                self.wall_loc.remove((bot_rand + offset, self.bot_face[j,i], (0,1)))
                except Exception as error:
                    pass

    # Create random dead ends
    def dead_end(self):
        # Find number of dead ends it will create
        num_walls = np.random.randint(self.num_dead_end)
        direc_list = [(0,1), (0,-1), (1,0), (-1,0)]
        for num in range(num_walls):
            # Choose a random wall to start the path. but it cannot be near already made paths
            rand_start_index = np.random.randint(len(self.wall_loc))
            rand_start = self.wall_loc[rand_start_index]
            direc = rand_start[2]
            opp_direc = tuple(-1*x for x in direc)
            possible_direc = [loc for loc in direc_list if loc != direc and loc != opp_direc]
            self.map_mat[rand_start[1],rand_start[0]] = self.inner_mat
            max_step = np.random.randint(self.min_dead_end,self.max_dead_end)
            step = 0
            step_forward = 0
            # Remove adjacent walls from potential dead end locations
            try:
                self.wall_loc.remove(rand_start)
                for loc in possible_direc:
                    self.wall_loc.remove((rand_start[0] + loc[0], rand_start[1] + loc[1], direc))
            except:
                pass
            rand_start = list(rand_start)
            # For each start location, start doing a random walk in a line
            while (step <= max_step):
                step += 1
                step_forward += 1
                # Choose a random direction to move
                rand_start[0] += direc[0]
                rand_start[1] += direc[1]
                try:
                    if (self.map_mat[rand_start[1],rand_start[0]] not in self.stop_end):
                        self.map_mat[rand_start[1],rand_start[0]] = self.inner_mat
                    else:
                        break
                    if (self.check_nearby(direc_list,rand_start[0],rand_start[1]) == True):
                        break
                except:
                    break
                # Change direction once in a while
                if (np.random.randint(self.chance_direc) == 0) and (step_forward >= 2):
                    # Can't use np.random.choice since possible_direc is 2-D. There is always only 2 possible ways
                    opp_direc = tuple(-1*x for x in direc)
                    possible_direc = [loc for loc in direc_list if loc != direc and loc != opp_direc]
                    direc = possible_direc[np.random.randint(2)]
                    step_forward = 0

    # Check for nearby paths so we don't have paths right next to eachother. checks 4 tiles and if 2 or more them are inner_mat, then break
    def check_nearby(self,direc_list,x,y):
        # Check up down left right tiles. you will always have a walkable tile behind you so find a different walkable tile
        counter = 0
        for loc in direc_list:
            if self.map_mat[y+loc[1], x+loc[0]] == self.inner_mat:
                counter += 1
            if counter == 2:
                return True
        return False

    # Create walls
    def set_walls(self):
        wall_mat = np.zeros_like(self.map_mat)
        # Check where specific types of walls are
        for j in range(1,map_y):
            for i in range(1,map_x):
                if self.map_mat[j,i] == self.wall_mat:
                    if self.map_mat[j,i-1] == self.inner_mat:
                        wall_mat[j,i] += 1
                    if self.map_mat[j,i+1] == self.inner_mat:
                        wall_mat[j,i] += 1
                    if self.map_mat[j+1,i] == self.inner_mat:
                        wall_mat[j,i] += 1
                    if self.map_mat[j-1,i] == self.inner_mat:
                        wall_mat[j,i] += 1

        # Fill in those walls with its corresponding tile number
        for j in range(1,map_y):
            for i in range(1,map_x):
                if wall_mat[j,i] == 1:
                    if self.map_mat[j,i-1] == self.inner_mat:
                        self.map_mat[j,i] = self.right_wall
                    elif self.map_mat[j,i+1] == self.inner_mat:
                        self.map_mat[j,i] = self.left_wall
                    elif self.map_mat[j+1,i] == self.inner_mat:
                        self.map_mat[j,i] = self.top_wall
                    elif self.map_mat[j-1,i] == self.inner_mat:
                        self.map_mat[j,i] = self.bot_wall
                elif wall_mat[j,i] == 2:
                    if (self.map_mat[j-1,i] == self.inner_mat) and (self.map_mat[j+1,i] == self.inner_mat):
                        self.map_mat[j,i] = self.path_horz
                    elif (self.map_mat[j,i-1] == self.inner_mat) and (self.map_mat[j,i+1] == self.inner_mat):
                        self.map_mat[j,i] = self.path_vert
                    elif self.map_mat[j-1,i] == self.inner_mat:
                        if self.map_mat[j,i+1] == self.inner_mat:
                            self.map_mat[j,i] = self.ne_wall
                        elif self.map_mat[j,i-1] == self.inner_mat:
                            self.map_mat[j,i] = self.nw_wall
                    elif self.map_mat[j+1,i] == self.inner_mat:
                        if self.map_mat[j,i+1] == self.inner_mat:
                            self.map_mat[j,i] = self.se_wall
                        elif self.map_mat[j,i-1] == self.inner_mat:
                            self.map_mat[j,i] = self.sw_wall
                elif wall_mat[j,i] == 3:
                    if (self.map_mat[j,i-1] != self.inner_mat):
                        self.map_mat[j,i] = self.left_corner
                    elif (self.map_mat[j,i+1] != self.inner_mat):
                        self.map_mat[j,i] = self.right_corner
                    elif (self.map_mat[j+1,i] != self.inner_mat):
                        self.map_mat[j,i] = self.bot_corner
                    elif (self.map_mat[j-1,i] != self.inner_mat):
                        self.map_mat[j,i] = self.top_corner

    # Check if the paths are correctly connected. else make a new map again
    def check_connection(self,m,n):
        while True:
            self.path_gen(m,n)
            label_array, num_feature = label(self.map_mat)
            # If the rooms are correctly connected, break from while loop. Else, make a new path
            if num_feature == 2:
                break
            else:
                print("RETRYING!")
                self.map_mat = np.copy(self.map_mat_backup)
                self.wall_loc = self.wall_loc_backup[:]

    # Get entrance of each room. This is used to make sure nothing blocks the entrance when spawning objects in.
    # Additionally, place a entrance tile right before going into the room
    def get_entrance(self,m,n):
        for j in range(m):
            for i in range(n):
                # Get list of tiles corresponding to the walls of each room. Top and left list needs special treatment due to how they were obtained
                bot_tiles = self.map_mat[self.bot_face[j,i], self.room_loc[j,i][0]:self.room_loc[j,i][0]+self.room_loc[j,i][2]]
                top_tiles = self.map_mat[self.top_face[j,i]-1, self.room_loc[j,i][0]:self.room_loc[j,i][0]+self.room_loc[j,i][2]]
                left_tiles = self.map_mat[self.room_loc[j,i][1]:self.room_loc[j,i][1]+self.room_loc[j,i][3], self.left_face[j,i]-1]
                right_tiles = self.map_mat[self.room_loc[j,i][1]:self.room_loc[j,i][1]+self.room_loc[j,i][3], self.right_face[j,i]]
                # Check to see if self.inner_mat (the entrance) exists
                bot_indices = [k+self.room_loc[j,i][0] for k in range(len(bot_tiles)) if bot_tiles[k] == self.inner_mat]
                top_indices = [k+self.room_loc[j,i][0] for k in range(len(top_tiles)) if top_tiles[k] == self.inner_mat]
                left_indices = [k+self.room_loc[j,i][1] for k in range(len(left_tiles)) if left_tiles[k] == self.inner_mat]
                right_indices = [k+self.room_loc[j,i][1] for k in range(len(right_tiles)) if right_tiles[k] == self.inner_mat]
                # Replace the entrance tile with something. Has entries in [x,y]. Some index requires a -1 since the top and left walls are not
                # included when indexing. Make sure entrance tiles don't spawn in 1x1 rooms.
                room_rect = self.room_loc[j,i]
                if ((i,j) != self.spawn_room) and ((room_rect[2],room_rect[3]) != (1,1)):
                    self.entrance_dict.update({(i,j):[]})
                    for loc in bot_indices:
                        self.entrance_dict[(i,j)].append((loc,self.bot_face[j,i]))
                        self.entrance_block.append((loc,self.bot_face[j,i]-1))
                        self.map_mat[self.bot_face[j,i],loc] = self.entrance_tile
                    for loc in top_indices:
                        self.entrance_dict[(i,j)].append((loc,self.top_face[j,i]-1))
                        self.entrance_block.append((loc,self.top_face[j,i]))
                        self.map_mat[self.top_face[j,i]-1,loc] = self.entrance_tile
                    for loc in left_indices:
                        self.entrance_dict[(i,j)].append((self.left_face[j,i]-1,loc))
                        self.entrance_block.append((self.left_face[j,i],loc))
                        self.map_mat[loc,self.left_face[j,i]-1] = self.entrance_tile
                    for loc in right_indices:
                        self.entrance_dict[(i,j)].append((self.right_face[j,i],loc))
                        self.entrance_block.append((self.right_face[j,i]-1,loc))
                        self.map_mat[loc,self.right_face[j,i]] = self.entrance_tile
        
# Get all the class required to obtain the map details. Returns a tuple of class
def make_map():
    start = time.time()
    global map_class,item_class
    map_class = MapGen()
    item_class = ItemGen(map_class.map_mat, map_class.room_loc)
    end = time.time()
    print(end-start)

# Function for creating the map data
def dump_data(map_class,item_class,id_list):
    global len_list,map_string,spawn_string,room_string,item_string
    map_string = pickle.dumps(map_class.map_mat)
    spawn_string = pickle.dumps(map_class.spawn_list)
    room_string = pickle.dumps(map_class.room_loc)
    item_string = pickle.dumps(item_class.item_loc)
    id_string = pickle.dumps(id_list)
    # Get length of all the strings that will be sent
    len_list = [len(map_string),len(spawn_string),len(room_string),len(item_string),len(id_string)]
    len_list = [str(x) for x in len_list]
    len_list = ','.join(len_list)
    len_list = str(len(len_list)) + ',' + len_list
    len_list = str.encode(len_list)
    return len_list,map_string,spawn_string,room_string,item_string,id_string

class ServerNetwork:
    def __init__(self, ipv="0.0.0.0", port=5555):
        self.ipv = ipv
        self.port = port
        self.enemy_data = []
        self.pos = []
        self.item = []
        self.players = []
        self.connection_list = []
        self.addr_list = {}
        self.id_list = []
        self.test_addr = [('12.3.456.789',1234),('12.545.6453',8888),('12.545.9453',8887),('12.545.6753',8868)]
        self.player_turn = []
        self.player_in_combat = []
        self.player_action = []
        self.ready_check = []
        self.enemy_action = Queue()
        make_map()
        global enemy_class
        enemy_class = Enemy(self,map_class)
        enemy_class.spawn_enemies(map_class.entrance_block)

    # Handle player position data
    async def pos_data(self,data,player_id,writer):
        self.pos[player_id] = data
        position = [x['pos'] for x in self.pos if x != data]
        room = [x['room'] for x in self.pos if x != data]
        health = [x['health'] for x in self.pos if x != data]
        defense = [x['defense'] for x in self.pos if x != data]
        ready = [x['ready check'] for x in self.pos if x != data]
        if data['turn'] == True:
            self.player_turn[player_id] = None
        elif (self.player_turn[player_id] == None) and (data['turn'] == False):
            self.player_turn[player_id] = not data['turn']  # Put in False if the player is able to move. If the player cannot move, put in True
        elif (self.player_turn[player_id] == False) and (data['turn'] == False):
            self.player_turn[player_id] = 10
            writer.write(pickle.dumps({'type':'turn','turn':True}))
            await writer.drain()
        if data['in combat'] is not self.player_in_combat[player_id]:
            writer.write(pickle.dumps({'type':'enemy','data':'in combat','in combat':self.player_in_combat[player_id]}))
            await writer.drain()
        reply = {'type':'pos','pos':position,'room':room,'health':health,'defense':defense,'ready check':ready}
        reply = pickle.dumps(reply)
        writer.write(reply)
        await writer.drain()

    # Handle player and enemy actions
    async def action_data(self,data,raw_data,player_id,writer):
        if data['action'] == 'attack':
            for num in range(len(self.connection_list)):
                if num != player_id:
                    self.player_action[num].put_nowait(raw_data)
            self.enemy_action.put_nowait(data)
        writer.write(raw_data)
        await writer.drain()

    # Handle item data
    async def item_data(self,data,raw_data,player_id,writer):
        item_name = data['type']
        item_loc = tuple(data[item_name])
        for num in range(len(self.connection_list)):
            if num != player_id:
                self.item[num].put_nowait(raw_data)
        if item_loc in item_class.item_loc[item_name]:
            item_class.item_loc[item_name].remove(item_loc)
        else:
            item_class.item_loc[item_name].append(item_loc)
        writer.write(raw_data)
        await writer.drain()

    # Send initial sets of data and initialize some lists when a player joins
    async def send_init_data(self,writer,id_int):
        # Send initial data to the clients
        writer.write(str(id_int).encode())
        await send_map(writer,(dump_data(map_class,item_class,self.id_list)))
        for num in range(len(self.players)):
            self.players[num] = pickle.dumps({"type":'conn','change':"add",'id':id_int})
        self.item.append(Queue())
        self.players.append(None)
        self.player_turn.append(None)
        self.player_in_combat.append(None)
        self.enemy_data.append(Queue())
        self.player_action.append(Queue())
        self.ready_check.append(None)
        self.pos.append({"type":"pos","id":id_int,"pos":None,'room':None,'turn':None,'in combat':None,'health':None,'defense':None,'ready check':None})

    # Main function for handling client
    async def handle_client(self, reader, writer):
        addr = random.choice(self.test_addr)
        self.test_addr.remove(addr)
        # addr = writer.get_extra_info('peername')
        addr_keys = list(self.addr_list.keys())
        if addr[0] not in addr_keys:
            self.addr_list.update({addr[0]:len(self.addr_list)})
            id_int = self.addr_list[addr[0]]
        else:
            id_int = self.addr_list[addr[0]]
        self.id_list.append(id_int)
        print(f"New connection from {addr} with ID: {id_int}")
        self.connection_list.append(writer)
        await self.send_init_data(writer,id_int)

        try:
            while raw_data := await reader.read(2048):
                data = pickle.loads(raw_data)
                player_id = self.id_list.index(data['id'])
                # Handle data given from outside source (not from player)
                if self.player_action[player_id].empty() == False:
                    writer.write(self.player_action[player_id].get_nowait())
                    await writer.drain()
                elif self.item[player_id].empty() == False:
                    writer.write(self.item[player_id].get_nowait())
                    await writer.drain()
                elif self.players[player_id] != None:
                    writer.write(self.players[player_id])
                    await writer.drain()
                    self.players[player_id] = None
                elif self.enemy_data[player_id].empty() == False:
                    writer.write(pickle.dumps(self.enemy_data[player_id].get_nowait()))
                    await writer.drain()
                # Handle sending main data
                elif data['type'] == 'pos':
                    await self.pos_data(data,player_id,writer)
                elif data['type'] == 'action':
                    await self.action_data(data,raw_data,player_id,writer)
                elif data['type'] in ('item', 'chest', 'head', 'legs', 'weapon'):
                    await self.item_data(data,raw_data,player_id,writer)
                elif data['type'] == 'map':  # Create new map and send the data to the client
                    # First, send the raw_data to all clients so they know the data is coming
                    # Then send all the map data
                    make_map()
                    enemy_class.load_new_map(map_class)
                    await send_to_all(send_to,raw_data,self.connection_list)
                    await send_to_all(send_map,(dump_data(map_class,item_class,self.id_list)), self.connection_list)
        finally:
            remove_index = self.connection_list.index(writer)
            self.connection_list.remove(writer)
            id_remove = self.id_list[remove_index]
            print(f'Disconnecting ID: {id_remove}')
            self.players.pop(remove_index)
            self.pos.pop(remove_index)
            self.item.pop(remove_index)
            self.ready_check.pop(remove_index)
            self.player_turn.pop(remove_index)
            self.test_addr.append(addr)
            for num in range(len(self.connection_list)):
                self.players[num] = pickle.dumps({"type":'conn','change':"remove",'id':remove_index})
            self.id_list.remove(id_remove)
            writer.close()
            await writer.wait_closed()

    # Start server when client joins
    async def get_clients(self):
        server = await asyncio.start_server(
            self.handle_client, self.ipv, self.port
        )
        print(f"Server listening on {self.ipv}:{self.port}")
        async with server:
            await server.serve_forever()

    # Create a thread that handles the enemies.
    async def main(self):
        loop = asyncio.get_event_loop()
        self.task = asyncio.wait([asyncio.create_task(self.get_clients()),
                             loop.run_in_executor(ThreadPoolExecutor(), enemy_class.update, loop)],return_when=asyncio.FIRST_COMPLETED)
        try:
            await self.task
        except asyncio.CancelledError:
            print("Server Shutting Down")

if __name__ == "__main__":
    network = ServerNetwork()
    asyncio.run(network.main(),debug=True)
