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

    def __repr__(self):
        return name_convert(self.name)


class Action():
    def execute(self, game_state):
        pass

class MoveAction(Action):
    def __init__(self, target_room):
        self.target_room = target_room

    def execute(self, game_state):
        self.state = game_state
        self.state.curr_room = self.target_room
        return self.state

    def __repr__(self):
        return f'Go to the room {self.target_room}'


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
        self.actions = []

class Monster(Creature):
    pass

class World():
    def __init__(self, x_line, y_line, cls_room = Room, action = MoveAction):
        self.size = (x_line, y_line)
        self.x_line = x_line
        self.y_line = y_line
        self.rooms_dict = dict()
        self.cls_room = cls_room
        self.action = action
        self.map_builder(self.cls_room)
        self.doors_builder(self.rooms_dict, self.action)

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



def name_convert(name):
    res = None
    if isinstance(name, tuple):
        res = f'{chr(name[0]+64)}{str(name[1])}'
    if isinstance(name, str):
        res = ord(name[0])-64, int(name[1])
    return res


game()