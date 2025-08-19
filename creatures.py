''' Module contains classes for player and monsters'''

class Creature():
    def __init__(self, name, attack, shield, hp, agility):
        self.name = name
        self.attack = attack
        self.shield = shield
        self.max_shield = shield
        if isinstance(self, Player): self.max_shield = 25
        self.hp = hp
        self.max_hp = 100
        self.agility = agility
        self.back_pack = []
        self.death_marker = False

    def heal_hp(self, value):
        self.hp = min(self.max_hp, self.hp + value)

    def take_damage(self, value, game_state, *, death = True):
        min_hp = -1
        ui = game_state.UI
        if not death and self.hp != 1: min_hp = 1
        damage = round(value*(1- self.shield/100))
        self.hp = max(min_hp, self.hp - damage)
        ui.say(f'{self.name} received damage: {damage}')
        self.death_chek(game_state)

    def increase_spec(self, spec, value):
        max_val = float('inf')
        if spec == 'shield': max_val = self.max_shield
        if spec == 'hp': max_val = self.max_hp
        setattr(self, spec, min(max_val, getattr(self, spec) + value))

    def reduce_spec(self, spec, value):
        min_val = 1
        setattr(self, spec, max(min_val, getattr(self, spec) - value))

    def death_chek(self, game_state):
        pass


class Player(Creature):
    def __init__(self, name, attack = 10, shield = 20, hp = 100, agility = 5):
        super().__init__(name, attack, shield, hp, agility)
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
    def __init__(self, name, attack, shield, hp, agility, room, loot = None):
        super().__init__(name, attack, shield, hp, agility)
        self.room = room
        if loot is not None:
            self.back_pack.append(loot)


    def death_chek(self, game_state):
        if self.hp < 1:
            self.room.loot += self.back_pack
            self.room.monster = None
            game_state.player.fight_marker = False

    def __repr__(self):
        return f'{self.name}'