''' Module contains all treasures'''

from actions import Action
import random
from game_endings import MissingInMase

class Treasure(Action):
    _registry = dict()
    rarity = 1

    def __init_subclass__(cls, **kwargs):
        Treasure._registry[cls.__name__] = cls

    def to_json(self) -> dict:
        return {'cls': self.__class__.__name__, **self.__dict__}

    @classmethod
    def from_json(cls, data: dict) -> 'Treasure':
        class_name = data.pop('cls')
        cls_ = cls._registry[class_name]
        return cls_(**data)


class Medicine(Treasure):
    def __init__(self, name='medicine', hp=5):
        self.name = name
        self.hp = hp

    def execute(self, game_state):
        ui = game_state.UI
        ui.say(f'get healed {self.hp}')
        player = game_state.player
        player.heal_hp(self.hp)
        player.back_pack.remove(self)
        return game_state

    def __repr__(self):
        return f'{self.name}'


class LittleMedicine(Medicine):
    rarity = 5

    def __init__(self, name='little medicine', hp=10):
        super().__init__(name, hp)


class MediumMedicine(Medicine):
    rarity = 3

    def __init__(self, name='medicine', hp=15):
        super().__init__(name, hp)


class LargeMedicine(Medicine):
    def __init__(self, name='large medicine', hp=25):
        super().__init__(name, hp)


class ImproveAttack(Treasure):
    def execute(self, game_state):
        ui = game_state.UI
        ui.say('improved attack on 5 points')
        player = game_state.player
        player.increase_spec('attack', 5)
        player.back_pack.remove(self)
        return game_state

    def __repr__(self):
        return 'attack booster'


class ImproveShield(Treasure):
    def execute(self, game_state):
        ui = game_state.UI
        ui.say('improved shield on 5 points')
        player = game_state.player
        player.increase_spec('shield', 5)
        player.back_pack.remove(self)
        return game_state

    def __repr__(self):
        return 'shield booster'


class FakePowerBook(Treasure):
    def execute(self, game_state):
        player = game_state.player
        ui = game_state.UI
        player.take_damage(50, game_state, death = False)
        player.back_pack.remove(self)
        ui.say('this thing blows up in your hand!')
        if player.death_marker:
            return MissingInMase(game_state)
        return game_state

    def __repr__(self):
        return 'medicine'

class SacrificeAmulet(Treasure):
    def __init__(self, usage_check = 0):
        self.usage_check = usage_check

    def execute(self, game_state):
        ui = game_state.UI
        ui.say('get healed 20 hp sacrificing your strength')
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


class ResilienceMutagen(Treasure):
    def execute(self, game_state):
        ui = game_state.UI
        ui.say('improved max hp on 10 points')
        player = game_state.player
        player.increase_spec('max_hp', 10)
        player.back_pack.remove(self)
        return game_state

    def __repr__(self):
        return 'resilience mutagen'

class Bomb(Treasure):
    mode = 'bomb'

    def execute(self, game_state):
        player = game_state.player
        ui = game_state.UI
        ui.say('the box suddenly explodes')
        player.take_damage(50, game_state, death=False)
        if player.death_marker:
            return MissingInMase(game_state)
        return game_state

    def __repr__(self):
        return 'BOMB!!'

class PhoenixAmulet(Treasure):
    mode = 'raise'

    def execute(self, game_state):
        ui = game_state.UI
        ui.say('looks like an ancient amulet')
        return game_state

    def last_chance(self, game_state):
        player = game_state.player
        player.hp = player.max_hp // 2
        player.death_marker = False
        ui = game_state.UI
        ui.say('\n\n\nA flash of light! An ancient burning bird brings you back from the hell..')
        player.back_pack.remove(self)
        return game_state

    def __repr__(self):
        return 'phoenix amulet'

class TrueBookOfPower(Treasure):
    def execute(self, game_state):
        player = game_state.player
        room = game_state.curr_room
        ui = game_state.UI
        sacrifice = random.choice([item for item in player.back_pack if not isinstance(item, QuestItem)])
        player.back_pack.remove(sacrifice)
        if room.monster:
            room.monster.take_damage(9999, game_state)
        ui.say('all living things turned to dust')
        return game_state

    def __repr__(self):
        return 'true book of power'

class QuestItem(Treasure):
    mode = 'quest'
    answer = '42'

    def __init__(self, *, id_, name='quest treasure'):
        self.name = name
        self.id_ = id_

    def execute(self, game_state):
        ui = game_state.UI
        ui.say(self.answer)
        return game_state

    def __repr__(self):
        return self.name


class Key(QuestItem):
    answer = 'You must find exit!'

    def __init__(self, id_, name = 'Golden Key'):
        super().__init__(id_ = id_, name = name)


class ImmortalAmulet(QuestItem):
    answer = 'You must find altar for sacrifice!'

    def __init__(self, id_, name = 'Immortal amulet'):
        super().__init__(id_ = id_, name = name)

# def take_treasures_list(items):
#     return [ Treasure.from_json(data) for item in items ]
#
#
# take_treasure_item = Treasure.from_json