''' Module contains all treasures'''

from actions import Action
import random

class Treasure(Action):
    pass

class Medicine(Treasure):
    def __init__(self, name, hp, rarity):
        self.name = name
        self.hp = hp
        self.rarity = rarity

    def execute(self, game_state):
        player = game_state.player
        player.hp = min(100, player.hp + self.hp)
        player.back_pack.remove(self)
        return game_state

    def __repr__(self):
        return f'{self.name}'

class LittleMedicine(Medicine):
    def __init__(self):
        super().__init__('little medicine', 10, 5)

class MediumMedicine(Medicine):
    def __init__(self):
        super().__init__('medicine', 15, 3)

class LargeMedicine(Medicine):
    def __init__(self):
        super().__init__('large medicine', 25, 1)


class ImproveAttack(Treasure):
    def __init__(self):
        self.rarity = 1

    def execute(self, game_state):
        player = game_state.player
        player.attack += 5
        player.back_pack.remove(self)
        return game_state

    def __repr__(self):
        return 'attack booster'


class ImproveShield(Treasure):
    def __init__(self):
        self.rarity = 1

    def execute(self, game_state):
        player = game_state.player
        player.shield += 10
        player.back_pack.remove(self)
        return game_state

    def __repr__(self):
        return 'shield booster'

class FakePowerBook(Treasure):
    def __init__(self):
        self.rarity = 1

    def execute(self, game_state):
        player = game_state.player
        ui = game_state.UI
        player.hp = max(1, player.hp - 50)
        player.back_pack.remove(self)
        ui.say('this thing blows up in your hand!')
        return game_state

    def __repr__(self):
        return 'medicine'

class VictimAmulet(Treasure):
    def __init__(self):
        self.usage_check = 0
        self.rarity = 1

    def execute(self, game_state):
        player = game_state.player
        player.hp = min(100, player.hp +20)
        variation = random.choice((
            lambda pl: setattr(pl, 'attack', max(1, pl.attack - 1)),
            lambda pl: setattr(pl, 'shield', max(1, pl.shield - 5)),
            lambda pl: setattr(pl, 'agility', max(1, pl.agility - 1)),
            lambda pl: setattr(pl, 'name', random.choice(('Dingus','Dork','Clown','Waffle')))
        ))
        variation(player)
        self.usage_check += 1
        if self.usage_check == 5: player.back_pack.remove(self)
        return game_state

    def __repr__(self):
        return 'victim amulet'