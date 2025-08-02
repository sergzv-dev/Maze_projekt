''' Module generate and fills the map in the beginning'''

import random
from actions import MoveAction, FightAction, OpenBox
from treasures import (LittleMedicine, MediumMedicine, LargeMedicine, ImproveAttack,
                       ImproveShield, FakePowerBook, VictimAmulet
                       )
from creatures import Monster
from loot_box import LootBox
from room import Room
from doors import EndDoorAction,Key

class World():
    def __init__(self, x_line, y_line):
        self.size = (x_line, y_line)
        self.x_line = x_line
        self.y_line = y_line
        self.rooms_dict = dict()
        self.treasures_list = [LittleMedicine, MediumMedicine, LargeMedicine, ImproveAttack,
                               ImproveShield, FakePowerBook, VictimAmulet
                               ]
        self.map_builder(Room)
        self.doors_builder(self.rooms_dict, MoveAction)
        self.add_monster(self.rooms_dict, NewMonster, Monster, FightAction)
        self.add_loot(self.rooms_dict, self.treasures_list, LootBox, OpenBox)
        self.add_end_game(self.rooms_dict, EndDoorAction, Key, LootBox, OpenBox)

    def map_builder(self, cls_room):
        for x in range(1, self.x_line+1):
            self.rooms_dict.update({(x, y): cls_room((x, y)) for y in range(1, self.y_line+1)})

    @staticmethod
    def doors_builder(rooms_dict, action):
        for x, y in rooms_dict:
            doors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
            for num in doors:
                door = rooms_dict.get(num)
                if door is not None:
                    rooms_dict[(x, y)].actions.append(action(door))

    @staticmethod
    def add_monster(rooms_dict, new_monster, monster, fight):
        creature = None
        add_func = lambda spec, impact: {key: impact.get(key, lambda x: x)(value) for key, value in spec.items()}
        for room in list(rooms_dict.values()):
            if random.randint(1, 4) == 1:
                creature = new_monster.up_monster()
                if random.randint(1, 2) == 1:
                    creature = add_func(creature, new_monster.up_name())
                    if random.randint(1, 5) == 1:
                        creature = add_func(creature, new_monster.up_super())
            if creature is not None:
                room.monster = monster(
                    creature['name'], creature['attack'], creature['shield'], creature['hp'], creature['agility']
                )
                room.hidden_actions.append(fight())

    @staticmethod
    def add_loot(rooms_dict, treasures_list, box, open_box):
        for room in list(rooms_dict.values()):
            if random.randint(1, 3) == 1:
                treas_choose = []
                for treas_clss_obj in treasures_list:
                    treas_item = treas_clss_obj()
                    treas_choose += [treas_item] * treas_item.rarity
                treasure = random.choice(treas_choose)
                room.box = box(treasure)
                room.hidden_actions.append(open_box())

    @staticmethod
    def add_end_game(rooms_dict, door, key, box, open_box):
        end_room = random.choice(list(rooms_dict.values()))
        end_room.hidden_actions.append(door())
        key_room = random.choice(list(rooms_dict.values()))

        if key_room.box is not None:
            key_room.box = box(key(1))
        else:
            key_room.box = box(key(1))
            key_room.hidden_actions.append(open_box())

class NewMonster():
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