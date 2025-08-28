# class Creature:
#     def __init__(self):
#         self.x = 1
#         self.y = 1
#         self.name = 'monster'
#
#     def get_name(self):
#         return  self.name
#
#
# class Knight(Creature):
#     def __init__(self):
#         super().__init__()
#         self.x = 2
#         self.name = 'Knight'
#
#     def get_name(self):
#         return self.name + 'beastly'
#
#
# class Ghost(Creature):
#     def __init__(self):
#         super().__init__()
#         self.y = 3
#         self.name = 'Ghost'
#
#
# class Wrapper:
#     def __init__(self, monster):
#         m_class = monster.__class__
#         class SuperMonster(m_class):
#             def __init__(self, in_monster):
#                 super().__init__()
#                 self.x = in_monster.x + 10
#                 self.name = in_monster.name + 'Super'
#         self.creature = SuperMonster(monster)
#         self.__class__ = SuperMonster
#         self.__init__(monster)
#
# monster = Knight()
# print(monster.get_name())
# super_m = Wrapper(monster)
# print(super_m.get_name())
#
# monster = Ghost()
# print(monster.get_name())
# super_m = Wrapper(monster)
# print(super_m.get_name())



import  json

# list_ = {'Alise': 'orange', 'Piter': 'appel'}
# jsn_data = json.dumps(list_)
#
# file = '/Users/serg/Projects/Python learning/test files/test.txt'
#
# with open(file, 'w+') as f:
#     f.write(jsn_data)
#
# with open(file, 'r') as f:
#     data = f.read()

# f_data = open(file, 'w+')
# f_data.write(jsn_data)
# f_data.close()
#
# f_data = open(file, 'r+')
# data = f_data.read()
# f_data.close()
#
# new_data = json.loads(data)
# print(f'{new_data['Alise']}')

class Player():
    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.attack = kwargs.get('attack', 10)
        self.max_attack = kwargs.get('max_attack', 100)
        self.shield = kwargs.get('shield', 10)
        self.max_shield = kwargs.get('max_shield', 50)
        self.hp = kwargs.get('hp', 100)
        self.max_hp = kwargs.get('max_hp', 100)
        self.agility = kwargs.get('agility', 5)
        self.max_agility = kwargs.get('max_agility', 40)
        self.fight_marker = False
        self.open_bp = False

    def get_name(self):
        return f'{self.name}'

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(data):
        specs = json.loads(data)
        name = specs.pop('name')
        fight_marker = specs.pop('fight_marker')
        open_bp = specs.pop('open_bp')
        player = Player(name, **specs)
        player.fight_marker = fight_marker
        player.open_bp = open_bp
        return player

lol = Player('lol')
print(lol.to_json())

data_pl = lol.to_json()
vov = Player.from_json(data_pl)
print(vov.get_name())



# ////////////////////////////////////////////////////////

# class Creature:
#     def __init__(self, name='monster', x=1, y=1):
#         self.x = x
#         self.y = y
#         self.name = name
#
#     def get_name(self):
#         return self.name
#
#     def on_death(self, game_state):
#         pass
#
#
# class Knight(Creature):
#     def __init__(self):
#         super().__init__(name='Knight', x=2)
#
#     def get_name(self):
#         return self.name + 'beastly'
#
#
# class Ghost(Creature):
#     def __init__(self):
#         super().__init__(name='Ghost', y=3)
#
#
# def buggy_make_super(cls: type) -> type:
#     old_init = cls.__init__
#     def __init__(self, *args, **kwargs):
#         old_init(self, *args, **kwargs)
#
#         self.x = self.x + 10
#         self.name = self.name + 'Super'
#
#     cls.__init__ = __init__
#     return cls
#
#
# def make_super(cls: type) -> type:
#     class Upgraded(cls):
#         def __init__(self, *args, **kwargs):
#             # print(f'about to call {super()=} {super().__init__=}')
#             super().__init__(*args, **kwargs)
#
#             self.x = self.x + 10
#             self.name = self.name + 'Super'
#
#     Upgraded.__name__ = cls.__name__
#     return Upgraded
#
#
# def make_explosive(cls: type) -> type:
#     class Upgraded(cls):
#         def __init__(self, *args, **kwargs):
#             # print(f'about to call {super()=} {super().__init__=}')
#             super().__init__(*args, **kwargs)
#
#         def on_death(self, game_state):
#             print("EXPLOSION!!!!")
#
#     Upgraded.__name__ = cls.__name__
#     return Upgraded
#
#
# def make_explosive_advanced(*, damage: int) -> type:
#     def decorator(cls):
#         class Upgraded(cls):
#             def __init__(self, *args, **kwargs):
#                 # print(f'about to call {super()=} {super().__init__=}')
#                 super().__init__(*args, **kwargs)
#
#             def on_death(self, game_state):
#                 print(f"EXPLOSION!!!! {damage=}")
#
#         Upgraded.__name__ = cls.__name__
#         return Upgraded
#     return decorator
#
# @make_super
# class MegaKnight(Knight):
#     pass
#
# @make_explosive
# class SparklingKnight(Knight):
#     pass
#
# @make_explosive_advanced(damage=5)
# class SparklingKnight5(Knight):
#     pass
#
#
# class Wrapper:
#     def __init__(self, monster):
#         m_class = monster.__class__
#         class SuperMonster(m_class):
#             def __init__(self, in_monster):
#                 super().__init__()
#                 self.x = in_monster.x + 10
#                 self.name = in_monster.name + 'Super'
#         self.creature = SuperMonster(monster)
#         self.__class__ = SuperMonster
#         self.__init__(monster)
#
# monster = Knight()
# assert monster.get_name() == "Knightbeastly"
# super_m = Wrapper(monster)
# assert super_m.get_name() == "KnightSuperbeastly"
#
# super_m = make_super(Knight)()
# assert super_m.get_name() == "KnightSuperbeastly"
#
#
# monster = Ghost()
# assert monster.get_name() == "Ghost"
# super_m = Wrapper(monster)
# assert super_m.get_name() == "GhostSuper"
#
# super_m = make_super(Ghost)()
# assert super_m.get_name() == "GhostSuper"
#
#
#
# # можно задекорировать класс целиком - как MegaKnight
# # можно на лету и точечно вкладывать в класс функциональность - как make_explosive(Ghost)
# monster_cls = [Creature, Knight, Ghost, buggy_make_super(Ghost), make_super(Knight), MegaKnight, SparklingKnight, make_explosive(Ghost), SparklingKnight5 ]
#
# for cls in monster_cls:
#     monster = cls()
#     print( cls, monster.get_name(), type(monster) )
#     monster.on_death(game_state=None)

# mon = Knight()
# print(mon.get_name())
#
#
# @buggy_make_super
# class DegaKnight(Knight):
#     pass
#
# lis = DegaKnight()
# print(lis.get_name())
#
# pip = DegaKnight()
# print(pip.get_name())