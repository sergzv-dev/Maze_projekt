
class UI():

    def ask(self, text):
        answer = input(text)
        return answer

    def offer(self, question, options):
        creat_opt = '\n'.join(f'{i}: {num+1}' for num, i in enumerate(options))
        pick = input(f'{question}\n{creat_opt}\n...')
        options[pick-1]()

    def say(self, text):
        print(text)


def game():
    master = UI()
    world = Map_bilder(10, 10)
    name = master.ask('Enter your name: ')
    stranger = Player(name)
    master.say(f'Hello {stranger.name}')
    while True:
        stranger.options

class Game_states():
    def __init__(self):
        self.name = None
        self.pl_state = dict()
        self.backpack = []
        self.curr_room = None
        self.x_size = 0
        self.y_size = 0


class Access_state():
    def __init__(self):
        self.state = Game_states()

    def get_name(self):
        return self.state.name

    def set_name(self, name):
        self.state.name = name

    def get_plst(self):
        return self.state.pl_state

    def change_plst(self, new_states):
        self.state.pl_state = new_states

    def get_bp(self):
        return self.state.backpack

    def change_bp(self, new_bp):
        self.state.backpack = new_bp

    def set_x(self, x):
        self.state.x_size = x

    def get_x(self):
        return self.state.x_size

    def set_y(self, y):
        self.state.y_size = y

    def get_y(self):
        return self.state.y_size

    def get_room(self):
        return self.state.curr_room

    def get_curr_room(self):
        return self.state.curr_room

    def change_room(self, new_room):
        self.state.curr_room = new_room


class Action():
    def __init__(self):
        self.master = UI()
        self.access = Access_state()

    def move(self):
        room = self.access.get_curr_room()
        self.master.offer('Which direction will you choose?', room.doors)

    def attack(self, pl_state, m_state):
        pass
    def get_itm(self, itm, pl_inv):
        pass

import itertools as it

class Rooms():
    def __init__(self, x, y):
        self.access = Access_state()
        self.name = str(x) + str(y)
        self.x = x
        self.y = y
        self.opt = []
        self.doors = []
        Rooms.doors(self)

    def options(self):
        return self.opt

    def doors(self):
        x_option = filter(lambda num: 0 < num <= self.access.get_x(), (self.x + 1, self.x - 1,))
        y_option = filter(lambda num: 0 < num <= self.access.get_y(), (self.y + 1, self.y - 1,))
        self.doors = [f'{room[0]}{room[1]}' for room in it.product(x_option, y_option)]


class Map_bilder():
    def __init__(self, x_line, y_line):
        self.access = Access_state()
        self.access.set_x(x_line)
        self.x_line = self.access.get_x()
        self.access.set_y(y_line)
        self.y_line = self.access.get_y()
        self.rooms_dict = dict()
        Map_bilder.map_builder(self)
        self.access.change_room('11')

    def map_builder(self):
        for x in range(1, self.x_line+1):
            self.rooms_dict.update({f'{str(x)}{str(y)}': Rooms(x,y) for y in range(1, self.y_line+1)})



import random

class Creature():
    def __iadd__(self, other):
        self.value = {key: other.get(key, lambda x: x)(value) for key, value in self.items()}
        return self


class Player(Creature):

    def __init__(self, name):
        self.access = Access_state()
        self.action = Action()
        self.access.set_name(name)
        self.name = self.access.get_name()
        self.state = {'name': self.name, 'attack': 10, 'shield': 10, 'hp': 100, 'agility': 1}
        self.backpack = []
        self.opt = [self.action.move()]

    def state(self, impact):
        self.state += impact
        return self.state

    def backpack(self):
        return self.backpack

    @property
    def options(self):
        return self.opt


class Monster(Creature):

    @property
    def up_monster(self):
        soldier = {'name': 'soldier', 'attack': 15, 'shield': 10, 'hp': 30, 'agility': 2}
        goblin = {'name': 'goblin', 'attack': 10, 'shield': 5, 'hp': 25, 'agility': 3}
        mage = {'name': 'mage', 'attack': 20, 'shield': 5, 'hp': 20, 'agility': 5}
        knight = {'name': 'knight', 'attack': 10, 'shield': 20, 'hp': 50, 'agility': 0}
        mimic = {'name': 'mimic', 'attack': 30, 'shield': 5, 'hp': 15, 'agility': 0}
        return random.choice((soldier, goblin, mage, knight, mimic))

    @property
    def up_name(self):
        undead = {'name': lambda x: 'undead '+x, 'attack': lambda x: x-5, 'hp': lambda x: x+15}
        beasty = {'name': lambda x: 'beasty '+x, 'attack': lambda x: x+5, 'agility': lambda x: x+5}
        demonic = {'name': lambda x: 'demonic '+x, 'shield': lambda x: x+30, 'hp': lambda x: x-5}
        frozen = {'name': lambda x: 'frozen '+x, 'hp': lambda x: x+30, 'agility': lambda x: 0}
        cursed = {'name': lambda x: 'cursed '+x, 'attack': lambda x: x-5, 'hp': lambda x: x-10}
        return random.choice((undead, beasty, demonic, frozen, cursed))

    @property
    def up_super(self):
        champion = {'name': lambda x: ('champion '+x).upper(), 'shield': lambda x: x+20, 'hp': lambda x: x+20}
        flaming = {'name': lambda x: ('flaming '+x).upper(), 'attack': lambda x: x+30}
        furious = {'name': lambda x: ('furious '+x).upper(), 'shield': lambda x: x+30}
        return random.choice((champion, flaming, furious))

    def create_monster(self):
        self.creature = Monster.up_monster
        if random.randint(1,2) == 1:
            self.creature += Monster.up_name
            if random.randint(1,5) == 1:
                self.creature += Monster.up_super
        return self.creature


class  Treasure(Creature):

    def choose_treas(self):
        mixture = {'hp': lambda x: x+20}
        false_key = False
        boost_attack = {'attack': lambda x: x+10}
        boost_shield = {'attack': lambda x: x+10}
        boost_agility = {'agility': lambda x: x+2}
        empty_box = None
        key = True
        super_shield = {'agility': lambda x: 10}

        if random.randint(1,2) == 1:
            treas = random.choice((mixture, false_key, boost_attack, boost_shield, boost_agility))
        elif random.randint(1,5) == 1:
            treas = random.choice((key, super_shield))
        else: treas = empty_box
        return treas

#def modify(specs, modifier):
    #return {key: modifier.get(key, lambda x: x)(value) for key, value in specs.items()}

#rooms_list.update({f'{chr(let)}{str(num)}': Rooms(chr(let), num) for num in range(1, y_line + 1)})

game()