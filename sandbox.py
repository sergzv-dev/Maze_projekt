class Creature:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.name = 'monster'

    def get_name(self):
        return  self.name


class Knight(Creature):
    def __init__(self):
        super().__init__()
        self.x = 2
        self.name = 'Knight'

    def get_name(self):
        return self.name + 'beastly'


class Ghost(Creature):
    def __init__(self):
        super().__init__()
        self.y = 3
        self.name = 'Ghost'


class Wrapper:
    def __init__(self, monster):
        m_class = monster.__class__
        class SuperMonster(m_class):
            def __init__(self, in_monster):
                super().__init__()
                self.x = in_monster.x + 10
                self.name = in_monster.name + 'Super'
        self.creature = SuperMonster(monster)
        self.__class__ = SuperMonster
        self.__init__(monster)

monster = Knight()
print(monster.get_name())
super_m = Wrapper(monster)
print(super_m.get_name())

monster = Ghost()
print(monster.get_name())
super_m = Wrapper(monster)
print(super_m.get_name())