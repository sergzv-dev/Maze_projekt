class LootBox():
    def __init__(self, loot):
        self.loot = loot

    def __repr__(self):
        return 'box'

    def to_json(self):
        pass

    @staticmethod
    def from_json(box_data):
        pass