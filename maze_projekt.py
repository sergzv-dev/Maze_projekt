'''Main game modul'''

from creatures import Player
from room import name_convert
from ui_terminal import UI
from map_bilder import World
from game_states import GameState


def game():
    master = UI()
    name = master.ask("What is your name? ")
    player = Player(name)
    world = World(10, 10)
    curr_room = world.rooms_dict[name_convert('A1')]
    game_state = GameState(master, world, player, curr_room)
    while True:
        print(f'current room: {game_state.curr_room}')
        print(f'monster: {game_state.curr_room.monster}')
        print(f'loot: {game_state.curr_room.loot}')
        print(f'box: {game_state.curr_room.box}\n')
        actions = game_state.possible_actions()
        action = master.choose(actions)
        game_state = action.execute(game_state)

game()