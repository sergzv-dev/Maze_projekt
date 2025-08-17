''' Module contains actions for the game'''

from game_endings import IngloriousDeath, HappyEnd
from game_states import GameState
from game_endings import EndGame

class Action():
    def execute(self, game_state) -> GameState | EndGame:
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
        room.room_searched = True
        return game_state

    def __repr__(self):
        return 'Search the room'


class FightAction(Action):
    def execute(self, game_state):
        player = game_state.player
        while True:
            monster = game_state.curr_room.monster
            if monster is None:
                return game_state
            monster.take_damage(player.attack)

            player.take_damage(monster.attack)
            if player.hp < 1:
                death = IngloriousDeath(game_state)
                return death.last_chance()

    def __repr__(self):
        return 'Fight to the monster!!'


class GetItem(Action):
    def execute(self, game_state):
        room = game_state.curr_room
        player = game_state.player
        player.back_pack += room.loot
        room.loot = []
        return game_state

    def __repr__(self):
        return 'Get loot'


class OpenBackPack(Action):
    def execute(self, game_state):
        player = game_state.player
        player.open_bp = True
        return game_state

    def __repr__(self):
        return 'Open backpack'

class CloseAction(Action):
    def execute(self, game_state):
        player = game_state.player
        player.open_bp = False
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
        mode = getattr(room.box.loot,'mode', None)
        if mode == 'bomb':
            game_state = room.box.loot.execute(game_state)
            room.box = None
            return game_state
        room.loot += room.box.loot
        room.box = None
        return game_state

    def __repr__(self):
        return 'Open the box'

class EndDoorAction(Action):
    def __init__(self, key):
        self.key = key

    def execute(self, game_state):
        player = game_state.player
        ui = game_state.UI

        if self.key in player.back_pack:
            return HappyEnd(game_state)
        else: ui.say('You don\'t have suitable key')
        return game_state

    def __repr__(self):
        return 'Try to open old hidden door'

class ImmortalAltarAction(Action):
    def __init__(self, amulet):
        self.amulet = amulet

    def execute(self, game_state):
        player = game_state.player
        ui = game_state.UI

        if self.amulet in player.back_pack:
            player.max_hp += 10
            player.hp = player.max_hp
            player.attack += 15
            player.shield += 10
            player.agility += 10
            ui.say('The power of sanctions gods bless your soul')
            player.back_pack.remove(self.amulet)
        else: ui.say('find amulet for sacrifice')
        return game_state

    def __repr__(self):
        return 'make a sacrifice'


class ActionProvider():
    @staticmethod
    def provide_action(game_state):
        player = game_state.player
        player_act = [ShowSpecs(), OpenBackPack()]
        bp_actions = [CloseAction()]
        if player.open_bp is True:
            return bp_actions + player.back_pack
        return player_act + ActionProvider.room_act_gen(game_state)

    @staticmethod
    def room_act_gen(game_state):
        room = game_state.curr_room
        room_act = room.actions
        room_doors = [MoveAction(door) for door in room.doors]
        if not room.room_searched:
            actions = [SearchAction()]
        elif room.monster:
            actions = [FightAction()]
        elif room.box:
            actions = [OpenBox()] + room_act
        elif room.loot:
            actions = [GetItem()] + room_act
        else: actions = room_act
        return actions + room_doors
