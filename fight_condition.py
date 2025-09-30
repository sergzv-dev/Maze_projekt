from game_endings import IngloriousDeath
import random
from itertools import cycle
from abstractions import Action

class FightCondition:
    temp_attrs = ['temp_seq', 'shield_effect', 'target']

    def __init__(self, game_state):
        self.state = None
        self.player = None
        self.team1 = None
        self.team2 = None
        self.hiding_mimic = False
        self.creatures_list = None
        self.queue = None
        self.repr = self.set_repr(game_state)

    def class_initialisation(self, game_state):
        self.state = game_state
        self.player = game_state.player
        self.team1 = [self.state.player]
        self.team2 = self.state.curr_room.monster
        self.hiding_mimic = False
        self.creatures_list = self.team1 + self.team2
        self.queue = cycle(self.make_queue(self.creatures_list))

    def monsters_move(self):
        while True:
            creature = self.take_next_creature()
            if creature == self.player: break
            else: self.take_monster_action(creature)

    def fight_execute(self, game_state):
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

    @staticmethod
    def make_queue(sequence):
        setattr_fun = lambda obj: setattr(obj, 'temp_seq', random.randint(1, max(1, obj.agility)))
        sequence = [setattr_fun(creature) for creature in sequence]
        sequence = sorted(sequence, key=lambda x: x['temp_seq'], reverse=True)
        return sequence

    def start_fight(self):
        return self.state

    def __repr__(self):
        return self.repr

    def get_action(self):
        actions =[]
        self.target_chek()
        if not self.player.target:
            actions.append(ChooseTarget())
        actions += [ShowMonstersSpecs(), EscapeAction()]
        return actions

    def target_chek(self):
        if self.player.target not in self.state.monster: self.player.target = None

    def take_next_creature(self):
        return next(self.queue)

    def take_monster_action(self, creature):
        pass

    @staticmethod
    def set_repr(game_state):
        if len(game_state.monster) > 1:
            res_repr = 'Search the room'
        elif 'Mimic' in game_state.monster[0].__name__:
            res_repr = 'Open the box'
        else: res_repr = 'Fight to the monster!!'
        return res_repr


    def enter_fight(self):
        for creature in self.creatures_list:
            for attr in self.temp_attrs:
                setattr(creature, attr, None)
        self.player.fight_marker = True

    def exit_fight(self):
        for creature in self.creatures_list:
            for attr in self.temp_attrs:
                delattr(creature, attr)
        self.player.fight_marker = False


class FightAction(Action):
    pass

class Attack(FightAction):
    def execute(self, game_state):
        player = game_state.player
        player.target.take_damage(player.attack, game_state)
        game_state.fight_action.monsters_move()
        return game_state

    def __repr__(self):
        return f'attack the monster'

class StrongAttack(FightAction):
    def execute(self, game_state):
        player = game_state.player
        player.shield_effect = -player.shield
        player.target.take_damage(player.attack*2, game_state)
        game_state.fight_action.monsters_move()
        return game_state

    def __repr__(self):
        return f'strike the monster hard'

class DefenseAttack(FightAction):
    def execute(self, game_state):
        player = game_state.player
        player.shield_effect = player.shield
        player.target.take_damage(player.attack/2, game_state)
        game_state.fight_action.monsters_move()
        return game_state

    def __repr__(self):
        return f'make defense attack'


class ChooseTarget(FightAction):
    def execute(self, game_state):
        ui = game_state.UI
        player = game_state.player
        target_list = game_state.fight_action.team2
        ui.say('which monster do you want to attack?')
        target = ui.choose(target_list)
        player.target = target
        return game_state

    def __repr__(self):
        return 'choose target monster'

class ShowMonstersSpecs(FightAction):
    def execute(self, game_state):
        mon = game_state.curr_room.monster
        specs = f'name: {mon.name}\nHP: {mon.hp}\nattack: {mon.attack}\nshield: {mon.shield}\nagility: {mon.agility}\n'
        game_state.UI.say(specs)
        return game_state

    def __repr__(self):
        return 'Show monsters specs'

class EscapeAction(FightAction):
    def execute(self, game_state):
        ui = game_state.UI
        ui.say(f'you try to sneak away')
        player = game_state.player
        monster = game_state.curr_room.monster
        if random.randint(1, 2) == 1:
            player.take_damage(monster.attack, game_state, death=False)
        player.fight_marker = False
        return game_state

    def __repr__(self):
        return 'Escape the fight'


class SearchMonsterAction(FightAction):
    def execute(self, game_state):
        ui = game_state.UI
        player = game_state.player
        room = game_state.curr_room
        fight_action = game_state.fight_action
        room.room_searched = True
        if len(room.monster) > 1:
            player.fight_marker = True
            ui.say(f'the monsters unexpectedly attacked!')
        elif 'Mimic' in room.monster[0].__name__:
            fight_action.hiding_mimic = True
            ui.say('this is looks like an old chest!')
        elif room.monster:
            ui.say(f'there is {room.monster[0]} lurking in a dark corner')
        return game_state

    def __repr__(self):
        return 'Search the room'