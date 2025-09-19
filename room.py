''' Module contains room class and name_convert function'''
from item_container import ItemContainer
from my_object import MyObject

class Room(MyObject):
    def __init__(self, name: tuple):
        self.name = name
        self.doors = []
        self.monster = None
        self.loot = ItemContainer()
        self.box = None
        self.room_searched = False
        self.quest = None

    def __repr__(self):
        return name_convert(self.name)

    # def to_json(self):
    #     data = self.__dict__.copy()
    #     if self.monster:
    #         data['monster'] = self.monster.to_json()
    #     if self.box:
    #         data['box'] = self.box.to_json()
    #     if self.quest:
    #         data['quest'] = self.quest.to_json()
    #     data['loot'] = self.loot.to_json()
    #     return data

    @classmethod
    def from_json(cls, room_data):
        from creatures import Monster
        from quests import QuestObject
        from boxes import LootBox

        name = tuple(room_data['name'])
        doors = [tuple(door) for door in room_data['doors']]
        monster = room_data['monster']
        loot = room_data['loot']
        box = room_data['box']
        quest = room_data['quest']

        room = cls(name)
        room.doors = doors
        if monster:
            room.monster = Monster.from_json(monster)
        room.loot = ItemContainer.from_json(loot)
        if box:
            room.box = LootBox.from_json(box)
        room.room_searched = room_data['room_searched']
        if quest:
            room.quest = QuestObject.from_json(quest)
        return room

def name_convert(name):
    if isinstance(name, tuple):
        return f'{chr(name[0] + 64)}{str(name[1])}'
    if isinstance(name, str):
        return ord(name[0]) - 64, int(name[1:])
    raise TypeError('"name" must be srt or tuple')