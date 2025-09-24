from abstractions import Treasure

class ItemContainer(list):
    def to_json(self) -> list[dict]:
        return [item.to_json() for item in self]

    @classmethod
    def from_json(cls, data):
        return cls([Treasure.from_json(item_data) for item_data in data])