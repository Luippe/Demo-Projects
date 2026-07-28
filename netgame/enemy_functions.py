import numpy as np
import random
import pygame
import time
tile_size = 64
center = (320, 256)

# Create a list with enemy position. return [name of enemy, list of spawning locations, group of enemies, position of enemies in dict]
# group_mat is m by n. group_names contains the name of each enemy
def random_enemy_spawn(room_loc,map_mat,walkable_tile,spawn_vars_list,player_spawn_room,entrance_list):
    dirn_list = [(0,-1),(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1)]
    enemy_spawn_loc = []
    loc = []
    m,n = np.shape(room_loc)[0:2]
    group_mat = [[pygame.sprite.Group() for i in range(n)] for j in range(m)] #2d list of pygame sprite groups
    group_names = [] # 2d list of dict that will be used to send enemy's position data
    # For each group of enemies, get their spawn points
    for vars in spawn_vars_list:
        min_per_room,max_per_room,group,func = vars
        group_names.append(group)
        enemy_id = 0
        for j in range(m):
            for i in range(n):
                room_rect = list(room_loc[j,i])
                # If the room is not 1x1, there is a chance for enemies to spawn.
                # The number of spawns is between min_per_room <= num < max_per_room
                # Use while loop to make sure it spawns. Only spawn in places that are walkable
                # Enemies cannot spawn in the same room as the players. add --> ( and ((i,j) != player_spawn_room))
                if ((room_rect[2],room_rect[3]) != (1,1)) and ((i,j) != player_spawn_room):
                    num_enemies = np.random.randint(min_per_room,max_per_room)
                    for k in range(num_enemies):
                        while True:
                            rand_x = np.random.randint(room_rect[2]) + room_rect[0]
                            rand_y = np.random.randint(room_rect[3]) + room_rect[1]
                            # Make sure enemies only spawn on walkable tiles, and make sure enemies don't spawn on top of eachother
                            if (map_mat[rand_y,rand_x] in walkable_tile) and ((rand_x,rand_y) not in loc) and ((rand_x,rand_y) not in entrance_list):
                                enemy_spawn_loc.append((rand_x,rand_y,group))
                                loc.append((rand_x,rand_y))
                                rand_direction = random.choice(dirn_list)
                                group_mat[j][i].add(func(rand_x,rand_y,j,i,rand_direction,room_rect,enemy_id))
                                enemy_id += 1
                                break
    return group_mat,group_names

def get_view_mat(room_loc,room_list,mat):
    room_mat = room_list[room_loc[0]][room_loc[1]]
    return mat[room_mat[1]-1:room_mat[1]+room_mat[3]+1,room_mat[0]-1:room_mat[0]+room_mat[2]+1]

# Check to see if the enemy can move diagonally
def allow_diag_move(view_mat,tiles_x,tiles_y,x_direc,y_direc):
    x_upper = tiles_x + 1
    x_lower = tiles_x
    y_upper = tiles_y + 1
    y_lower = tiles_y
    if x_direc > 0:
        x_upper += x_direc
    else:
        x_lower += x_direc
    if y_direc > 0:
        y_upper += y_direc
    else:
        y_lower += y_direc
    checking = [j for sub in view_mat[y_lower:y_upper,x_lower:x_upper] for j in sub]
    return 0 in checking

# Get the first diagonal movement from sol_path. Used by enemy pathfinding
def choose_first_diag(sol_path):
    # Check to see if sol_path has elements inside. If not, return an empty list
    if len(sol_path) > 0:
        all_diag = [x for x in sol_path if (x[0] != 0 and x[1] != 0)]
        # Check if there even is a diagonal movement because the path can just be straight
        if len(all_diag) > 0:
            return all_diag[-1]
        else:
            return sol_path[-1]
    else:
        return []

# Change direction of enemy towards a nearby player
def change_direction(obj_pos, enemy_pos, direc):
    dirn_list = [(0,-1),(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1)]
    # If we are already in the range of the player, just correct the direction
    for player_pos in obj_pos:
        direction = tuple([x - y for x,y in zip(player_pos,enemy_pos)])   # Subtract player position and enemy position to get direction
        if direction in dirn_list:
            return direction
    return direc

# Get position of players with respect to the room. Used for pathfinding. view_mat has border of 0 with thickness 1.
# obj_center and thickness is (0,0) for enemy and 1 by default. Returns a 2D list if obj_pos is 2D, and 1D if obj_pos is 1D
def get_pos_view(obj_pos, room_x, room_y, obj_center=(0,0), thickness=1):
    obj_view_pos = []
    try:
        m,n = np.shape(obj_pos)
        for pos in obj_pos:
            tile_x = (-pos[0] + obj_center[0])//tile_size - room_x + thickness
            tile_y = (-pos[1] + obj_center[1])//tile_size - room_y + thickness
            obj_view_pos.append([tile_x,tile_y])
    except:
        tile_x = (-obj_pos[0] + obj_center[0])//tile_size - room_x + thickness
        tile_y = (-obj_pos[1] + obj_center[1])//tile_size - room_y + thickness
        obj_view_pos = [tile_x,tile_y]
    return obj_view_pos

