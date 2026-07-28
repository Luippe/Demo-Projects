import asyncio
import numpy as np
import netgame_img as img
tile_size = 64
center = (320, 256)

def get_path_vars():
    # Gap between room and path
    line_min_gap = 1
    max_pathx_remove = 2
    max_pathy_remove = 2
    return line_min_gap,max_pathx_remove,max_pathy_remove

def get_dead_end_vars():
    # Number of dead ends and their min,max length
    num_dead_end = 8
    max_dead_end = 10
    min_dead_end = 5
    return num_dead_end,max_dead_end,min_dead_end

def get_room_vars():
    # Minimum size of each room. Min gap between rooms*2
    min_height = 6
    min_width = 6
    room_min_gap = 3
    max_dummy_rooms = 3
    return min_height,min_width,room_min_gap,max_dummy_rooms

# Send data to all clients. data is given as an encoded string
# func is the function that specifies how you send the data
async def send_to_all(func,data,connection_list):
    task_list = [func(connection_list[i],data) for i in range(len(connection_list))]
    await asyncio.wait_for(asyncio.gather(*task_list),10)

# Function for sending data to a specified client
async def send_to(writer,data):
    writer.write(data)
    await writer.drain()

# Function for sending map data to a specified client
async def send_map(writer,data_string):
    for strings in data_string:
        writer.write(strings)
    await writer.drain()

# Place objects on map 
def place_object(obj,room_loc,map_mat,replace_tile,entrance_list,wall_tile_num=img.wall_tile_list):
    x_size,y_size = np.shape(obj)
    m,n,_ = np.shape(room_loc)
    map_mat_backup = np.copy(map_mat)
    while True:
        # Get a room to spawn the object. This room cannot be a 1x1 room
        room_m = np.random.randint(m)
        room_n = np.random.randint(n)
        room_rect = room_loc[room_m,room_n]
        rand_x = np.random.randint(room_rect[2]) + room_rect[0]
        rand_y = np.random.randint(room_rect[3]) + room_rect[1]
        check_mat = map_mat[rand_y:rand_y+y_size,rand_x:rand_x+x_size]
        # Check if there is enough room to spawn in the object using .all() and making sure all the tiles are replaceable before actually replacing them
        if ((room_rect[2],room_rect[3]) != (1,1)) and ((check_mat == replace_tile).all() == True):
            map_mat[rand_y:rand_y+y_size,rand_x:rand_x+x_size] = obj
            if check_entrance_block(entrance_list,map_mat) == False:  # Check if entrance is blocked
                break
            else:   # If it is, go to start of while loop with the original map_mat
                map_mat = np.copy(map_mat_backup)

# Check if the entrance is blocked. Returns True if it is blocked
def check_entrance_block(entrance_list,map_mat,wall_tile_num=img.wall_tile_list):
    for loc in entrance_list:
        if map_mat[loc[1],loc[0]] in wall_tile_num:
            return True
    return False

# Calculate the number of item spawn chance per room. Feed the chance for 0 items to spawn, as well as the max number of items per room
def get_item_spawn_chance(max_item_per_room, chance_for_zero_item):
    list_of_num = list(range(max_item_per_room))
    choices = list_of_num[1:]
    one_over_chance = [1/x for x in choices]
    chance = (1 - chance_for_zero_item)/(sum(one_over_chance))
    item_chance = [chance*x for x in one_over_chance]
    item_chance.insert(0,chance_for_zero_item)
    return list_of_num, item_chance

