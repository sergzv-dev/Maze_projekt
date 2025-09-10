from game_endings import EndGame, HappyEnd
from creatures import Player
from actions import EndDoorAction
from game_states import GameState
from room import Room
from treasures import Key
from ui_terminal import UI
from quests import QuestObject
import uuid
import pytest

@pytest.fixture
def game_state_test():
    test_ui = UI()
    test_player = Player('test')
    test_room = Room((1, 1))
    return GameState(master = test_ui, world = None, player = test_player, curr_room = test_room)

@pytest.fixture
def endgame_quest(game_state_test):
    game_states = game_state_test
    id_ = str(uuid.uuid4())
    test_ques = QuestObject('test', id_)
    test_key = Key(id_)
    game_states.curr_room.quest = test_ques
    game_states.player.back_pack = [test_key]
    return game_states

def test_right_key(endgame_quest):
    test_action = EndDoorAction()
    game_states = endgame_quest

    assert isinstance(test_action.execute(game_states), HappyEnd)
    assert isinstance(test_action.execute(game_states), EndGame)

def test_wrong_key(endgame_quest):
    game_states = endgame_quest
    wrong_key = Key(str(uuid.uuid4()))
    game_states.player.back_pack = [wrong_key]
    test_action = EndDoorAction()

    assert isinstance(test_action.execute(game_states), GameState)

def test_none_key(endgame_quest):
    game_states = endgame_quest
    game_states.player.back_pack = []
    test_action = EndDoorAction()

    assert isinstance(test_action.execute(game_states), GameState)