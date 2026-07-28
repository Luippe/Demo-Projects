import asyncio
import pickle
from game import Game,Player
from enemy_client_test import Enemy
from concurrent.futures import ThreadPoolExecutor
import pygame
center = (320, 256)
tile_size = 64

# Class that takes care of networking between server and client
class Network:
    def __init__(self, ipv="127.0.0.1", port=5555, connect_attempts=1, retry_delay=0.2):
        self.ipv = ipv
        self.port = port
        self.connect_attempts = max(1, connect_attempts)
        self.retry_delay = retry_delay
        self.mini_map = None
        self.canvas = None
        self.id = None
        self.get_map = False
        self.item_change = None
        self.num_players = None
        self.enemy_class = None
        self.action_class = None
        self.health_class = None
        self.do_action = None

    # Get user ID specific to you
    async def get_id(self,reader):
        id_string = await reader.read(1)
        self.id = int(id_string)
        await asyncio.sleep(0.03)

    # Get initial map data from the server when you first connect.
    async def init_data(self,reader):
        len_tot = await reader.readuntil(separator=b',')
        # Get the length of len_list
        len_tot = int(len_tot[-3:-1].decode())
        len_list = await reader.read(len_tot)
        len_list = len_list.decode()
        print(f"Initial Data Size is: {len_list}")
        self.data_list = []
        arr = len_list.split(',')
        for num in range(len(arr)):
            data_temp = await reader.read(int(arr[num]))
            self.data_list.append(pickle.loads(data_temp))
        self.map_mat,self.spawn_list,self.room_list,self.item_loc,self.id_list = self.data_list
        self.index = self.id_list.index(self.id)
        self.num_players = len(self.id_list)

    # Get number of players when joined
    async def get_players(self):
        self.player_dict = [Player(1000,1000,num) for num in self.id_list]

    # Async function for transferring data to the server, as well as obtaining data from the server.
    # Using dictionaries to pack data and pickle.dumps to encode them into bytes
    async def transfer_data(self,reader,writer):
        running = True
        while running:
            self.player = self.player_dict[self.index]
            # Prepare to send data to server using writer
            if self.get_map == True:
                send_data = {"type":"map","id":self.id}
                send_data = pickle.dumps(send_data)
                self.get_map = False
            elif self.item_change != None:
                send_data = pickle.dumps(self.item_change)
                self.item_change = None
            elif self.do_action != None:
                send_data = pickle.dumps(self.do_action)
                self.do_action = None
            else:
                send_data = {"type":"pos","id":self.id,"pos":[self.player.scrollx,self.player.scrolly,self.player.facing],
                             'room':self.player.in_room_loc,
                             'turn':self.player.turn,
                             'in combat':self.player.in_combat,
                             'health':[self.player.max_health,self.player.curr_health],
                             'defense':[self.player.base_defense,self.player.defense],
                             'ready check':self.player.ready_check}
                send_data = pickle.dumps(send_data)
            writer.write(send_data)
            await writer.drain()
            # Prepare to receive data from server using reader
            raw_data = await reader.read(2048)
            data = pickle.loads(raw_data)
            # print(data, len(raw_data))
            # Obtain specific data from the dictionary
            try:
                if data["type"] == "pos":
                    self.pos_data(data)
                elif data['type'] == 'turn':
                    self.player.turn = data['turn']
                    if data['turn'] == True:    # If it is the player's turn. Decrease cooldown of all abilities and special moves
                        self.action_class.handle_cooldown()
                elif data['type'] == 'enemy':
                    self.enemy_data(data)
                elif data["type"] in ('item', 'chest', 'head', 'legs', 'weapon'):
                    self.item_data(data)
                elif data['type'] == 'action':
                    self.action_data(data)
                elif data['type'] == 'tile':
                    self.tile_data(data)
                elif data["type"] == "map":
                    await self.init_data(reader)
                    game_class.new_map()
                elif data['type'] == 'conn':
                    self.connection_data(data)
            except:
                pass
        # Close connection if client disconnects
        print('Close the connection')
        writer.close()
        await writer.wait_closed()
        pygame.quit()

    async def connect(self):
        last_error = None
        for attempt in range(self.connect_attempts):
            try:
                return await asyncio.open_connection(self.ipv, self.port)
            except OSError as error:
                last_error = error
                if attempt + 1 < self.connect_attempts:
                    await asyncio.sleep(self.retry_delay)
        raise ConnectionError(
            f"Could not connect to {self.ipv}:{self.port}. "
            "Check that the host is running and Hamachi is connected."
        ) from last_error

    async def main(self):
        reader, writer = await self.connect()
        loop = asyncio.get_event_loop()
        await self.get_id(reader)
        await self.init_data(reader)
        await self.get_players()
        global game_class
        game_class = Game(self)
        self.task = asyncio.wait([asyncio.ensure_future(self.transfer_data(reader,writer)),
                                  loop.run_in_executor(ThreadPoolExecutor(), game_class.run,loop)],return_when=asyncio.FIRST_COMPLETED)
        try:
            await self.task
        except asyncio.CancelledError:
            print("Disconnecting from Server")

    # Handle enemy data
    def enemy_data(self,data):
        if data['data'] == 'pos':
            self.enemy_class.enemy_pos = []
            self.enemy_class.enemy_names = []
            self.enemy_class.enemy_pos = data['pos']
            self.enemy_class.enemy_names = list(data['pos'].keys())
        elif data['data'] == 'health':
            self.enemy_class.enemy_take_damage(data['health'])
        elif data['data'] == 'in combat':
            self.player.in_combat = data['in combat']
            if data['in combat'] == False:
                self.player.turn = True
        elif data['data'] == 'attack':
            pass

    # Handle player position data
    def pos_data(self,data):
        counter = 0
        for num,players in enumerate(self.player_dict):
            if (num != self.index):
                players.scrollx, players.scrolly, players.facing = data['pos'][counter]
                players.in_room_loc = data['room'][counter]
                players.max_health,players.curr_health = data['health'][counter]
                players.base_defense,players.defense = data['defense'][counter]
                players.ready_check = data['ready check'][counter]
                counter += 1

    # Handle items
    def item_data(self,data):
        item_name = data['type']
        item_data = tuple(data[item_name])
        if item_data in self.item_loc[item_name]:
            self.item_loc[item_name].remove(item_data)
            self.canvas.item_loc = self.item_loc
            self.mini_map.display_items_list.remove((item_data[0],item_data[1]))
        else:
            self.item_loc[item_name].append(item_data)
            self.canvas.item_loc = self.item_loc
            self.mini_map.display_items_list.append((item_data[0],item_data[1]))

    # Handle actions
    def action_data(self,data):
        if data['action'] == 'attack':
            self.player.damage, self.player.damage_tile_list, self.player.max_damage_delay, self.player.attack_order = data['data']
            self.player.damage_delay = 100

    # Handle changing tiles on the map
    def tile_data(self,data):
        pass
    
    # Handle multiple connections
    def connection_data(self,data):
        if data['change'] == 'add':
            self.player_dict.append(Player(1000,1000,data['id']))
            self.id_list.append(data['id'])
        elif data['change'] == 'remove':
            self.player_dict.pop(data['id'])
            self.id_list.remove(self.id_list[data['id']])
        self.num_players = len(self.id_list)
        self.index = self.id_list.index(self.id)
        game_class.new_player(self.player_dict)
