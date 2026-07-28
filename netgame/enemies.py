import pygame
from enemy_functions import *
tile_size = 64
center = (320, 256)

class Goblin(pygame.sprite.Sprite):
    def __init__(self,x,y,m,n,direc,room_rect,enemy_id):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x,y,1,1)
        self.rect.x,self.rect.y = (x,y)
        self.scrollx,self.scrolly = (x*tile_size,y*tile_size)
        self.prev_scrollx,self.prev_scrolly = (x*tile_size,y*tile_size)
        self.in_room = (m,n)
        self.room_x,self.room_y = (room_rect[0],room_rect[1])
        self.name = 'goblin'
        self.direction = direc
        self.facing = direc
        self.move_to_player = True
        self.max_health = 100
        self.curr_health = 100
        self.defense = 0
        self.damage_taken = 0
        self.group_move_to = []
        self.move_to = []
        self.stationary = False
        self.stationary_enemy = []
        self.action = ''
        self.id = enemy_id

    # Decide on what action to take
    def decide(self):
        if self.near_player == True:
            self.action = 'Attack'
            self.stationary = True
        else:
            self.action = 'Move Towards'

    # Get path to all players using A*
    def get_path(self,player_ids,players_pos,view_mat):
        # Find tile location of enemy and player based on the room
        player_view_pos = get_pos_view(players_pos,self.room_x,self.room_y,center)
        enemy_view_pos = get_pos_view([-self.scrollx,-self.scrolly],self.room_x,self.room_y)
        obj_view_pos = []
        # If there are any enemies that are stationary, find them
        for loc in self.stationary_enemy:
            obj_view_pos.append(get_pos_view([-loc[0],-loc[1]],self.room_x,self.room_y))
        # Return a dict with player id as key and path and the length of each path for the values. id:path
        self.all_path = enemy_pathfind_all(player_view_pos,player_ids,enemy_view_pos,view_mat,obj_view_pos)
        self.stationary_enemy = []
        
    # Decide what kind of path it will take
    def decide_path(self):
        if self.move_to_player == True:
            self.move_closest()

    # Move the given path
    def move_path(self):
        if self.stationary == False:
            self.scrolly += tile_size*self.direction[1]
            self.scrollx += tile_size*self.direction[0]
            tiles_x,tiles_y = (self.scrollx//tile_size, self.scrolly//tile_size)
            self.rect.x,self.rect.y = (tiles_x,tiles_y)

    # Move to the closest player
    def move_closest(self):
        # Sort based on the minimum path length, which is in index 1
        self.closest_path = min(self.all_path, key = lambda x: x[3])
        self.direction = self.closest_path[1][-1]
        self.facing = self.direction
        if len(self.closest_path[1]) > 1:
            self.stationary = False
            self.move_to = [self, ((self.scrollx+tile_size*self.direction[0])//tile_size, (self.scrolly+tile_size*self.direction[1])//tile_size), self.closest_path[2]]
        else:
            self.stationary = True
            self.move_to = [self, (self.rect.x,self.rect.y), 0]

    # Move if I am stationary. Set self.stataionary = False so we can move when move_path is called later.
    def move_stationary(self,move_to_data):
        enemy_view_pos = get_pos_view([-self.scrollx,-self.scrolly],self.room_x,self.room_y)
        move_to_tile = move_to_data[0]
        self.direction = (move_to_tile[0] - enemy_view_pos[0], move_to_tile[1] - enemy_view_pos[1])
        self.move_to = [self, ((self.scrollx+tile_size*self.direction[0])//tile_size, (self.scrolly+tile_size*self.direction[1])//tile_size), np.linalg.norm(self.direction)]
        self.stationary = False

    # Check surrounding for player
    def check_intersection(self,players_pos,view_mat):
        dirn_list = [(0,-1),(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1)]
        # Get all tiles around the player in a 3x3 area that the enemies can go to
        player_tile_loc = []
        player_view_pos = get_pos_view(players_pos,self.room_x,self.room_y,center)
        enemy_view_pos = get_pos_view([-self.scrollx,-self.scrolly],self.room_x,self.room_y)
        for pos in player_view_pos:
            for direc in dirn_list:
                tile_x = pos[0] + direc[0]
                tile_y = pos[1] + direc[1]
                if view_mat[tile_y,tile_x] != 0:
                    player_tile_loc.append((tile_x,tile_y))
            # If player is near enemy, set the self.near_player to True
            player_direction = (pos[0] - enemy_view_pos[0], pos[1] - enemy_view_pos[1])
            if player_direction in dirn_list:
                self.near_player = True
            else:
                self.near_player = False
        # Get all tiles around the enemy in a 3x3 area that the enemies can go to
        self.intersecting_tiles = []
        for direc in dirn_list:
            if (direc[0] != 0) and (direc[1] != 0) and (allow_diag_move(view_mat,enemy_view_pos[0],enemy_view_pos[1],direc[0],direc[1])) == True:
                pass
            else:
                tile_x = enemy_view_pos[0] + direc[0]
                tile_y = enemy_view_pos[1] + direc[1]
                val = np.linalg.norm(direc)
                if (view_mat[tile_y,tile_x] != 0) and ((tile_x,tile_y) in player_tile_loc):
                    self.intersecting_tiles.append([(tile_x,tile_y),val])       

    # Function for taking damage
    def take_damage(self,data):
        self.damage_taken = 0
        for area in data[1]:
            if (self.rect.x,self.rect.y) == area:
                self.damage_taken = sorted([1,data[0] - self.defense])[1]   # Make sure the damage is at least 1
                if self.curr_health > 0:
                    self.curr_health -= self.damage_taken
                if self.curr_health <= 0:
                    self.curr_health = 0

    # Face the player if the player is in range
    def face_player(self,players_pos):
        # See if I am close to a player in a 3x3 area
        player_view_pos = get_pos_view(players_pos,self.room_x,self.room_y,center)
        enemy_view_pos = get_pos_view([-self.scrollx,-self.scrolly],self.room_x,self.room_y)
        self.facing = change_direction(player_view_pos, enemy_view_pos, self.direction)


class Ogre(pygame.sprite.Sprite):
    def __init__(self,x,y,m,n,direc,room_rect,enemy_id):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x,y,1,1)
        self.rect.x,self.rect.y = (x,y)
        self.scrollx,self.scrolly = (x*tile_size,y*tile_size)
        self.prev_scrollx,self.prev_scrolly = (x*tile_size,y*tile_size)
        self.in_room = (m,n)
        self.name = 'ogre'
        self.direction = direc
        self.room_x,self.room_y = (room_rect[0],room_rect[1])
        self.move_to_player = True
        self.max_health = 100
        self.curr_health = 100
        self.defense = 0
        self.damage_taken = 0
        self.group_move_to = []
        self.move_to = []
        self.stationary = False
        self.stationary_enemy = []
        self.action = ''
        self.id = enemy_id

    # Decide on what action to take
    def decide(self):
        if self.near_player == True:
            self.action = 'Attack'
            self.stationary = True
        else:
            self.action = 'Move Towards'
            
    # Get path to all players using A*
    def get_path(self,player_ids,players_pos,view_mat):
        # Find tile location of enemy and player based on the room
        player_view_pos = get_pos_view(players_pos,self.room_x,self.room_y,center)
        enemy_view_pos = get_pos_view([-self.scrollx,-self.scrolly],self.room_x,self.room_y)
        obj_view_pos = []
        # If there are any enemies that are stationary, find them
        for loc in self.stationary_enemy:
            obj_view_pos.append(get_pos_view([-loc[0],-loc[1]],self.room_x,self.room_y))
        # Return a dict with player id as key and path and the length of each path for the values. id:path
        self.all_path = enemy_pathfind_all(player_view_pos,player_ids,enemy_view_pos,view_mat,obj_view_pos)
        self.stationary_enemy = []
        
    # Decide what kind of path it will take
    def decide_path(self):
        if self.move_to_player == True:
            self.move_closest()

    # Move the given path
    def move_path(self):
        if self.stationary == False:
            self.scrolly += tile_size*self.direction[1]
            self.scrollx += tile_size*self.direction[0]
            tiles_x,tiles_y = (self.scrollx//tile_size, self.scrolly//tile_size)
            self.rect.x,self.rect.y = (tiles_x,tiles_y)

    # Move to the closest player
    def move_closest(self):
        # Sort based on the minimum path length, which is in index 1
        self.closest_path = min(self.all_path, key = lambda x: x[3])
        self.direction = self.closest_path[1][-1]
        self.facing = self.direction
        if len(self.closest_path[1]) > 1:
            self.stationary = False
            self.move_to = [self, ((self.scrollx+tile_size*self.direction[0])//tile_size, (self.scrolly+tile_size*self.direction[1])//tile_size), self.closest_path[2]]
        else:
            self.stationary = True
            self.move_to = [self, (self.rect.x,self.rect.y), 0]

    # Move if I am stationary. Set self.stataionary = False so we can move when move_path is called later.
    def move_stationary(self,move_to_data):
        enemy_view_pos = get_pos_view([-self.scrollx,-self.scrolly],self.room_x,self.room_y)
        move_to_tile = move_to_data[0]
        self.direction = (move_to_tile[0] - enemy_view_pos[0], move_to_tile[1] - enemy_view_pos[1])
        self.move_to = [self, ((self.scrollx+tile_size*self.direction[0])//tile_size, (self.scrolly+tile_size*self.direction[1])//tile_size), np.linalg.norm(self.direction)]
        self.stationary = False

    # Check surrounding for player
    def check_intersection(self,players_pos,view_mat):
        dirn_list = [(0,-1),(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1)]
        # Get all tiles around the player in a 3x3 area that the enemies can go to
        player_tile_loc = []
        player_view_pos = get_pos_view(players_pos,self.room_x,self.room_y,center)
        enemy_view_pos = get_pos_view([-self.scrollx,-self.scrolly],self.room_x,self.room_y)
        for pos in player_view_pos:
            for direc in dirn_list:
                tile_x = pos[0] + direc[0]
                tile_y = pos[1] + direc[1]
                if view_mat[tile_y,tile_x] != 0:
                    player_tile_loc.append((tile_x,tile_y))
            # If player is near enemy, set the self.near_player to True
            player_direction = (pos[0] - enemy_view_pos[0], pos[1] - enemy_view_pos[1])
            if player_direction in dirn_list:
                self.near_player = True
            else:
                self.near_player = False
        # Get all tiles around the enemy in a 3x3 area that the enemies can go to
        self.intersecting_tiles = []
        
        for direc in dirn_list:
            if (direc[0] != 0) and (direc[1] != 0) and (allow_diag_move(view_mat,enemy_view_pos[0],enemy_view_pos[1],direc[0],direc[1])) == True:
                pass
            else:
                tile_x = enemy_view_pos[0] + direc[0]
                tile_y = enemy_view_pos[1] + direc[1]
                val = np.linalg.norm(direc)
                if (view_mat[tile_y,tile_x] != 0) and ((tile_x,tile_y) in player_tile_loc):
                    self.intersecting_tiles.append([(tile_x,tile_y),val])       


    # Function for taking damage
    def take_damage(self,data):
        self.damage_taken = 0
        for area in data[1]:
            if (self.rect.x,self.rect.y) == area:
                self.damage_taken = sorted([1,data[0] - self.defense])[1]   # Make sure the damage is at least 1
                if self.curr_health > 0:
                    self.curr_health -= self.damage_taken
                if self.curr_health <= 0:
                    self.curr_health = 0
                    self.kill()

    # Face the player if the player is in range
    def face_player(self,players_pos):
        # See if I am close to a player in a 3x3 area
        player_view_pos = get_pos_view(players_pos,self.room_x,self.room_y,center)
        enemy_view_pos = get_pos_view([-self.scrollx,-self.scrolly],self.room_x,self.room_y)
        self.facing = change_direction(player_view_pos, enemy_view_pos, self.direction)

class Whisp(pygame.sprite.Sprite):
    def __init__(self,x,y,m,n,direc,room_rect,enemy_id):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x,y,1,1)
        self.rect.x,self.rect.y = (x,y)
        self.scrollx,self.scrolly = (x*tile_size,y*tile_size)
        self.prev_scrollx,self.prev_scrolly = (x*tile_size,y*tile_size)
        self.in_room = (m,n)
        self.name = 'whisp'
        self.direction = direc
        self.facing = direc
        self.room_x,self.room_y = (room_rect[0],room_rect[1])
        self.move_to_player = True
        self.max_health = 100
        self.curr_health = 100
        self.defense = 0
        self.attack = 10
        self.damage_taken = 0
        self.group_move_to = []
        self.move_to = []
        self.stationary = False
        self.stationary_enemy = []
        self.id = enemy_id

    # Decide on what action to take
    def decide(self):
        if self.near_player == True:
            self.action = 'Attack'
            self.stationary = True
        else:
            self.action = 'Move Towards'
            
    # Get path to all players using A*
    def get_path(self,player_ids,players_pos,view_mat):
        # Find tile location of enemy and player based on the room
        player_view_pos = get_pos_view(players_pos,self.room_x,self.room_y,center)
        enemy_view_pos = get_pos_view([-self.scrollx,-self.scrolly],self.room_x,self.room_y)
        obj_view_pos = []
        # If there are any enemies that are stationary, find them
        for loc in self.stationary_enemy:
            obj_view_pos.append(get_pos_view([-loc[0],-loc[1]],self.room_x,self.room_y))
        # Return a dict with player id as key and path and the length of each path for the values. id:path
        self.all_path = enemy_pathfind_all(player_view_pos,player_ids,enemy_view_pos,view_mat,obj_view_pos)
        self.stationary_enemy = []
        
    # Decide what kind of path it will take
    def decide_path(self):
        if self.move_to_player == True:
            self.move_closest()

    # Move the given path
    def move_path(self):
        if self.stationary == False:
            self.scrolly += tile_size*self.direction[1]
            self.scrollx += tile_size*self.direction[0]
            tiles_x,tiles_y = (self.scrollx//tile_size, self.scrolly//tile_size)
            self.rect.x,self.rect.y = (tiles_x,tiles_y)

    # Move to the closest player
    def move_closest(self):
        # Sort based on the minimum path length, which is in index 1
        self.closest_path = min(self.all_path, key = lambda x: x[3])
        self.direction = self.closest_path[1][-1]
        self.facing = self.direction
        if len(self.closest_path[1]) > 1:
            self.stationary = False
            self.move_to = [self, ((self.scrollx+tile_size*self.direction[0])//tile_size, (self.scrolly+tile_size*self.direction[1])//tile_size), self.closest_path[2]]
        else:
            self.stationary = True
            self.move_to = [self, (self.rect.x,self.rect.y), 0]

    # Move if I am stationary. Set self.stataionary = False so we can move when move_path is called later.
    def move_stationary(self,move_to_data):
        enemy_view_pos = get_pos_view([-self.scrollx,-self.scrolly],self.room_x,self.room_y)
        move_to_tile = move_to_data[0]
        self.direction = (move_to_tile[0] - enemy_view_pos[0], move_to_tile[1] - enemy_view_pos[1])
        self.move_to = [self, ((self.scrollx+tile_size*self.direction[0])//tile_size, (self.scrolly+tile_size*self.direction[1])//tile_size), np.linalg.norm(self.direction)]
        self.stationary = False

    # Check surrounding for player
    def check_intersection(self,players_pos,view_mat):
        dirn_list = [(0,-1),(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1)]
        # Get all tiles around the player in a 3x3 area that the enemies can go to
        player_tile_loc = []
        player_view_pos = get_pos_view(players_pos,self.room_x,self.room_y,center)
        enemy_view_pos = get_pos_view([-self.scrollx,-self.scrolly],self.room_x,self.room_y)
        for pos in player_view_pos:
            for direc in dirn_list:
                tile_x = pos[0] + direc[0]
                tile_y = pos[1] + direc[1]
                if view_mat[tile_y,tile_x] != 0:
                    player_tile_loc.append((tile_x,tile_y))
            # If player is near enemy, set the self.near_player to True
            player_direction = (pos[0] - enemy_view_pos[0], pos[1] - enemy_view_pos[1])
            if player_direction in dirn_list:
                self.near_player = True
            else:
                self.near_player = False
        # Get all tiles around the enemy in a 3x3 area that the enemies can go to
        self.intersecting_tiles = []
        for direc in dirn_list:
            if (direc[0] != 0) and (direc[1] != 0) and (allow_diag_move(view_mat,enemy_view_pos[0],enemy_view_pos[1],direc[0],direc[1])) == True:
                pass
            else:
                tile_x = enemy_view_pos[0] + direc[0]
                tile_y = enemy_view_pos[1] + direc[1]
                val = np.linalg.norm(direc)
                if (view_mat[tile_y,tile_x] != 0) and ((tile_x,tile_y) in player_tile_loc):
                    self.intersecting_tiles.append([(tile_x,tile_y),val])       


    # Function for taking damage
    def take_damage(self,data):
        self.damage_taken = 0
        for area in data[1]:
            if (self.rect.x,self.rect.y) == area:
                self.damage_taken = sorted([1,data[0] - self.defense])[1]   # Make sure the damage is at least 1
                if self.curr_health > 0:
                    self.curr_health -= self.damage_taken
                if self.curr_health <= 0:
                    self.curr_health = 0
                    self.kill()

    # Face the player if the player is in range
    def face_player(self,players_pos):
        # See if I am close to a player in a 3x3 area
        player_view_pos = get_pos_view(players_pos,self.room_x,self.room_y,center)
        enemy_view_pos = get_pos_view([-self.scrollx,-self.scrolly],self.room_x,self.room_y)
        self.facing = change_direction(player_view_pos, enemy_view_pos, self.direction)

    # Organize data which will be sent to all players
    def init_data(self):
        pass