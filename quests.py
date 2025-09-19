from treasures import QuestItem, Key, ImmortalAmulet
from boxes import LootBox
from actions import Action, EndDoorAction, ImmortalAltarAction
import random
import uuid
from my_object import MyObject


class Quest():
    pass

class MainQuest(Quest):
    @staticmethod
    def add_quest(world):
        rooms_dict = world.rooms_dict
        id_ = str(uuid.uuid4())
        end_g_key = Key(id_=id_)
        end_door = QuestObject(EndDoorAction, id_)
        end_room = random.choice([room for room in rooms_dict.values() if room.quest is None])
        end_room.quest = end_door
        key_room = random.choice(list(rooms_dict.values()))
        key_room.box = LootBox(end_g_key)
        return world

class ImmortalAmuletQuest(Quest):
    @staticmethod
    def add_quest(world):
        from map_builder import get_random_monster

        rooms_dict = world.rooms_dict
        id_ = str(uuid.uuid4())
        amulet = ImmortalAmulet(id_=id_)
        altar = QuestObject(ImmortalAltarAction, id_)
        altar_room = random.choice([room for room in rooms_dict.values() if room.quest is None])
        altar_room.quest = altar
        amulet_room = random.choice(list(rooms_dict.values()))
        amulet_room.monster = get_random_monster(amulet)
        return world

class QuestObject(MyObject):
    def __init__(self, quest_action, id_):
        self.quest_action = quest_action.__name__
        self.id_ = id_

    def take_key(self, game_state):
        player = game_state.player
        quest_items = [item for item in player.back_pack if isinstance(item, QuestItem)]
        if quest_items:
            for key in quest_items:
                if key.id_ == self.id_:
                    return key

    def get_action(self) -> 'Action':
        return Action.take_class_from_reg(self.quest_action)()

    # def to_json(self):
    #     return self.__dict__.copy()

    @classmethod
    def from_json(cls, data):
        quest_action = Action.take_class_from_reg(data['quest_action'])
        id_ = data['id_']
        return cls(quest_action, id_)