''' Module contains room class and name_convert function'''

class Room():
    def __init__(self, name):
        self.name = name
        self.doors = []
        self.monster = None
        self.loot = []
        self.box = None
        self.room_searched = False
        self.quest = None

    def __repr__(self):
        return name_convert(self.name)

    def to_json(self):
        data = self.__dict__.copy()
        if self.monster is not None:
            data['monster'] = self.monster.to_json()
        if self.box is not None:
            data['box'] = self.box.to_json()
        if self.quest is not None:
            data['quest'] = self.quest.to_json()
        data['loot'] = [item.to_json() for item in self.loot]
        return data

    @classmethod
    def from_json(cls, room_data):
        from creatures import Monster
        from quests import QuestObject
        from treasures import take_treasures_list
        from boxes import LootBox

        name = tuple(room_data.pop('name'))
        doors = [tuple(door) for door in room_data['doors']]
        monster = room_data.pop('monster')
        loot = room_data.pop('loot')
        box = room_data.pop('box')
        quest = room_data.pop('quest')

        room = cls(name)
        room.doors = doors
        if monster:
            room.monster = Monster.from_json(monster)
        room.loot = take_treasures_list(loot)
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