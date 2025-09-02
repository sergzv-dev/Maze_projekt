class LootBox():
    def __init__(self, loot):
        self.loot = loot

    def __repr__(self):
        return 'box'

    def to_json(self):
        return self.loot.to_json()

    @staticmethod
    def from_json(box_data):
        from treasures import take_treasure_item
        box = LootBox(take_treasure_item(box_data))
        return box