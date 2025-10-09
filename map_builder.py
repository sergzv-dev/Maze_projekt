''' Module generate and fills the map in the beginning'''

import random
from treasures import get_random_treasure
from creatures import get_random_monster
from room import Room, name_convert
from boxes import LootBox

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
        return sum([1 for room in self.rooms_dict.values() if room.monsters])

    def amount_of_boxes(self):
        return sum([1 for room in self.rooms_dict.values() if room.box])

class WorldBuilder:

    def add_rooms(self, size_x: int, size_y: int) -> 'WorldBuilder':
        if size_x * size_y < 4: raise ValueError('The world must contain 4 or more rooms')
        self._add_rooms_params = dict(size_x = size_x, size_y = size_y)
        return self

    def add_monsters(self, *, monster_probability=0.25, loot_probability=0.33) -> 'WorldBuilder':
        self._add_monsters_params = dict(monster_probability=monster_probability, loot_probability=loot_probability)
        return self

    def add_loot(self, *, box_probability=0.33) -> 'WorldBuilder':
        self._add_loot_params = dict(box_probability=box_probability)
        return self

    def add_quests(self, *, quests: list['Quest']) -> 'WorldBuilder':
        self._quests = quests
        return self

    def build(self) -> 'World':
        if not getattr(self, '_add_rooms_params', None): raise AttributeError('You must build rooms')
        rooms_dict = self._build_rooms_dict(**self._add_rooms_params)
        rooms_dict = self._doors_builder(rooms_dict)
        rooms_dict = self._add_monster(rooms_dict, **self._add_monsters_params)
        rooms_dict = self._add_loot(rooms_dict, **self._add_loot_params)
        world = World(rooms_dict)

        for quest in self._quests:
            world = quest.add_quest(world)
        return world

    @staticmethod
    def _build_rooms_dict(size_x, size_y):
        rooms = dict()
        for x in range(1, size_x+1):
            for y in range(1, size_y+1):
                rooms[(x,y)] = Room((x,y))
        return rooms

    @staticmethod
    def _doors_builder(rooms_dict:dict) -> dict:
        for x, y in rooms_dict:
            doors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
            for num in doors:
                door = rooms_dict.get(num)
                if door is not None:
                    rooms_dict[(x, y)].doors.append(num)
        return rooms_dict

    @staticmethod
    def _add_monster(rooms_dict, *, monster_probability=0.25, loot_probability=0.33) -> dict:
        for room in rooms_dict.values():
            while random.random() < monster_probability:
                loot = get_random_treasure() if random.random() < loot_probability else None
                room.monsters.append(get_random_monster(loot))
        return rooms_dict

    @staticmethod
    def _add_loot(rooms_dict, *, box_probability=0.33):
        for room in rooms_dict.values():
            room.box = LootBox(get_random_treasure(bomb_mode=True)) if random.random() < box_probability else None
        return rooms_dict