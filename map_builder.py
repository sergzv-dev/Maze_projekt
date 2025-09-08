''' Module generate and fills the map in the beginning'''

import random
from treasures import (LittleMedicine, MediumMedicine, LargeMedicine, ImproveAttack,
                       ImproveShield, FakePowerBook, SacrificeAmulet, ResilienceMutagen, Bomb,
                       PhoenixAmulet, TrueBookOfPower
                       )
from creatures import (Soldier, Goblin, Mage, Knight, Mimic, undead, beastly, demonic, frozen, cursed,
                       champion, flaming, furious)
from room import Room, name_convert

class World:
    def __init__(self, rooms_dict=None):
        self.rooms_dict = rooms_dict or dict()

    def get_room(self, name: str) -> Room:
        return self.rooms_dict[name_convert(name)]

    def to_json(self):
        return [room.to_json() for room in self.rooms_dict.values()]

    @classmethod
    def from_json(cls, data):
        rooms_dict = dict()
        for room_data in data:
            name = tuple(room_data['name'])
            rooms_dict.update({name: Room.from_json(room_data)})
        return cls(rooms_dict)

    def amount_of_monsters(self):
        return sum([1 for room in self.rooms_dict.values() if room.monster])

    def amount_of_boxes(self):
        return sum([1 for room in self.rooms_dict.values() if room.box])

class WorldBuilder:
    @classmethod
    def build(cls, size_x, size_y, quests: list['Quest']):
        rooms_dict = cls.build_rooms_dict(size_x, size_y)
        rooms_dict = cls.doors_builder(rooms_dict)
        rooms_dict = cls.add_monster(rooms_dict)
        rooms_dict = cls.add_loot(rooms_dict)
        world = World(rooms_dict)

        for quest in quests:
            world = quest.add_quest(world)
        return world

    @staticmethod
    def build_rooms_dict(x_line, y_line):
        rooms = dict()
        for x in range(1, x_line):
            for y in range(1, y_line):
                rooms[(x,y)] = Room((x,y))
        return rooms

    @staticmethod
    def doors_builder(rooms_dict:dict) -> dict:
        for x, y in rooms_dict:
            doors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
            for num in doors:
                door = rooms_dict.get(num)
                if door is not None:
                    rooms_dict[(x, y)].doors.append(num)
        return rooms_dict

    @staticmethod
    def add_monster(rooms_dict, *, monster_probability=0.25, loot_probability=0.33) -> dict:
        for room in rooms_dict.values():
            if random.random() < monster_probability:
                loot = get_random_treasure() if random.random() < loot_probability else None
                room.monster = get_random_monster(loot)
        return rooms_dict
        
    @staticmethod
    def add_loot(rooms_dict, *, dox_probability=0.33):
        from boxes import LootBox
        for room in rooms_dict.values():
            room.box = LootBox(get_random_treasure(bomb_mode=True)) if random.random() < dox_probability else None
        return rooms_dict


def get_random_treasure(bomb_mode=False):
    treasures_list = [LittleMedicine, MediumMedicine, LargeMedicine, ImproveAttack,
                      ImproveShield, FakePowerBook, SacrificeAmulet, ResilienceMutagen,
                      PhoenixAmulet, TrueBookOfPower
                      ]
    if bomb_mode: treasures_list += [Bomb]
    treas_choose = []
    for treas_clss_obj in treasures_list:
        treas_item = treas_clss_obj()
        treas_choose += [treas_item] * treas_item.rarity
    return random.choice(treas_choose)


def get_random_monster(loot = None):
    creature = random.choice([Soldier, Goblin, Mage, Knight, Mimic])
    strong = random.choice([undead, beastly, demonic, frozen, cursed])
    super_m = random.choice([champion, flaming, furious])
    monster = creature(loot)
    if random.random() < 0.33:
        monster = strong(monster)
        if random.random() < 0.2:
            monster = super_m(monster)
    return monster