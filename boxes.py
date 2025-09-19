from my_object import MyObject

class LootBox(MyObject):
    def __init__(self, loot):
        self.loot = loot

    def __repr__(self):
        return 'box'

    # def to_json(self):
    #     return self.loot.to_json()

    @classmethod
    def from_json(cls, box_data):
        from treasures import Treasure
        box = cls(Treasure.from_json(box_data['loot']))
        return box