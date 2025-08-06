from game_endings import EndGame, HappyEnd
from creatures import Player
from actions import EndDoorAction
from game_states import GameState
from room import Room
from treasures import Key
from ui_terminal import UI

def test():
    test_player = Player('test')
    test_room = Room((1,1))
    test_key = Key('test key')
    wrong_key = Key('wrong')
    test_ui = UI()
    test_action = EndDoorAction(test_key)
    game_states = GameState(master = test_ui, world = None, player = test_player, curr_room = test_room)

    game_states.curr_room.actions.append(test_action)

    game_states.player.back_pack = [test_key]
    test_action.execute(game_states)

    assert isinstance(test_action.execute(game_states), HappyEnd)
    assert isinstance(test_action.execute(game_states), EndGame)

    game_states.player.back_pack = [wrong_key]
    assert isinstance(test_action.execute(game_states), GameState)

    game_states.player.back_pack = [None]
    assert isinstance(test_action.execute(game_states), GameState)