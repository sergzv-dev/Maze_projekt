from abstractions import MyObject, Treasure

class LootBox(MyObject):
    def __init__(self, loot):
        self.loot = loot

    def __repr__(self):
        return 'box'

    @classmethod
    def from_json(cls, box_data):
        box = cls(Treasure.from_json(box_data['loot']))
        return box