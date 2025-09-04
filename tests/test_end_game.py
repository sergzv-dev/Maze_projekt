from game_endings import EndGame, HappyEnd
from creatures import Player
from actions import EndDoorAction
from game_states import GameState
from room import Room
from treasures import Key
from ui_terminal import UI
from quests import QuestObject
import uuid

def test():
    test_player = Player('test')
    test_room = Room((1,1))
    id_ = str(uuid.uuid4())
    test_ques = QuestObject('test', id_)
    test_room.quest =  test_ques
    test_key = Key(id_)
    wrong_key = Key(str(uuid.uuid4()))
    test_ui = UI()
    test_action = EndDoorAction()
    game_states = GameState(master = test_ui, world = None, player = test_player, curr_room = test_room)

    game_states.player.back_pack = [test_key]
    test_action.execute(game_states)

    assert isinstance(test_action.execute(game_states), HappyEnd)
    assert isinstance(test_action.execute(game_states), EndGame)

    game_states.player.back_pack = [wrong_key]
    assert isinstance(test_action.execute(game_states), GameState)

    game_states.player.back_pack = [None]
    assert isinstance(test_action.execute(game_states), GameState)