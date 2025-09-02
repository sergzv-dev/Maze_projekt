''' Module contains all treasures'''

from actions import Action
import random
from game_endings import MissingInMase

class Treasure(Action):
    def to_json(self):
        return [f'{self.sign}', 'Treasure', None]

    @staticmethod
    def from_json(sign):
        return treas_chek_list[sign]()


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
        self.sign = 'LittleMedicine'

class MediumMedicine(Medicine):
    def __init__(self):
        super().__init__('medicine', 15, 3)
        self.sign = 'MediumMedicine'

class LargeMedicine(Medicine):
    def __init__(self):
        super().__init__('large medicine', 25, 1)
        self.sign = 'LargeMedicine'


class ImproveAttack(Treasure):
    def __init__(self):
        self.rarity = 1
        self.sign = 'ImproveAttack'

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
        self.sign = 'ImproveShield'

    def execute(self, game_state):
        player = game_state.player
        player.increase_spec('shield', 5)
        player.back_pack.remove(self)
        return game_state

    def __repr__(self):
        return 'shield booster'


class FakePowerBook(Treasure):
    def __init__(self):
        self.rarity = 1
        self.sign = 'FakePowerBook'

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
    def __init__(self):
        self.usage_check = 0
        self.rarity = 1
        self.sign = 'SacrificeAmulet'

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


class ResilienceMutagen(Treasure):
    def __init__(self):
        self.rarity = 1
        self.sign = 'ResilienceMutagen'

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
        self.sign = 'Bomb'

    def execute(self, game_state):
        player = game_state.player
        ui = game_state.UI
        player.take_damage(50, game_state, death=False)
        ui.say('the box suddenly explodes')
        if player.death_marker:
            return MissingInMase(game_state)
        return game_state

class PhoenixAmulet(Treasure):
    def __init__(self):
        self.rarity = 1
        self.mode = 'raise'
        self.sign = 'PhoenixAmulet'

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
    def __init__(self):
        self.rarity = 1
        self.sign = 'TrueBookOfPower'

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
    def __init__(self, id_):
        self.sign = 'QuestItem'
        self.name = 'quest treasure'
        self.id_ = id_
        self.mode = 'quest'
        self.answer = '42'

    def execute(self, game_state):
        ui = game_state.UI
        ui.say(self.answer)
        return game_state

    def __repr__(self):
        return self.name

    def to_json(self):
        return [self.sign, 'QuestItem', self.id_]

    @staticmethod
    def from_json(sign, id_):
        return treas_chek_list[sign](id_)


class Key(QuestItem):
    def __init__(self, id_):
        super().__init__(id_)
        self.name = 'Golden Key'
        self.answer = 'You must find exit!'
        self.sign = 'Key'


class ImmortalAmulet(QuestItem):
    def __init__(self, id_):
        super().__init__(id_)
        self.name = 'Immortal amulet'
        self.answer = 'You must find altar for sacrifice!'
        self.sign = 'ImmortalAmulet'

treas_chek_list = {'LittleMedicine': LittleMedicine, 'MediumMedicine': MediumMedicine, 'LargeMedicine': LargeMedicine,
                   'ImproveAttack': ImproveAttack, 'ImproveShield': ImproveShield, 'FakePowerBook': FakePowerBook,
                   'SacrificeAmulet': SacrificeAmulet, 'ResilienceMutagen': ResilienceMutagen, 'Bomb': Bomb,
                   'PhoenixAmulet': PhoenixAmulet, 'TrueBookOfPower': TrueBookOfPower, 'QuestItem': QuestItem,
                   'Key': Key, 'ImmortalAmulet': ImmortalAmulet}

def take_treasures_list(trs_data):
    trs_list = []
    for sign, kind, id_ in trs_data:
        if kind == 'Treasure':
            trs_list.append(Treasure.from_json(sign))
        if kind == 'QuestItem':
            trs_list.append(QuestItem.from_json(sign, id_))
    return trs_list

def take_treasure_item(trs_data):
    item = None
    if trs_data is not None:
        sign, kind, id_ =  trs_data
        if kind == 'Treasure':
            item = Treasure.from_json(sign)
        if kind == 'QuestItem':
            item = QuestItem.from_json(sign, id_)
    return item