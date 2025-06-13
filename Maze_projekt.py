
class UI():
    def ask(self, question, options):
        creat_opt = '\n'.join(f'{i}: {num+1}' for num, i in enumerate(options))
        pick = input(f'{question}\n{creat_opt}\n...')
        options[pick-1]()

    def say(self, text):
        print(text)


def game():
    master = UI()
    name = master.ask('Enter your name: ')
    stranger = Player(name)
    master.say(f'Hello {stranger.name}')
    while True:
        master.ask('What will you do?', stranger.options+stranger.curr_room.options)


class Action():
    def move(self, direction):
        pass
    def attack(self, pl_state, m_state):
        pass
    def get_itm(self, itm, pl_inv):
        pass


class Rooms():
    def __init__(self, let, num):
        self.name = let + str(num)
        self.opt = []
        self.doors = []

    @property
    def options(self):
        return self.opt

    def doors(self):
        return self.doors

def map_builder(x_line, y_line):
    rooms_list = dict()
    for let in range(65, x_line+65):
        rooms_list.update({f'{chr(let)}{str(num)}': Rooms(chr(let),num) for num in range(1, y_line+1)})
    return rooms_list


class Creature():
    def __iadd__(self, other):
        self.value = {key: other.get(key, lambda x: x)(value) for key, value in self.items()}
        return self


class Player(Creature):

    def __init__(self, name):
        self.name = name
        self.state = {'name': self.name, 'attack': 10, 'shield': 10, 'hp': 100, 'agility': 1}
        self.backpack = []
        self.opt = []

    def state(self, impact):
        self.state = modify(self.state, impact)
        return self.state

    def backpack(self):
        return self.backpack

    @property
    def options(self):
        return self.opt




def modify(specs, modifier):
    return {key: modifier.get(key, lambda x: x)(value) for key, value in specs.items()}


import random

def monster():
    soldier = {'name': 'soldier', 'attack': 15, 'shield': 10, 'hp': 30, 'agility': 2}
    goblin = {'name': 'goblin', 'attack': 10, 'shield': 5, 'hp': 25, 'agility': 3}
    mage = {'name': 'mage', 'attack': 20, 'shield': 5, 'hp': 20, 'agility': 5}
    knight = {'name': 'knight', 'attack': 10, 'shield': 20, 'hp': 50, 'agility': 0}
    mimic = {'name': 'mimic', 'attack': 30, 'shield': 5, 'hp': 15, 'agility': 0}

    up_monster = random.choice((soldier, goblin, mage, knight, mimic))

    undead = {'name': lambda x: 'undead '+x, 'attack': lambda x: x-5, 'hp': lambda x: x+15}
    beasty = {'name': lambda x: 'beasty '+x, 'attack': lambda x: x+5, 'agility': lambda x: x+5}
    demonic = {'name': lambda x: 'demonic '+x, 'shield': lambda x: x+30, 'hp': lambda x: x-5}
    frozen = {'name': lambda x: 'frozen '+x, 'hp': lambda x: x+30, 'agility': lambda x: 0}
    cursed = {'name': lambda x: 'cursed '+x, 'attack': lambda x: x-5, 'hp': lambda x: x-10}

    up_name = random.choice((undead, beasty, demonic, frozen, cursed))

    champion = {'name': lambda x: ('champion '+x).upper(), 'shield': lambda x: x+20, 'hp': lambda x: x+20}
    flaming = {'name': lambda x: ('flaming '+x).upper(), 'attack': lambda x: x+30}
    furious = {'name': lambda x: ('furious '+x).upper(), 'shield': lambda x: x+30}

    up_super = random.choice((champion, flaming, furious))

    creature = modify(up_monster, up_name)
    if random.randint(1,10) == 1:
        creature = modify(up_super, creature)

    return creature

def itm():
    mixture = {'hp': lambda x: x+20}
    false_key = False
    boost_attack = {'attack': lambda x: x+10}
    boost_shield = {'attack': lambda x: x+10}
    boost_agility = {'agility': lambda x: x+2}
    empty_box = None
    key = True
    super_shield = {'agility': lambda x: 10}

    if random.randint(1,2) == 1:
        prize = random.choice((mixture, false_key, boost_attack, boost_shield, boost_agility))
    elif random.randint(1,5) == 1:
        prize = random.choice((key, super_shield))
    else: prize = empty_box

    return prize

