''' Module contains actions for the game'''

from game_endings import IngloriousDeath, HappyEnd
import random

class Action():
    def execute(self, game_state):
        pass

class MoveAction(Action):
    def __init__(self, target_room):
        self.target_room = target_room

    def execute(self, game_state):
        game_state.curr_room = self.target_room
        ui = game_state.UI
        ui.say(f'you enter the room {self.target_room}')
        return game_state

    def __repr__(self):
        return f'Go to the room {self.target_room}'


class SearchAction(Action):
    def execute(self, game_state):
        ui = game_state.UI
        room = game_state.curr_room
        room.room_searched = True
        if room.monster:
            ui.say(f'there is {room.monster} lurking in a dark corner')
        elif room.quest:
            if room.quest.sign == 'EndDoor':
                ui.say('you find old dusty door')
            if room.quest.sign == 'ImmortalAltar':
                ui.say('many candles in the room and circle of runes in the center')
        elif room.box:
            ui.say('this is looks like an old chest!')
        else: ui.say('the rom is empty')
        return game_state

    def __repr__(self):
        return 'Search the room'


class FightAction(Action):
    def execute(self, game_state):
        player = game_state.player
        player.fight_marker = True
        monster = game_state.curr_room.monster
        monster.take_damage(player.attack, game_state)
        if monster.death_marker:
            return game_state
        if not monster.death_marker:
            player.take_damage(monster.attack, game_state)
        if player.death_marker:
            return IngloriousDeath(game_state)
        return game_state

    def __repr__(self):
        return 'Fight to the monster!!'


class GetItem(Action):
    def execute(self, game_state):
        ui = game_state.UI
        ui.say('picked up the loot')
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
        room = game_state.curr_room
        pl = game_state.player
        specs = f'room: {room} \nname: {pl.name}\nHP: {pl.hp}\nattack: {pl.attack}\nshield: {pl.shield}\nagility: {pl.agility}\n'
        game_state.UI.say(specs)
        return game_state

    def __repr__(self):
        return 'Show your\'s specs'

class ShowMonstersSpecs(Action):
    def execute(self, game_state):
        mon = game_state.curr_room.monster
        specs = f'name: {mon.name}\nHP: {mon.hp}\nattack: {mon.attack}\nshield: {mon.shield}\nagility: {mon.agility}\n'
        game_state.UI.say(specs)
        return game_state

    def __repr__(self):
        return 'Show monsters specs'

class OpenBox(Action):
    def execute(self, game_state):
        ui = game_state.UI
        room = game_state.curr_room
        ui.say(f'you find {room.box.loot}')
        mode = getattr(room.box.loot,'mode', None)
        if mode == 'bomb':
            game_state = room.box.loot.execute(game_state)
            room.box = None
            return game_state
        room.loot.append(room.box.loot)
        room.box = None
        return game_state

    def __repr__(self):
        return 'Open the box'

class EscapeAction(Action):
    def execute(self, game_state):
        ui = game_state.UI
        ui.say(f'you try to sneak away')
        player = game_state.player
        monster = game_state.curr_room.monster
        if random.randint(1, 2) == 1:
            player.take_damage(monster.attack, game_state, death = False)
        player.fight_marker = False
        return game_state

    def __repr__(self):
        return 'Escape the fight'

class SaveGame(Action):
    def execute(self, game_state):
        game_state = game_state.save_game()
        return game_state

    def __repr__(self):
        return 'Save game'

class LoadGame(Action):
    def execute(self, game_state):
        ui = game_state.UI
        game_state = game_state.load_game(ui = ui)
        return game_state

    def __repr__(self):
        return 'Load game'

class QuestAction(Action):
    pass

class EndDoorAction(QuestAction):
    def execute(self, game_state):
        ui = game_state.UI
        room = game_state.curr_room
        key = room.quest.take_key(game_state)

        if key:
            return HappyEnd(game_state)
        else: ui.say('You don\'t have suitable key')
        return game_state

    def __repr__(self):
        return 'Try to open old hidden door'

class ImmortalAltarAction(QuestAction):
    def execute(self, game_state):
        player = game_state.player
        ui = game_state.UI
        room = game_state.curr_room
        amulet = room.quest.take_key(game_state)

        if amulet:
            player.increase_spec('max_hp', 10)
            player.hp = player.max_hp
            player.increase_spec('attack', 15)
            player.increase_spec('shield', 10)
            player.increase_spec('agility', 10)
            ui.say('The power of sanctions gods bless your soul')
            player.back_pack.remove(amulet)
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
        opt_actions = [SaveGame(), LoadGame()]
        if player.open_bp:
            return bp_actions + player.back_pack
        if player.fight_marker:
            return [FightAction(), EscapeAction(), ShowMonstersSpecs()] + player_act
        return player_act + ActionProvider.room_act_gen(game_state) + opt_actions

    @staticmethod
    def room_act_gen(game_state):
        actions = []
        rooms_dict = game_state.world.rooms_dict
        room = game_state.curr_room
        room_doors = [MoveAction(rooms_dict[door]) for door in room.doors]
        if not room.room_searched:
            actions = [SearchAction()]
        elif room.monster:
            actions = [FightAction()]
        else:
            if room.box:
                actions.append(OpenBox())
            if room.loot:
                actions.append(GetItem())
            if getattr(room.quest, 'sing', None) == 'EndDoor':
                actions.append(EndDoorAction())
            if getattr(room.quest, 'sing', None) == 'ImmortalAltar':
                actions.append(ImmortalAltarAction())
        return actions + room_doors