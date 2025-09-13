''' Module contains classes for player and monsters'''

import random


class Backpack(list):

    def to_json(self) -> list[dict]:
        return [ item.to_json() for item in self ]

    @classmethod
    def from_json(cls, data: list[dict]) -> Backpack:
        return cls([ Treasure.from_json(data) for item in data ])

# разные опции использования
# monster = chosen_monster_cls(loot=give_random_loot())
#
# monster = chosen_monster_cls().add_loot(give_random_loot())
#
# monster = chosen_monster_cls()
# monster.add_loot(give_random_loot())
#
# monster = chosen_monster_cls()
# monster.back_pack.append(give_random_loot())


class Creature:
    max_attack = 999
    DEFAULTS = {......}

    def __init__(self, backpack=None, *args, **kwargs):
        # self.name = name or self.DEFAULS['name']
        # self.attack = attack or self.DEFAULS['attack']

        self.name = kwargs.get('name', 'creature')
        self.attack = kwargs.get('attack', 1)
        self.max_attack = kwargs.get('max_attack', 999)
        self.shield = kwargs.get('shield', 0)
        self.max_shield = kwargs.get('max_shield', 999)
        self.hp = kwargs.get('hp', 10)
        self.max_hp = kwargs.get('max_hp', 999)
        self.agility = kwargs.get('agility', 0)
        self.max_agility = kwargs.get('max_agility', 999)
        self.back_pack = backpack or Backpack()
        self.death_marker = False
        self.after_death_act = None

    def add_loot(self, item):
        self.back_pack.append(item)
        return self


    def heal_hp(self, value):
        self.hp = min(self.max_hp, self.hp + value)

    def take_damage(self, value, game_state, *, death = True):
        min_hp = -1
        ui = game_state.UI
        if not death and self.hp != 1: min_hp = 1
        damage = round(value*(1- self.shield/100))
        if random.randint(1, 100) <= self.agility:
            damage = 0
            ui.say(f'{self.name} dodged the attack')
        self.hp = max(min_hp, self.hp - damage)
        ui.say(f'{self.name} received damage: {damage}')
        self.death_chek(game_state)

    def increase_spec(self, spec, value):
        max_val = getattr(self, f'max_{spec}', float('inf'))
        setattr(self, spec, min(max_val, getattr(self, spec) + value))

    def reduce_spec(self, spec, value):
        min_val = 1
        setattr(self, spec, max(min_val, getattr(self, spec) - value))

    def death_chek(self, game_state):
        pass

    def to_json(self):
        data = self.__dict__.copy()
        data['back_pack'] = [item.to_json() for item in self.back_pack]
        if self.after_death_act is not None:
            data['after_death_act'] = self.after_death_act.to_json()
        return data

class Player(Creature):
    DEFAULTS = dict(attack = 10, max_attack = 100, shield = 10, max_shield = 50, hp = 100, max_hp = 100,
                    agility = 5, max_agility = 40
                    )

    def __init__(self, name, *args, **kwargs):
        params = {**self.DEFAULTS, **kwargs}
        super().__init__(*args, **params)
        self.name = name
        self.fight_marker = False
        self.open_bp = False


    def death_chek(self, game_state):
        last_chance_list = []
        if self.hp < 1:
            last_chance_list = list(filter(lambda item: getattr(item, 'mode', None) == 'raise', self.back_pack))
            self.death_marker = True
        if self.death_marker and last_chance_list:
            last_chance_list[0].last_chance(game_state)


    @classmethod
    def from_json(cls, data):
        from treasures import take_treasures_list

        name = data.pop('name')
        bp_data = data.pop('back_pack')
        back_pack = take_treasures_list(bp_data)
        fight_marker = data.pop('fight_marker')
        open_bp = data.pop('open_bp')
        death_marker = data.pop('death_marker')

        player = cls(name, **data)

        player.back_pack = back_pack
        player.fight_marker = fight_marker
        player.open_bp = open_bp
        player.death_marker = death_marker
        return player


