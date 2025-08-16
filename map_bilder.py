''' Module generate and fills the map in the beginning'''

import random
from treasures import (LittleMedicine, MediumMedicine, LargeMedicine, ImproveAttack,
                       ImproveShield, FakePowerBook, SacrificeAmulet, Key, ResilienceMutagen, Bomb,
                       PhoenixAmulet, TrueBookOfPower
                       )
from creatures import Monster
from loot_box import LootBox
from room import Room

class World():
    def __init__(self, x_line, y_line):
        self.size = (x_line, y_line)
        self.x_line = x_line
        self.y_line = y_line
        self.rooms_dict = dict()
        self.treasures_list = [LittleMedicine, MediumMedicine, LargeMedicine, ImproveAttack,
                               ImproveShield, FakePowerBook, SacrificeAmulet, ResilienceMutagen, Bomb,
                               PhoenixAmulet, TrueBookOfPower
                               ]
        self.map_builder()
        self.doors_builder()
        self.add_monster()
        self.add_loot()

    def map_builder(self):
        for x in range(1, self.x_line+1):
            self.rooms_dict.update({(x, y): Room((x, y)) for y in range(1, self.y_line+1)})

    def doors_builder(self):
        for x, y in self.rooms_dict:
            doors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
            for num in doors:
                door = self.rooms_dict.get(num)
                if door is not None:
                    self.rooms_dict[(x, y)].doors.append(door)

    def add_monster(self):
        add_func = lambda spec, impact: {key: impact.get(key, lambda x: x)(value) for key, value in spec.items()}
        for room in list(self.rooms_dict.values()):
            creature = None
            loot = None
            if random.randint(1, 4) == 1:
                creature = NewMonster.up_monster()
                if random.randint(1, 2) == 1:
                    creature = add_func(creature, NewMonster.up_name())
                    if random.randint(1, 5) == 1:
                        creature = add_func(creature, NewMonster.up_super())
            if creature is not None:
                if random.randint(1, 3) == 1:
                    loot = self.give_treasure(self.treasures_list)
                room.monster = Monster(
                    creature['name'], creature['attack'], creature['shield'], creature['hp'],
                    creature['agility'], room, loot
                )

    def add_loot(self):
        for room in list(self.rooms_dict.values()):
            if random.randint(1, 3) == 1:
                room.box = LootBox(self.give_treasure(self.treasures_list))


    @staticmethod
    def give_treasure(treasures_list):
        treas_choose = []
        for treas_clss_obj in treasures_list:
            treas_item = treas_clss_obj()
            treas_choose += [treas_item] * treas_item.rarity
        return random.choice(treas_choose)

class NewMonster():
    def give_monster(self, room, loot = None):
        add_func = lambda spec, impact: {key: impact.get(key, lambda x: x)(value) for key, value in spec.items()}
        creature = self.up_monster()
        if random.randint(1, 2) == 1:
            creature = add_func(creature, self.up_name())
            if random.randint(1, 5) == 1:
                creature = add_func(creature, self.up_super())
        return Monster(creature['name'], creature['attack'], creature['shield'], creature['hp'],
                       creature['agility'], room, loot
                       )

    @staticmethod
    def up_monster():
        soldier = {'name': 'soldier', 'attack': 15, 'shield': 10, 'hp': 30, 'agility': 2}
        goblin = {'name': 'goblin', 'attack': 10, 'shield': 5, 'hp': 25, 'agility': 3}
        mage = {'name': 'mage', 'attack': 20, 'shield': 5, 'hp': 20, 'agility': 5}
        knight = {'name': 'knight', 'attack': 10, 'shield': 20, 'hp': 50, 'agility': 0}
        mimic = {'name': 'mimic', 'attack': 30, 'shield': 5, 'hp': 15, 'agility': 0}
        return random.choice((soldier, goblin, mage, knight, mimic))

    @staticmethod
    def up_name():
        undead = {'name': lambda x: 'undead '+x, 'attack': lambda x: x-5, 'hp': lambda x: x+15}
        beasty = {'name': lambda x: 'beasty '+x, 'attack': lambda x: x+5, 'agility': lambda x: x+5}
        demonic = {'name': lambda x: 'demonic '+x, 'shield': lambda x: x+30, 'hp': lambda x: x-5}
        frozen = {'name': lambda x: 'frozen '+x, 'hp': lambda x: x+30, 'agility': lambda x: 0}
        cursed = {'name': lambda x: 'cursed '+x, 'attack': lambda x: x-5, 'hp': lambda x: x-10}
        return random.choice((undead, beasty, demonic, frozen, cursed))

    @staticmethod
    def up_super():
        champion = {'name': lambda x: ('champion '+x).upper(), 'shield': lambda x: x+20, 'hp': lambda x: x+20}
        flaming = {'name': lambda x: ('flaming '+x).upper(), 'attack': lambda x: x+30}
        furious = {'name': lambda x: ('furious '+x).upper(), 'shield': lambda x: x+30}
        return random.choice((champion, flaming, furious))