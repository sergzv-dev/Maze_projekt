''' Module contains classes for player and monsters'''

import random

class Creature():
    def __init__(self):
        self.name = None
        self.attack = None
        self.max_attack = None
        self.shield = None
        self.max_shield = None
        self.hp = None
        self.max_hp = None
        self.agility = None
        self.max_agility = None
        self.back_pack = []
        self.death_marker = False

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


class Player(Creature):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.attack = 10
        self.max_attack = 100
        self.shield = 10
        self.max_shield = 50
        self.hp = 100
        self.max_hp = 100
        self.agility = 5
        self.max_agility = 40
        self.fight_marker = False
        self.open_bp = False

    def death_chek(self, game_state):
        last_chance_list = []
        if self.hp < 1:
            last_chance_list = list(filter(lambda item: getattr(item, 'mode', None) == 'raise', self.back_pack))
            self.death_marker = True
        if self.death_marker and last_chance_list:
            last_chance_list[0].last_chance(game_state)


class Monster(Creature):
    def __init__(self, loot = None):
        super().__init__()
        self.max_attack = 999
        self.max_shield = 999
        self.max_hp = 999
        self.max_agility = 999
        if loot is not None:
            self.back_pack.append(loot)

    def death_chek(self, game_state):
        room = game_state.curr_room
        if self.hp < 1:
            room.loot += self.back_pack
            room.monster = None
            game_state.player.fight_marker = False

    def __repr__(self):
        return f'{self.name}'


class Soldier(Monster):
    def __init__(self, loot = None):
        super().__init__(loot)
        self.name = 'Soldier'
        self.attack = 7
        self.shield = 10
        self.hp = 50
        self.agility = 5

class Goblin(Monster):
    def __init__(self, loot = None):
        super().__init__(loot)
        self.name = 'Goblin'
        self.attack = 5
        self.shield = 0
        self.hp = 30
        self.agility = 15

class Mage(Monster):
    def __init__(self, loot = None):
        super().__init__(loot)
        self.name = 'Mage'
        self.attack = 12
        self.shield = 5
        self.hp = 40
        self.agility = 0

class Knight(Monster):
    def __init__(self, loot = None):
        super().__init__(loot)
        self.name = 'Knight'
        self.attack = 9
        self.shield = 20
        self.hp = 70
        self.agility = 5

class Mimic(Monster):
    def __init__(self, loot = None):
        super().__init__(loot)
        self.name = 'Mimic'
        self.attack = 8
        self.shield = 15
        self.hp = 60
        self.agility = 10



class StrongMonster(Monster):
    def __init__(self, monster):
        super().__init__()
        self.max_attack = monster.max_attack
        self.max_shield = monster.max_shield
        self.max_hp = monster.max_hp
        self.max_agility = monster.max_agility
        self.back_pack = monster.back_pack

class Undead(StrongMonster):
    def __init__(self, monster):
        super().__init__(monster)
        self.name = 'Undead ' + monster.name
        self.attack = monster.attack + 2
        self.shield = monster.shield + 10
        self.hp = monster.hp + 20
        self.agility = monster.agility

class Beastly(StrongMonster):
    def __init__(self, monster):
        super().__init__(monster)
        self.name = 'Beastly ' + monster.name
        self.attack = monster.attack + 3
        self.shield = monster.shield
        self.hp = monster.hp + 15
        self.agility = monster.agility + 5

class Demonic(StrongMonster):
    def __init__(self, monster):
        super().__init__(monster)
        self.name = 'Demonic ' + monster.name
        self.attack = monster.attack + 5
        self.shield = monster.shield + 5
        self.hp = monster.hp + 30
        self.agility = monster.agility + 5

    def death_chek(self, game_state):
        room = game_state.curr_room
        ui = game_state.UI
        player = game_state.player
        if self.hp < 1:
            room.loot += self.back_pack
            room.monster = None
            ui.say('The monster blowing up in the room!!!')
            player.take_damage(50, game_state, death=False)
            game_state.player.fight_marker = False

class Frozen(StrongMonster):
    def __init__(self, monster):
        super().__init__(monster)
        self.name = 'Frozen ' + monster.name
        self.attack = monster.attack
        self.shield = monster.shield + 15
        self.hp = monster.hp + 10
        self.agility = max(0, monster.agility - 5)

class Cursed(StrongMonster):
    def __init__(self, monster):
        super().__init__(monster)
        self.name = 'Cursed ' + monster.name
        self.attack = monster.attack + 4
        self.shield = monster.shield
        self.hp = monster.hp + 10
        self.agility = max(0, monster.agility - 5)


class SuperMonster(StrongMonster):
    pass

class Champion(SuperMonster):
    def __init__(self, st_monster):
        super().__init__(st_monster)
        self.name = 'CHAMPION ' + st_monster.name.upper()
        self.attack = st_monster.attack
        self.shield = st_monster.shield + 20
        self.hp = st_monster.hp + 50
        self.agility = st_monster.agility + 10

class Flaming(SuperMonster):
    def __init__(self, st_monster):
        super().__init__(st_monster)
        self.name = 'FLAMING ' + st_monster.name.upper()
        self.attack = st_monster.attack + 8
        self.shield = st_monster.shield
        self.hp = st_monster.hp + 20
        self.agility = st_monster.agility

class Furious(SuperMonster):
    def __init__(self, st_monster):
        super().__init__(st_monster)
        self.name = 'FURIOUS ' + st_monster.name.upper()
        self.attack = st_monster.attack + 10
        self.shield = st_monster.shield + 10
        self.hp = st_monster.hp + 30
        self.agility = st_monster.agility