class Monster(Creature):
    DEFAULTS = dict()
    _registry = dict()

    def __init__(self, loot = None, *args, **kwargs):
        params = {**self.DEFAULTS, **kwargs}
        super().__init__(*args, **params)
        if loot is not None:
            self.back_pack.append(loot)

    def __init_subclass__(cls, **kwargs):
        Monster._registry[cls.__name__] = cls

    def death_chek(self, game_state):
        ui = game_state.UI
        room = game_state.curr_room
        if self.hp < 1:
            ui.say(f'{self} is defeated')
            if self.back_pack:
                ui.say(f'the monster dropped the {self.back_pack[0]}')
                room.loot += self.back_pack
            game_state.player.fight_marker = False
            if self.after_death_act:
                game_state = self.after_death_act.execute(game_state)
            room.monster = None
        return game_state

    def __repr__(self):
        return f'{self.name}'

    def to_json(self):
        data = super().to_json()
        data.update({'cls': self.__class__.__name__})
        return data

    @classmethod
    def from_json(cls, data):
        from treasures import take_treasures_list
        class_name = data.pop('cls')
        cls_ = cls._registry[class_name]

        bp_data = data.pop('back_pack')
        back_pack = take_treasures_list(bp_data)
        death_marker = data.pop('death_marker')
        ada_sign = data.pop('after_death_act')
        after_death_act = None
        if ada_sign is not None:
            after_death_act = AfterDeathAction.from_json(ada_sign)

        monster = cls_(**data)

        monster.back_pack = back_pack
        monster.death_marker = death_marker
        monster.after_death_act = after_death_act
        return monster

class Soldier(Monster):
    DEFAULTS = dict(name = 'Soldier', attack = 7, shield = 10, hp = 50, agility = 5)

class Goblin(Monster):
    DEFAULTS = dict(name = 'Goblin', attack = 5, shield = 0, hp = 30, agility = 15)

class Mage(Monster):
    DEFAULTS = dict(name = 'Mage', attack = 12, shield = 5, hp = 40, agility = 0)

class Knight(Monster):
    DEFAULTS = dict(name = 'Knight', attack = 9, shield = 20, hp = 70, agility = 5)

class Mimic(Monster):
    DEFAULTS = dict(name = 'Mimic', attack = 8, shield = 15, hp = 60, agility = 10)


# StrongMonsters:

def undead(monster):
    monster.name = 'Undead ' + monster.name
    monster.attack = monster.attack + 2
    monster.shield = monster.shield + 10
    monster.hp = monster.hp + 20
    monster.agility = monster.agility
    return monster

def beastly(monster):
    monster.name = 'Beastly ' + monster.name
    monster.attack = monster.attack + 3
    monster.shield = monster.shield
    monster.hp = monster.hp + 15
    monster.agility = monster.agility + 5
    return monster

def demonic(monster):
    monster.name = 'Demonic ' + monster.name
    monster.attack = monster.attack + 5
    monster.shield = monster.shield + 5
    monster.hp = monster.hp + 30
    monster.agility = monster.agility + 5
    monster.after_death_act = ExplosionMod()
    return monster


def frozen(monster):
    monster.name = 'Frozen ' + monster.name
    monster.attack = monster.attack
    monster.shield = monster.shield + 15
    monster.hp = monster.hp + 10
    monster.agility = max(0, monster.agility - 5)
    return monster

def cursed(monster):
    monster.name = 'Cursed ' + monster.name
    monster.attack = monster.attack + 4
    monster.shield = monster.shield
    monster.hp = monster.hp + 10
    monster.agility = max(0, monster.agility - 5)
    return monster

# SuperMonsters:

def champion(st_monster):
    st_monster.name = 'CHAMPION ' + st_monster.name.upper()
    st_monster.attack = st_monster.attack
    st_monster.shield = st_monster.shield + 20
    st_monster.hp = st_monster.hp + 50
    st_monster.agility = st_monster.agility + 10
    return st_monster

def flaming(st_monster):
    st_monster.name = 'FLAMING ' + st_monster.name.upper()
    st_monster.attack = st_monster.attack + 8
    st_monster.shield = st_monster.shield
    st_monster.hp = st_monster.hp + 20
    st_monster.agility = st_monster.agility
    return st_monster

def furious(st_monster):
    st_monster.name = 'FURIOUS ' + st_monster.name.upper()
    st_monster.attack = st_monster.attack + 10
    st_monster.shield = st_monster.shield + 10
    st_monster.hp = st_monster.hp + 30
    st_monster.agility = st_monster.agility
    return st_monster

class AfterDeathAction:
    _registry = dict()

    def __init_subclass__(cls, **kwargs):
        AfterDeathAction._registry[cls.__name__] = cls

    def to_json(self) -> dict:
        return {'cls': self.__class__.__name__, **self.__dict__}

    @classmethod
    def from_json(cls, data: dict) -> 'AfterDeathAction':
        class_name = data.pop('cls')
        cls_ = cls._registry[class_name]
        return cls_(**data)


class ExplosionMod(AfterDeathAction):
    def __init__(self, hp=50):
        self.hp = hp

    def execute(self, game_state):
        game_state.UI.say('The monster blowing up in the room!!!')
        game_state.player.take_damage(self.hp, game_state, death=False)
        return game_state