'''Main game modul'''

from creatures import Player
from room import name_convert
from ui_terminal import UI
from map_bilder import World
from game_states import GameState
from game_endings import EndGame
from actions import ActionProvider
from quests import MainQuest, ImmortalAmuletQuest


def game():
    master = UI()
    name = master.ask("What is your name? ")
    player = Player(name)
    world = World(10, 10)
    curr_room = world.rooms_dict[name_convert('A1')]
    game_state = GameState(master, world, player, curr_room)
    action_provider = ActionProvider()
    MainQuest(world)
    ImmortalAmuletQuest(world)

    while True:
        # print(f'current room: {game_state.curr_room}')
        print(f'monster: {game_state.curr_room.monster}')
        print(f'loot: {game_state.curr_room.loot}')
        # print(f'hidden actions: {game_state.curr_room.hidden_actions}')
        print(f'box: {game_state.curr_room.box}\n')

        actions = action_provider.provide_action(game_state)
        action = master.choose(actions)
        game_state = action.execute(game_state)
        if isinstance(game_state, EndGame): break

game()