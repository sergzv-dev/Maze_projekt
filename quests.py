from treasures import Key, ImmortalAmulet
from actions import EndDoorAction, ImmortalAltarAction
from loot_box import LootBox
import random
from map_bilder import NewMonster

class MainQuest():
    def __init__(self, world):
        self.rooms_dict = world.rooms_dict
        end_g_key = Key('Golden key')
        end_room = random.choice(list(self.rooms_dict.values()))
        end_room.actions.append(EndDoorAction(end_g_key))
        key_room = random.choice(list(self.rooms_dict.values()))
        key_room.box = LootBox(end_g_key)

class ImmortalAmuletQuest():
    def __init__(self, world):
        self.rooms_dict = world.rooms_dict
        amulet = ImmortalAmulet()
        altar_room = random.choice(list(self.rooms_dict.values()))
        altar_room.actions.append(ImmortalAltarAction(amulet))
        amulet_room = random.choice(list(self.rooms_dict.values()))
        amulet_room.monster = NewMonster.give_monster(amulet_room, amulet)
