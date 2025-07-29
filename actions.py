''' Module contains actions for the game'''

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


class SearchAction(Action):
    def execute(self, game_state):
        room = game_state.curr_room
        room.actions = room.hidden_actions + room.actions
        room.actions.remove(self)
        return game_state

    def __repr__(self):
        return 'Search the room'


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
        return 'Fight to the monster!!'


class GetItem(Action):
    def execute(self, game_state):
        room = game_state.curr_room
        player = game_state.player
        player.back_pack.append(room.loot)
        room.loot = None
        room.actions.remove(self)
        return game_state

    def __repr__(self):
        return 'Get loot'


class OpenBackPack(Action):
    def execute(self, game_state):
        player = game_state.player
        ui = game_state.UI
        action = ui.choose(player.back_pack)
        game_state = action.execute(game_state)
        return game_state

    def __repr__(self):
        return 'Open backpack'

class CloseAction(Action):
    def execute(self, game_state):
        return game_state

    def __repr__(self):
        return 'Close'


class ShowSpecs(Action):
    def execute(self, game_state):
        pl = game_state.player
        specs = f'name: {pl.name}\nHP: {pl.hp}\nattack: {pl.attack}\nshield: {pl.shield}\nagility: {pl.agility}\n'
        game_state.UI.say(specs)
        return game_state

    def __repr__(self):
        return 'Show specs'

class OpenBox(Action):
    def execute(self, game_state):
        room = game_state.curr_room
        room.loot = room.box.loot
        room.actions.append(GetItem())
        room.box = None
        room.actions.remove(self)
        return game_state

    def __repr__(self):
        return 'Open the box'