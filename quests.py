from treasures import Key, ImmortalAmulet
from boxes import LootBox, Lock
import random

class MainQuest():
    @staticmethod
    def add_quest(world):
        rooms_dict = world.rooms_dict
        end_g_key = Key('Golden key')
        end_room = random.choice(list(rooms_dict.values()))
        end_room.end_door = Lock(end_g_key)
        key_room = random.choice(list(rooms_dict.values()))
        key_room.box = LootBox(end_g_key)
        return world

class ImmortalAmuletQuest():
    @staticmethod
    def add_quest(world):
        rooms_dict = world.rooms_dict
        amulet = ImmortalAmulet()
        altar_room = random.choice(list(rooms_dict.values()))
        altar_room.phoenix_altar = Lock(amulet)
        amulet_room = random.choice(list(rooms_dict.values()))
        amulet_room.monster = world.get_random_monster(amulet)
        return world