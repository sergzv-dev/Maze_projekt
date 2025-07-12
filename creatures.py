''' Module contains classes for player and monsters'''

from actions import ShowSpecs, OpenBackPack, CloseAction

class Creature():
    def __init__(self, name, attack, shield, hp, agility):
        self.name = name
        self.attack = attack
        self.shield = shield
        self.hp = hp
        self.agility = agility


class Player(Creature):
    def __init__(self, name, attack = 10, shield = 20, hp = 100, agility = 5):
        super().__init__(name, attack, shield, hp, agility)
        self.actions = [ShowSpecs(), OpenBackPack()]
        self.back_pack = [CloseAction()]

class Monster(Creature):
    def __repr__(self):
        return f'{self.name}'