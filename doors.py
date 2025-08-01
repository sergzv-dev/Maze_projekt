
from actions import Action
from game_endings import HappyEnd
from treasures import Treasure

class EndDoorAction(Action):
    def execute(self, game_state):
        player = game_state.player
        ui = game_state.UI
        chek = 0

        for key in filter(lambda x: isinstance(x, Key), player.back_pack):
            if key.end_door is True:
                chek = 2
                break
            if key.end_door is False: chek = 1

        if chek == 0: ui.say('Find the key\n')
        if chek == 1: ui.say('The key doesn\'t past\n')
        if chek == 2: return HappyEnd(game_state)
        return game_state

    def __repr__(self):
        return 'Try to open old hidden door'

class Key(Treasure):
    def __init__(self, kind):
        self.end_door = False
        self.name = 'Key'
        if kind == 1:
            self.end_door = True
            self.name = 'Golden key'

    def execute(self, game_state):
        ui = game_state.UI
        ui.say('You must find exit!')
        return game_state

    def __repr__(self):
        return self.name