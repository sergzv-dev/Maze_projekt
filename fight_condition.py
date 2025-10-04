from game_endings import IngloriousDeath
import random
from itertools import cycle
from abstractions import Action

class FightCondition:
    def __init__(self, game_state):
        self.player = game_state.player
        self.team1 = [game_state.player]
        self.team2 = game_state.curr_room.monsters
        self.creatures_list = self.team1 + self.team2
        self.queue = self.make_queue(self.creatures_list)
        self.effects_dict = self.make_effects_dict(self.creatures_list)
        self.targets_dict = self.make_targets_dict(self.creatures_list)

    @staticmethod
    def make_queue(sequence):
        return cycle(sorted(sequence, key=lambda creature: -random.randint(1, max(1, creature.agility))))

    @staticmethod
    def make_effects_dict(sequence):
        return {creature: UnderEffects() for creature in sequence}

    @staticmethod
    def make_targets_dict(sequence):
        return {creature: None for creature in sequence}


class FightService:
    def get_action(self):
        actions = []
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

    def start_fight(self):
        return self.state

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


    def behavior(self, creature):
        pass

    def choose_action(self, action_list):
        return random.choice(action_list)

class UnderEffects:
    def __init__(self):
        self.temp_shield = None
        self.temp_agility = None

    def set_effects(self, *, temp_shield = None, temp_agility = None):
        self.temp_shield = temp_shield
        self.temp_agility = temp_agility

    def aplay_effects(self):
        effects = self.__dict__.copy()
        self.set_effects()
        return effects

class Behavior:
    pass

class PlayerBehavior(Behavior):
    pass

class DefaultBehavior(Behavior):
    pass

class AggressiveBehavior(Behavior):
    pass

class DefenceBehavior(Behavior):
    pass

class MageBehavior(Behavior):

class BehaviorConstractor:
    CHEK_DICT = {'pl': PlayerBehavior, None: DefaultBehavior, 'at': AggressiveBehavior, 'def': DefenceBehavior,
                 'mag': MageBehavior
                 }
    def __init__(self):
        pass

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