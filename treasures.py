''' Module contains all treasures'''

from actions import Action
import random
from game_endings import MissingInMase

class Treasure(Action):
    pass

class Medicine(Treasure):
    def __init__(self, name, hp, rarity):
        self.name = name
        self.hp = hp
        self.rarity = rarity

    def execute(self, game_state):
        player = game_state.player
        player.heal_hp(self.hp)
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
        player.increase_spec('attack', 5)
        player.back_pack.remove(self)
        return game_state

    def __repr__(self):
        return 'attack booster'


class ImproveShield(Treasure):
    def __init__(self):
        self.rarity = 1

    def execute(self, game_state):
        player = game_state.player
        player.increase_spec('shield', 3)
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
        player.get_damage(50, death = False)
        player.back_pack.remove(self)
        ui.say('this thing blows up in your hand!')
        if player.hp < 1:
            death = MissingInMase(game_state)
            return death.last_chance()
        return game_state

    def __repr__(self):
        return 'medicine'

class SacrificeAmulet(Treasure):
    def __init__(self):
        self.usage_check = 0
        self.rarity = 1

    def execute(self, game_state):
        player = game_state.player
        player.heal_hp(20)
        variation = random.choice((
            lambda pl: pl.reduce_spec('attack', 1),
            lambda pl: pl.reduce_spec('shield', 5),
            lambda pl: pl.reduce_spec('agility', 1),
            lambda pl: setattr(pl, 'name', random.choice(('Dingus','Dork','Clown','Waffle')))
        ))
        variation(player)
        self.usage_check += 1
        if self.usage_check == 5: player.back_pack.remove(self)
        return game_state

    def __repr__(self):
        return 'sacrifice amulet'


class Key(Treasure):
    def __init__(self, name):
        self.name = name
        self.mode = 'quest'

    def execute(self, game_state):
        ui = game_state.UI
        ui.say('You must find exit!')
        return game_state

    def __repr__(self):
        return self.name

class ResilienceMutagen(Treasure):
    def __init__(self):
        self.rarity = 1

    def execute(self, game_state):
        player = game_state.player
        player.increase_spec('max_hp', 10)
        player.back_pack.remove(self)
        return game_state

    def __repr__(self):
        return 'resilience mutagen'

class Bomb(Treasure):
    def __init__(self):
        self.rarity = 1
        self.mode = 'bomb'

    def execute(self, game_state):
        player = game_state.player
        ui = game_state.UI
        player.get_damage(50, death=False)
        ui.say('the box suddenly explodes')
        if player.hp < 1:
            death = MissingInMase(game_state)
            return death.last_chance()
        return game_state

class PhoenixAmulet(Treasure):
    def __init__(self):
        self.rarity = 1
        self.mode = 'raise'

    def execute(self, game_state):
        ui = game_state.UI
        ui.say('looks like an ancient amulet')
        return game_state

    def last_chance(self, game_state):
        player = game_state.player
        player.hp = player.max_hp // 2
        ui = game_state.UI
        ui.say('\n\n\nA flash of light! An ancient burning bird brings you back from the hell..')
        player.back_pack.remove(self)
        return game_state

    def __repr__(self):
        return 'phoenix amulet'

class TrueBookOfPower(Treasure):
    def __init__(self):
        self.rarity = 1

    def execute(self, game_state):
        player = game_state.player
        room = game_state.curr_room
        ui = game_state.UI
        sacrifice = random.choice(list(filter(lambda item: getattr(item, 'mode', None) != 'quest', player.back_pack)))
        player.back_pack.remove(sacrifice)
        if room.monster:
            room.monster = None
        ui.say('all living things turned to dust')
        return game_state

    def __repr__(self):
        return 'true book of power'