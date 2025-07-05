class UI():
    def ask(self, text):
        answer = input(text)
        return answer

    def choose(self, options):
        create_opt = '\n'.join(f'{i}: {num + 1}' for num, i in enumerate(options))
        answer = input(f'{create_opt}')
        return options[answer]

    def say(self, text):
        print(text)

def game():
    master = UI()
    name = master.ask("What is your name? ")
    stranger = Player(name)
    world = World()
    curr_room = world.rooms_dict[name_convert('A1')]
    game_state = GameState(master, world, stranger, curr_room)
    while True:
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
        self.actions = []
        MoveAction(self)

    def __repr__(self):
        return name_convert(self.name)


class Action():
    def execute(self, game_state):
        pass

class MoveAction(Action):
    def __init__(self, room): #как при создании класса сделать возможным обращаться к UI или лучше к
                                #GameState ведь это доступно становится только после execute
        self.room = room
        self.doors = []
        self.room.append(self)

    def move(self):
        self.state.curr_room = self.room

    def execute(self, game_state):
        self.state = game_state

    def __repr__(self):  #хочу сделать repr чтоб печаталось "выбрать путь" но нет доступа к UI на данном этапе
        return f'Go to the room {self.room}'


class OpenBackPack:
    def show(self):
        return self.state.player.back_pack
    def __repr__(self):
        return 'Open back pack'

class GetItem():
    def get_it(self):
        self.state.player.back_pack = self.state.player.back_pack + ['heal']
        return self.state.player.back_pack


class SearchAction(Action):
    pass

class FightAction(Action):
    pass


class Creature():
    def __init__(self, name):
        self.name = name
        self.back_pack = []
        self.actions = []


class Player(Creature):
    def __init__(self, name):
        super().__init__(name)
        self.actions = [OpenBackPack]

class Monster(Creature):
    pass

class World():
    def __innit__(self, x_line, y_line):
        self.size = (x_line, y_line)
        self.x_line = x_line
        self.y_line = y_line
        self.rooms_dict = dict()
        self.map_builder()

    def map_builder(self, func):
        for x in range(self.x_line):
            self.rooms_dict.update({(x, y): func((x, y)) for y in range(self.y_line)})


def name_convert(x, y = None):
    res = None
    if isinstance(x, int):
        res = f'{chr(x+64)}{str(y)}'
    if isinstance(x, str):
        res = ord(x[0])-64, int(x[1])
    return res



'''def map_builder(x_line, y_line):
    rooms_dict = {'map_size': (x_line, y_line)}  #что думаешь если зашить map_size в rooms_dict как тех.инфу чтоб достать из GameState
    name = lambda x, y: f'{str(x)}{str(y)}'
    for x in range(x_line):
        rooms_dict.update({name(x,y): Room(name(x,y)) for y in range(y_line)})
    return rooms_dict'''


game()