# Find the closest path. Goal is to get to the goal_pos
def enemy_pathfind_all(goal_pos, players_id, current_pos, view_mat, stationary_enemy):
    start = time.time()
    pos_id_dict = {tuple(goal_pos[i]):players_id[i] for i in range(len(players_id))}
    start_pos = current_pos
    curr_start_val = 0
    sorted_index = 0
    path_pos = []
    sol_path = []
    priority_queue = [[1000,0]]
    checked_pos = [current_pos]
    direc_path = [current_pos]
    next_path = [current_pos]
    all_sol_path = []
    sum_queue = [[1000,0]]
    # Set scale equal to zero to do a flood fill algorithm
    scale = 0
    # If enemy is already close to player, then only change its directions
    # next_to_player, goal_pos = change_direction(goal_pos, pos_id_dict, current_pos)
    # Loop until we get a path towards given destination
    while len(goal_pos) > 0:
        path_pos.append(current_pos)
        x_curr = current_pos[0]
        y_curr = current_pos[1]
        for i in range(-1,2):
            for j in range(-1,2):
                next_pos = [x_curr+i, y_curr+j]
                # Use try except block here since we know we get an error at (view_mat[y_curr+j,x_curr+i] != 0) because we check a tile outside
                # the bounds. When that happens, ignore that tile
                try:
                    if (next_pos in path_pos) == False and (view_mat[y_curr+j,x_curr+i] != 0) and ([x_curr+i, y_curr+j] not in stationary_enemy) == True:
                        if (i != 0) and (j != 0) and allow_diag_move(view_mat,x_curr,y_curr,i,j) == True:
                            pass
                        else:
                            goal_dist = scale*np.linalg.norm([a_i - b_i for a_i, b_i in zip(next_pos, goal_pos)])
                            start_dist = np.linalg.norm([a_i - b_i for a_i, b_i in zip(next_pos, current_pos)]) + curr_start_val
                            if (next_pos in checked_pos) == False:
                                checked_pos.append(next_pos)
                                priority_queue.append([goal_dist + start_dist,start_dist])
                                direc_path.append(current_pos)
                                next_path.append(next_pos)
                                sum_queue.append([goal_dist + start_dist,start_dist])
                            else:
                                comparing_index = checked_pos.index(next_pos)
                                if priority_queue[comparing_index][0] > goal_dist + start_dist:
                                    priority_queue[comparing_index] = [goal_dist + start_dist,start_dist]
                                    sum_queue[comparing_index] = [goal_dist + start_dist,start_dist]
                                    path_index = next_path.index(next_pos)
                                    direc_path[path_index] = current_pos
                                    next_path[path_index] = next_pos
                except Exception as error:
                    # print(error)
                    pass
        checked_pos.remove(current_pos)
        priority_queue.remove(priority_queue[sorted_index])
        sorted_index = priority_queue.index(min(priority_queue, key = lambda x: x[0]))
        curr_start_val = priority_queue[sorted_index][1]
        current_pos = checked_pos[sorted_index]
        # See if current position has reached any of the goals
        if current_pos in goal_pos:
            sol_index = goal_pos.index(current_pos)
            next_loc = goal_pos[sol_index]
            sol_tiles = [next_loc]
            goal_pos.remove(current_pos)
            sum_path_values = 0
            while True:
                place = next_path.index(next_loc)
                next_loc = direc_path[place]
                sum_path_values += sum_queue[place][0]
                next_value = sum_queue[place][0]
                sol_tiles.append(next_loc)
                if sol_tiles[-1] == start_pos:
                    sol_tiles = np.array(sol_tiles)
                    sol_path = [tuple(sol_tiles[num]-sol_tiles[num+1]) for num in range(len(sol_tiles)-1)]
                    all_sol_path.append([pos_id_dict[current_pos[0],current_pos[1]],sol_path,next_value,sum_path_values])
                    break
    end = time.time()
    # print(end-start)
    # Return the shortest path for all players, as well as the length of path, and the direction it must face if it is adjacent to a player
    return all_sol_path

# Get direction from differences between two adjacent
def direction_from_tiles(tile_1, tile_2):
    return (tile_1[0] - tile_2[0], tile_1[1] - tile_2[1])

# Check if all element in a list are specifically True. Returns False if any element is anything other than True
def check_if_all_true(turn_list):
    for turn in turn_list:
        if turn != True:
            return False
    return True
