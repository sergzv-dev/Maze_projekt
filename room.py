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
        pass

    @staticmethod
    def from_json(name, room_data):
        pass

def name_convert(name):
    if isinstance(name, tuple):
        return f'{chr(name[0] + 64)}{str(name[1])}'
    if isinstance(name, str):
        return ord(name[0]) - 64, int(name[1:])
    raise TypeError('"name" must be srt or tuple')