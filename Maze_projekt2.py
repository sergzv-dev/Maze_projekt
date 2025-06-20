class UI():
    def ask(self, text):
        answer = input(text)
        return answer

    def choose(self, options):
        answer = input(f'{options}')
        return options[answer]

    def say(self, text):
        print(text)

def game():
    master = UI()
    name = master.ask("What is your name? ")
    stranger = Player(name)
    world = map_builder(10, 10)
    game_state = GameState(world, stranger)
    while True:
        actions = game_state.possible_actions()
        action = master.choose(actions)
        game_state = action.execute(game_state)


class GameState():
    def __init__(self, world, player):
        self.player = player
        self.world = world
        self.curr_room = '00'

    def possible_actions(self):
        return self.player.actions() + self.world[self.curr_room].actions()

class Room():
    def __init__(self, x, y):
        self.name = str(x) + str(y)
        self.actions = [MoveAction.move(f'{str(x+1)}{str(y+1)}')(), ShowCurrRoom.show()]

    def actions(self):
        return self.actions

    def __repr__(self):
        return self.name


class Action():
    def execute(self, game_state):
        self.state = game_state

class MoveAction(Action):
    def __init__(self, new_room):
        self.room = new_room

    def move(self):
        self.state.curr_room = self.room

class ShowCurrRoom(Action):

    def show(self):
        return self.state.curr_room

class OpenBackPack:
    def show(self):
        return self.state.player.back_pack

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
    def actions(self):
        return [OpenBackPack.show(), GetItem.get_it()]


class Monster(Creature):
    pass

def map_builder(x_line, y_line):
    rooms_dict = dict()
    for x in range(x_line):
        rooms_dict.update({f'{str(x)}{str(y)}': Room(x,y) for y in range(y_line)})
    return rooms_dict


game()