''' Module contains states of current game'''
import json
from creatures import Player
from map_builder import World

class GameState():
    def __init__(self, master, world, player, curr_room):
        self.UI = master
        self.player = player
        self.world = world
        self.curr_room = curr_room

    def save_game(self, file_link):
        with open(file_link, 'w') as f:
            f.write(self.to_json())

    def load_game(self, file_link):
        with open(file_link, 'r') as f:
            json_data = f.read()
            game_state = self.from_json(json_data)
            return game_state

    def to_json(self):
        player = self.player.to_json()
        world = self.world.to_json()
        curr_room = list(self.curr_room.name)
        data = {'player': player, 'world': world, 'curr_room': curr_room}
        return json.dumps(data)

    def from_json(self, json_data):
        data = json.loads(json_data)
        master = self.UI
        player = Player.from_json(data['player'])
        world = World.from_json(data['world'])
        curr_room = world.rooms_dict(tuple(data['curr_room']))
        return GameState(master, world, player, curr_room)