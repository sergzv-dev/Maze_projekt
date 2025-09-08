class LootBox():
    def __init__(self, loot):
        self.loot = loot

    def __repr__(self):
        return 'box'

    def to_json(self):
        return self.loot.to_json()

    @classmethod
    def from_json(cls, box_data):
        from treasures import take_treasure_item
        box = cls(take_treasure_item(box_data))
        return box