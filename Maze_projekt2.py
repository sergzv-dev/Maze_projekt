import random

class UI():
    def ask(self, text):
        answer = input(text)
        return answer

    def choose(self, options):
        create_opt = '\n'.join(f'{i}: {num + 1}' for num, i in enumerate(options))
        answer = input(f'{create_opt}\n...')
        return options[int(answer)-1]

    def say(self, text):
        print(text)

def game():
    master = UI()
    name = master.ask("What is your name? ")
    player = Player(name)
    world = World(10, 10)
    curr_room = world.rooms_dict[name_convert('A1')]
    game_state = GameState(master, world, player, curr_room)
    while True:
        print(f'player hp = {game_state.player.hp}')
        print(f'monster {game_state.curr_room.monster}\n')
        actions = game_state.possible_actions()
        action = master.choose(actions)
        game_state = action.execute(game_state)


class GameState():
    def __init__(self, master, world, player, curr_room):
        self.UI = master
        self.player = player
        self.world = world
        self.curr_room = curr_room

    def possible_actions(self):
        return self.player.actions + self.curr_room.actions

class Room():
    def __init__(self, name):
        self.name = name
        self.actions = [SearchAction()]
        self.hidden_actions = []
        self.monster = None

    def __repr__(self):
        return name_convert(self.name)


class Action():
    def execute(self, game_state):
        pass

class MoveAction(Action):
    def __init__(self, target_room):
        self.target_room = target_room

    def execute(self, game_state):
        game_state.curr_room = self.target_room
        return game_state

    def __repr__(self):
        return f'Go to the room {self.target_room}'


class OpenBackPack(Action):
    pass

class GetItem(Action):
    pass


class SearchAction(Action):
    def execute(self, game_state):
        room = game_state.curr_room
        room.actions = room.hidden_actions + room.actions
        room.actions.remove(self)
        return game_state

    def __repr__(self):
        return f'Search the room'


class FightAction(Action):
    def execute(self, game_state):
        room = game_state.curr_room
        player = game_state.player
        monster = game_state.curr_room.monster
        while True:
            monster.hp -= max(1, round(player.attack - player.attack * (monster.shield/100)))
            if monster.hp < 1:
                game_state.curr_room.monster = None
                room.actions.remove(self)
                return game_state
            player.hp -= max(1, round(monster.attack - monster.attack * (player.shield/100)))
            if player.hp < 1:
                raise ValueError('Game Over!!')

    def __repr__(self):
        return f'Fight to the monster!!'


class Creature():
    def __init__(self, name, attack, shield, hp, agility):
        self.name = name
        self.attack = attack
        self.shield = shield
        self.hp = hp
        self.agility = agility
        self.back_pack = []


class Player(Creature):
    def __init__(self, name, attack = 10, shield = 20, hp = 100, agility = 5):
        super().__init__(name, attack, shield, hp, agility)
        self.actions = []

class Monster(Creature):
    def __repr__(self):
        return f'{self.name}'

class World():
    def __init__(self, x_line, y_line):
        self.size = (x_line, y_line)
        self.x_line = x_line
        self.y_line = y_line
        self.rooms_dict = dict()
        self.map_builder(Room)
        self.doors_builder(self.rooms_dict, MoveAction)
        self.add_monster(self.rooms_dict, NewMonster, Monster, FightAction)

    def map_builder(self, cls_room):
        for x in range(1, self.x_line+1):
            self.rooms_dict.update({(x, y): cls_room((x, y)) for y in range(1, self.y_line+1)})

    @staticmethod
    def doors_builder(rooms_dict, action):
        for x, y in rooms_dict:
            doors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
            for num in doors:
                door = rooms_dict.get(num)
                if door is not None:
                    rooms_dict[(x, y)].actions.append(action(door))

    @staticmethod
    def add_monster(rooms_dict, new_monster, monster, fight):
        creature = None
        add_func = lambda spec, impact: {key: impact.get(key, lambda x: x)(value) for key, value in spec.items()}
        for room in rooms_dict:
            if random.randint(1, 4) == 1:
                creature = new_monster.up_monster()
                if random.randint(1, 2) == 1:
                    creature = add_func(creature, new_monster.up_name())
                    if random.randint(1, 5) == 1:
                        creature = add_func(creature, new_monster.up_super())
            if creature is not None:
                rooms_dict[room].monster = monster(
                    creature['name'], creature['attack'], creature['shield'], creature['hp'], creature['agility']
                )
                rooms_dict[room].hidden_actions.append(fight())


class NewMonster():
    @staticmethod
    def up_monster():
        soldier = {'name': 'soldier', 'attack': 15, 'shield': 10, 'hp': 30, 'agility': 2}
        goblin = {'name': 'goblin', 'attack': 10, 'shield': 5, 'hp': 25, 'agility': 3}
        mage = {'name': 'mage', 'attack': 20, 'shield': 5, 'hp': 20, 'agility': 5}
        knight = {'name': 'knight', 'attack': 10, 'shield': 20, 'hp': 50, 'agility': 0}
        mimic = {'name': 'mimic', 'attack': 30, 'shield': 5, 'hp': 15, 'agility': 0}
        return random.choice((soldier, goblin, mage, knight, mimic))

    @staticmethod
    def up_name():
        undead = {'name': lambda x: 'undead '+x, 'attack': lambda x: x-5, 'hp': lambda x: x+15}
        beasty = {'name': lambda x: 'beasty '+x, 'attack': lambda x: x+5, 'agility': lambda x: x+5}
        demonic = {'name': lambda x: 'demonic '+x, 'shield': lambda x: x+30, 'hp': lambda x: x-5}
        frozen = {'name': lambda x: 'frozen '+x, 'hp': lambda x: x+30, 'agility': lambda x: 0}
        cursed = {'name': lambda x: 'cursed '+x, 'attack': lambda x: x-5, 'hp': lambda x: x-10}
        return random.choice((undead, beasty, demonic, frozen, cursed))

    @staticmethod
    def up_super():
        champion = {'name': lambda x: ('champion '+x).upper(), 'shield': lambda x: x+20, 'hp': lambda x: x+20}
        flaming = {'name': lambda x: ('flaming '+x).upper(), 'attack': lambda x: x+30}
        furious = {'name': lambda x: ('furious '+x).upper(), 'shield': lambda x: x+30}
        return random.choice((champion, flaming, furious))


def name_convert(name):
    if isinstance(name, tuple):
        return f'{chr(name[0]+64)}{str(name[1])}'
    if isinstance(name, str):
        return ord(name[0])-64, int(name[1:])
    raise TypeError('"name" must be srt or tuple')


game()