from creatures import Player
from treasures import ResilienceMutagen
from game_states import GameState

def test_resilience_mutagen():
    test_player = Player('test')
    game_states = GameState(master=None, world=None, player=test_player, curr_room=None)
    game_states.player.back_pack = [ResilienceMutagen()]
    test_max_hp = game_states.player.max_hp
    game_states.player.back_pack[0].execute(game_states)
    assert test_player.max_hp == test_max_hp + 10