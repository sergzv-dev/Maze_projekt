from treasures import QuestItem, Key, ImmortalAmulet
from boxes import LootBox
import random
import uuid


class Quest():
    def to_json(self):
        pass

    @staticmethod
    def from_json(sign):
        pass


class MainQuest(Quest):
    @staticmethod
    def add_quest(world):
        rooms_dict = world.rooms_dict
        id_ = str(uuid.uuid4())
        end_g_key = Key(id_)
        end_door = QuestObject('EndDoor', id_)
        end_room = random.choice([room for room in rooms_dict.values() if room.quest is None])
        end_room.quest = end_door
        key_room = random.choice(list(rooms_dict.values()))
        key_room.box = LootBox(end_g_key)
        return world

class ImmortalAmuletQuest(Quest):
    @staticmethod
    def add_quest(world):
        from map_builder import WorldBuilder

        rooms_dict = world.rooms_dict
        id_ = str(uuid.uuid4())
        amulet = ImmortalAmulet(id_)
        altar = QuestObject('ImmortalAltar', id_)
        altar_room = random.choice([room for room in rooms_dict.values() if room.quest is None])
        altar_room.quest = altar
        amulet_room = random.choice(list(rooms_dict.values()))
        amulet_room.monster = WorldBuilder.get_random_monster(amulet)
        return world

class QuestObject():
    def __init__(self, sing, id_):
        self.sing = sing
        self.id_ = id_

    def take_key(self, game_state):
        player = game_state.player
        quest_items = [item for item in player.back_pack if isinstance(item, QuestItem)]
        if quest_items:
            for key in quest_items:
                if key.id_ == self.id_:
                    return key
        return None