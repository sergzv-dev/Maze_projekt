from treasures import Key
from actions import EndDoorAction
from loot_box import LootBox
import random

class MainQuest():
    def __init__(self, world):
        self.rooms_dict = world.rooms_dict
        end_g_key = Key('Golden key')
        end_room = random.choice(list(self.rooms_dict.values()))
        end_room.actions.append(EndDoorAction(end_g_key))
        key_room = random.choice(list(self.rooms_dict.values()))
        key_room.box = LootBox(end_g_key)
