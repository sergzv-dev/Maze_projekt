''' Module contains states of current game'''
import json

class GameState():
    def __init__(self, master, world, player, curr_room):
        self.UI = master
        self.player = player
        self.world = world
        self.curr_room = curr_room

    def save_game(self, file_link = 'save_data.json'):
        with open(file_link, 'w') as f:
            f.write(self.to_json())
        return self

    def load_game(self, ui, file_link = 'save_data.json',):
        with open(file_link, 'r') as f:
            json_data = f.read()
            game_state = GameState.from_json(json_data, ui)
        return game_state

    def to_json(self) -> str:
        player = self.player.to_json()
        world = self.world.to_json()
        curr_room = list(self.curr_room.name)
        data = {'player': player, 'world': world, 'curr_room': curr_room}
        return json.dumps(data)

    @classmethod
    def from_json(cls, json_data: str, ui) -> GameState:
        from creatures import Player
        from map_builder import World

        data = json.loads(json_data)
        player = Player.from_json(data['player'])
        world = World.from_json(data['world'])
        curr_room = world.rooms_dict[tuple(data['curr_room'])]
        return cls(ui, world, player, curr_room)
