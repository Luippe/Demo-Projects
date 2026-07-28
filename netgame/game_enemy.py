from enemy_functions import *
import time
import asyncio
import pygame
import netgame_img as img
import enemies
import random
import threading
clock = pygame.time.Clock()

class Enemy():
    def __init__(self,network,map_class):
        self.pos = network.pos
        self.id_list = network.id_list
        self.room_loc = map_class.room_loc
        self.map_mat = map_class.map_mat
        self.player_spawn_room = map_class.spawn_room
        self.player_turn = network.player_turn
        self.network = network
        self.wall_tile_num = img.wall_tile_list
        self.wall_mat = [[element not in self.wall_tile_num for element in row] for row in self.map_mat]
        self.wall_mat = np.array(self.wall_mat,dtype=int)
        self.enemy_action = network.enemy_action
        self.map_lock = threading.Lock()
        pygame.init()

    def update(self,loop):
        run = True
        while run:
            with self.map_lock:
                self.update_enemies()

    def room_exists(self,room_loc):
        try:
            room_row,room_column = room_loc
            return (
                room_row is not None
                and room_column is not None
                and 0 <= room_row < len(self.group_mat)
                and 0 <= room_column < len(self.group_mat[room_row])
            )
        except (TypeError, ValueError, IndexError):
            return False

    def update_enemies(self):
        start = time.time()
        if len(self.id_list) > 0:
            player_in_list = []
            player_turn_list = {}
            for data in self.pos:   # For each player, find which room they are in
                if data['pos'] != None:
                    room_loc = data['room']   # m ,n for room location
                    player_id = self.id_list.index(data['id'])
                    if self.room_exists(room_loc):   # Make sure player is in a room on the current map
                        if (len(self.group_mat[room_loc[0]][room_loc[1]]) > 0): # If there are enemies inside the room
                            self.network.player_in_combat[player_id] = True
                            if (room_loc not in player_in_list):
                                player_in_list.append(room_loc)
                                player_turn_list.update({room_loc:{'ids':[data['id']],'turns':[self.network.player_turn[player_id]],'pos':[data['pos'][0:2]]}})  # room location:{ids list,turns list}
                            else:
                                player_turn_list[room_loc]['ids'].append(data['id'])
                                player_turn_list[room_loc]['turns'].append(self.network.player_turn[player_id])
                                player_turn_list[room_loc]['pos'].append(data['pos'][0:2])
                        else:
                            self.network.player_in_combat[player_id] = False
                    else:
                        self.network.player_in_combat[player_id] = False

            # If there is any items in queue for enemy_action
            if self.enemy_action.empty() == False:
                action = self.enemy_action.get_nowait()
                enemy_data = []
                for room_loc in player_in_list:
                    for enemy in self.group_mat[room_loc[0]][room_loc[1]]:
                        if action['action'] == 'attack':
                            enemy.take_damage(action['data'])
                            enemy_data.append([enemy.scrollx, enemy.scrolly, enemy.curr_health, enemy.damage_taken])
                            if enemy.curr_health == 0:  # If enemy is defeated
                                print('defeated')
                                if (len(self.group_mat[room_loc[0]][room_loc[1]]) == 1):    # If that is the last enemy in the room
                                    print('he')
                                    self.end_turn(room_loc,player_turn_list)
                                    enemy.kill()
                                    break
                                enemy.kill()
                for num in range(len(self.id_list)):
                    self.network.enemy_data[num].put_nowait({'type':'enemy','data':'health','health':enemy_data})

            # Check if all players in room have ended their turn and update enemy_data accordingly
            for room_loc in player_in_list:
                players_data = player_turn_list[room_loc]
                if check_if_all_true(players_data['turns']) == True: # If all the turns are equal to False (all player in that room has ended their turns)
                    # print('he',self.network.player_turn,player_in_list,player_turn_list,players_data)
                    start = time.time()
                    self.prev_pos(player_in_list)
                    self.update_room(room_loc,players_data)
                    self.get_enemy_data(player_in_list)
                    self.end_turn(room_loc,player_turn_list)
                    end = time.time()
                    print(end-start)


        end = time.time()
        # print(self.player_turn)
        # print(player_turn_list)

    # Spawns enemies onto the map. returns (x,y,group) and list of enemy names that spawned in
    def spawn_enemies(self,entrance_list):
        spawn_vars_list = self.get_enemies_spawn_vars()
        self.group_mat,self.group_names = random_enemy_spawn(self.room_loc,self.map_mat,img.walkable_list,spawn_vars_list,self.player_spawn_room,entrance_list)

    def load_new_map(self,map_class):
        with self.map_lock:
            for player_data in self.pos:
                player_data['pos'] = None
                player_data['room'] = (None,None)
            for player_id in range(len(self.network.player_in_combat)):
                self.network.player_in_combat[player_id] = False

            for group_row in self.group_mat:
                for group in group_row:
                    for enemy in group.sprites():
                        enemy.kill()

            self.group_mat = []
            self.group_names = []
            self.room_loc = map_class.room_loc
            self.map_mat = map_class.map_mat
            self.player_spawn_room = map_class.spawn_room
            self.wall_mat = [[element not in self.wall_tile_num for element in row] for row in self.map_mat]
            self.wall_mat = np.array(self.wall_mat,dtype=int)
            self.spawn_enemies(map_class.entrance_block)

                    
    # Variables for spawning enemies. [min spawn per room, max spawn per room, group name]
    def get_enemies_spawn_vars(self):
        goblin_vars = [1,2,'goblin',enemies.Goblin]
        ogre_vars = [1,2,'ogre',enemies.Ogre]
        # whisp_vars = [1,2,'whisp',enemies.Whisp]
        # return [goblin_vars,ogre_vars,whisp_vars]
        return [goblin_vars,ogre_vars]

    # Update all the enemies inside a given room. First find the shortest path using get_path, then make sure no collision happens with path_no_collision
    def update_room(self,room_loc,players_data):
        view_mat = get_view_mat(room_loc,self.room_loc,self.wall_mat)
        group_in_room = self.group_mat[room_loc[0]][room_loc[1]]
        group_move_to = []
        intersecting_tiles = {}
        stationary_enemy_list = []
        for enemy in group_in_room: # For enemy group in that room, see if the enemy is close to a player
            enemy.check_intersection(players_data['pos'],view_mat)
            # Add values of all intersecting tiles
            for tiles in enemy.intersecting_tiles:
                # If tile does not exist in dict, update it with {(x,y):val}. If there is a duplicate, add the values at the preexisting tile
                if tiles[0] not in list(intersecting_tiles.keys()):
                    intersecting_tiles.update({tiles[0]:tiles[1]})
                else:
                    intersecting_tiles[tiles[0]] += tiles[1]
        for enemy in group_in_room:
            enemy.decide()
        for enemy in group_in_room: # For all enemy with an action of 'Attack
            if enemy.action == 'Attack':
                stationary_enemy_list.append((enemy.scrollx,enemy.scrolly))
                enemy.move_to = [enemy, (enemy.rect.x, enemy.rect.y), 0]
        for enemy in group_in_room: # For all enemy with an action of 'Move Towards' find shortest path to player and decide which path to take
            if enemy.action == 'Move Towards':
                enemy.stationary_enemy = stationary_enemy_list
                enemy.get_path(players_data['ids'],players_data['pos'],view_mat)
                enemy.decide_path() # Decide which path to take
            
        
        # Start while loop which will keep looping until all collision between enemies has been handled
        until_no_collision = True
        while until_no_collision:
            temp_check_tile = []
            group_move_to = []
            for enemy in group_in_room:  # For enemy group in that room, find path without collision
                # Check if collision will occur with other enemies. Move the enemy accordingly
                    group_move_to.append(enemy.move_to)
            group_move_to.sort(key = lambda x: x[2])
            group_move_to.reverse()
            for move in group_move_to:
                if move[1] not in temp_check_tile:
                    temp_check_tile.append(move[1])
                    if len(temp_check_tile) == len(group_move_to):
                        until_no_collision = False
                else:
                    # If there is an overlap
                    if move[0].stationary == True:  # If the overlap has a stationary enemy
                        intersection_with_player = []
                        # See which tiles the stationary enemy can move on
                        for tiles in move[0].intersecting_tiles:
                            intersection_with_player.append([tiles[0], intersecting_tiles[tiles[0]]])
                        intersection_with_player.sort(key = lambda x: x[1])
                        # Move the stationary enemy to the tile with the least value in intersection_with_player
                        move[0].move_stationary(intersection_with_player[0])
                    else:   # If the overlap is caused by 2 enemies moving into 1 tile
                        stationary_enemy_list.append((move[1][0]*tile_size, move[1][1]*tile_size))
                        move[0].stationary_enemy = stationary_enemy_list
                        move[0].get_path(players_data['ids'],players_data['pos'],view_mat)
                        move[0].decide_path()
                        break
        for enemy in group_in_room:  # For enemy group in that room, find path without collision
            enemy.move_path()

    def check_end_turn(self,room_loc,player_turn_list):
        for player_room_id in player_turn_list[room_loc]['ids']:
            player_id = self.id_list.index(player_room_id)
            if self.network.player_turn[player_id] == False or self.network.player_turn[player_id] == None:
                return False    # It is not the enemy's turn
        return True # It is the enemy's turn

    # End turn for the enemies inside a given room_loc. If all enemies are dead, end combat
    def end_turn(self,room_loc,player_turn_list):
        for player_room_id in player_turn_list[room_loc]['ids']:
            player_id = self.id_list.index(player_room_id)
            self.network.player_turn[player_id] = False

    # See if all enemies are beaten. If so players should be able to move freely.
    def all_enemies_defeat(self,room_loc):
        if len(self.group_mat[room_loc[0]][room_loc[1]]) == 0:
            print("COMBAT END")

    # Get data of all the enemies
    def get_enemy_data(self,player_in_list):
        enemy_data = {}
        for room_loc in player_in_list:
            for enemy in self.group_mat[room_loc[0]][room_loc[1]]:
                if enemy.name not in list(enemy_data.keys()): # If the enemy name does not exit, add it to enemy_data
                    enemy_data.update({enemy.name:[[enemy.scrollx,enemy.scrolly,enemy.prev_scrollx,enemy.prev_scrolly,enemy.rect.x,enemy.rect.y,enemy.direction,enemy.facing]]})
                else:
                    enemy_data[enemy.name].append([enemy.scrollx,enemy.scrolly,enemy.prev_scrollx,enemy.prev_scrolly,enemy.rect.x,enemy.rect.y,enemy.direction,enemy.facing])
        for num in range(len(self.id_list)):
            self.network.enemy_data[num].put_nowait({'type':'enemy','data':'pos','pos':enemy_data})

    # Set previous prosition to current position
    def prev_pos(self,player_in_list):
        for room_loc in player_in_list:
            for enemy in self.group_mat[room_loc[0]][room_loc[1]]:
                enemy.prev_scrollx,enemy.prev_scrolly = (enemy.scrollx,enemy.scrolly)
