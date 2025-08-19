from treasures import Key, ImmortalAmulet
from actions import EndDoorAction, ImmortalAltarAction
from loot_box import LootBox
import random

class MainQuest():
    @staticmethod
    def add_quest(world):
        rooms_dict = world.rooms_dict
        end_g_key = Key('Golden key')
        end_room = random.choice(list(rooms_dict.values()))
        end_room.actions.append(EndDoorAction(end_g_key))
        key_room = random.choice(list(rooms_dict.values()))
        key_room.box = LootBox(end_g_key)
        return world

class ImmortalAmuletQuest():
    @staticmethod
    def add_quest(world):
        rooms_dict = world.rooms_dict
        amulet = ImmortalAmulet()
        altar_room = random.choice(list(rooms_dict.values()))
        altar_room.actions.append(ImmortalAltarAction(amulet))
        amulet_room = random.choice(list(rooms_dict.values()))
        amulet_room.monster = world.get_random_monster(amulet)
        return world