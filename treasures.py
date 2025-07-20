''' Module contains all treasures'''

from actions import Action

class Treasure(Action):
    pass

class Medicine(Treasure):
    def __init__(self, size):
        if size == 10:
            self.name, self.hp = 'little medicine', 10
        elif size == 15:
            self.name, self.hp = 'medicine', 15
        elif size == 25:
            self.name, self.hp = 'large medicine', 25
        else:
            raise ValueError('"size" should be 10, 15 or 25')

    def execute(self, game_state):
        player = game_state.player
        player.hp = min(100, player.hp + self.hp)
        player.back_pack.remove(self)
        return game_state

    def __repr__(self):
        return f'{self.name}'


class ImproveAttack(Treasure):
    def execute(self, game_state):
        player = game_state.player
        player.attack += 5
        player.back_pack.remove(self)
        return game_state

    def __repr__(self):
        return 'attack booster'


class ImproveShield(Treasure):
    def execute(self, game_state):
        player = game_state.player
        player.shield += 10
        player.back_pack.remove(self)
        return game_state

    def __repr__(self):
        return 'shield booster'