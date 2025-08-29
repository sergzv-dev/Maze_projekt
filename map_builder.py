''' Module generate and fills the map in the beginning'''

import random
from treasures import (LittleMedicine, MediumMedicine, LargeMedicine, ImproveAttack,
                       ImproveShield, FakePowerBook, SacrificeAmulet, ResilienceMutagen, Bomb,
                       PhoenixAmulet, TrueBookOfPower
                       )
from creatures import (Soldier, Goblin, Mage, Knight, Mimic, undead, beastly, demonic, frozen, cursed,
                       champion, flaming, furious)
from boxes import LootBox
from room import Room

class World:
    def __init__(self, rooms_dict):
        self.rooms_dict = rooms_dict

class WorldBuilder:
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
        amount_of_monsters(self.rooms_dict)
        amount_of_boxes(self.rooms_dict)


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
        for room in list(self.rooms_dict.values()):
            loot = None
            if random.randint(1, 4) == 1:
                if random.randint(1, 3) == 1:
                    loot = self.get_random_treasure(self.treasures_list)
                room.monster = self.get_random_monster(loot)
        

    def add_loot(self):
        for room in list(self.rooms_dict.values()):
            if random.randint(1, 3) == 1:
                room.box = LootBox(self.get_random_treasure(self.treasures_list))


    @staticmethod
    def get_random_treasure(treasures_list):
        treas_choose = []
        for treas_clss_obj in treasures_list:
            treas_item = treas_clss_obj()
            treas_choose += [treas_item] * treas_item.rarity
        return random.choice(treas_choose)


    @staticmethod
    def get_random_monster(loot = None):
        creature = random.choice([Soldier, Goblin, Mage, Knight, Mimic])
        strong = random.choice([undead, beastly, demonic, frozen, cursed])
        super_m = random.choice([champion, flaming, furious])
        monster = creature(loot)
        if random.randint(1,3) == 1:
            monster = strong(monster)
            if random.randint(1,5) == 1:
                monster = super_m(monster)
        return monster

    @staticmethod
    def give_world(x_line, y_line):
        world = WorldBuilder(x_line, y_line)
        return world.rooms_dict


def amount_of_monsters(rooms_dict):
    monsters = len([1 for room in rooms_dict.values() if room.monster])
    return print(f'amount of monsters {monsters}')

def amount_of_boxes(rooms_dict):
    boxes = len([1 for room in rooms_dict.values() if room.box])
    return print(f'amount of boxes {boxes}')

