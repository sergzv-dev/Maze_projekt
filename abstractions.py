class MyObject:
    def to_json(self):
        data = self.__dict__.copy()
        for key in data:
            value = data[key]
            if hasattr(value, 'to_json'):
                data[key] = value.to_json()
        data.update({'cls': self.__class__.__name__})
        return data


class Action(MyObject):
    _registry = dict()

    def execute(self, game_state):
        pass

    def __init_subclass__(cls, **kwargs):
        Action._registry[cls.__name__] = cls

    @classmethod
    def take_class_from_reg(cls, class_name):
        return cls._registry[class_name]


class QuestAction(Action):
    pass

class Treasure(Action):
    _registry = dict()
    rarity = 1
    mode = 'default'

    def __init_subclass__(cls, **kwargs):
        Treasure._registry[cls.__name__] = cls

    @classmethod
    def from_json(cls, data: dict) -> 'Treasure':
        class_name = data.pop('cls')
        cls_ = cls._registry[class_name]
        return cls_(**data)


class QuestItem(Treasure):
    mode = 'quest'
    answer = '42'

    def __init__(self, *, id_, name='quest treasure'):
        self.name = name
        self.id_ = id_

    def execute(self, game_state):
        ui = game_state.UI
        ui.say(self.answer)
        return game_state

    def __repr__(self):
        return self.name