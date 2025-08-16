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

    def heal_hp(self, value):
        self.hp = min(self.max_hp, self.hp + value)

    def get_damage(self, value, *, death = True):
        min_hp = -1
        if not death and self.hp != 1: min_hp = 1
        self.hp = max(min_hp, self.hp - value)

    def increase_spec(self, spec, value):
        max_val = float('inf')
        if spec == 'shield': max_val = self.max_shield
        if spec == 'hp': max_val = self.max_hp
        setattr(self, spec, min(max_val, getattr(self, spec) + value))

    def reduce_spec(self, spec, value):
        min_val = 1
        setattr(self, spec, max(min_val, getattr(self, spec) - value))


class Player(Creature):
    def __init__(self, name, attack = 10, shield = 20, hp = 100, agility = 5):
        super().__init__(name, attack, shield, hp, agility)
        self.open_bp = False


class Monster(Creature):
    def __init__(self, name, attack, shield, hp, agility, room, loot = None):
        super().__init__(name, attack, shield, hp, agility)
        self.room = room
        if loot is not None:
            self.back_pack.append(loot)

    def get_damage(self, value, *, death = True):
        super().get_damage(value)
        self.death_chek()

    def death_chek(self):
        if self.hp < 1:
            self.room.loot += self.back_pack
            self.room.monster = None

    def __repr__(self):
        return f'{self.name}'