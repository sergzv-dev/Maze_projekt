from game_endings import IngloriousDeath
import random
from itertools import cycle
from abstractions import Action

class FightCondition:
    def __init__(self, game_state):
        self.player = game_state.player
        self.team1 = [game_state.player]
        self.team2 = list(game_state.curr_room.monsters)
        self.creatures_list = self.team1 + self.team2
        self.queue = self.make_queue(self.creatures_list)
        self.effects_dict = self.make_effects_dict(self.creatures_list)
        self.targets_dict = self.make_targets_dict(self.creatures_list)
        self.current_attacker = None

    @staticmethod
    def make_queue(sequence):
        return cycle(sorted(sequence, key=lambda creature: -random.randint(1, max(1, creature.agility))))

    @staticmethod
    def make_effects_dict(sequence):
        return {id(creature): UnderEffects() for creature in sequence}

    @staticmethod
    def make_targets_dict(sequence):
        return {id(creature): None for creature in sequence}

    def take_next_creature(self):
        creature = next(self.queue)
        self.current_attacker = creature
        return creature

    def take_effects(self, creature):
        return self.effects_dict[id(creature)]

    def take_target(self, creature):
        return self.targets_dict[id(creature)]

    def take_possible_targets(self, creature):
        if creature in self.team1: targets_list = self.team2
        else: targets_list = self.team1
        return list(filter(lambda obj: not obj.death_marker, targets_list))

    def set_target(self, creature, target):
        self.targets_dict[id(creature)] = target

    def win_check(self, game_state):
        if getattr(self.take_target(self.player) ,'death_marker'):
            self.targets_dict[id(self.player)] = None
        if all(creature.death_marker for creature in self.team2):
            game_state.fight_state = None
        return game_state


class FightService:
    def get_action(self, game_state):
        player = game_state.player
        fight_state = game_state.fight_state

        self.manage_fight(game_state)
        if player.death_marker:
            return IngloriousDeath(game_state)

        player_target = fight_state.take_target(player)
        if not player_target:
            action = ChooseTarget()
            action.execute(game_state)

        actions = [Attack()] #StrongAttack(), DefenseAttack(), ChangeTarget(), EscapeAction()
        return actions

    def target_chek(self):
        if self.player.target not in self.state.monster: self.player.target = None


    def manage_fight(self, game_state):
        while True:
            creature = game_state.fight_state.take_next_creature()
            if creature.death_marker: continue
            elif creature is game_state.player: break
            else: self.monster_move(game_state)

    def monster_move(self, game_state):
        fight_state = game_state.fight_state
        monster = fight_state.current_attacker
        target = fight_state.take_target(monster)
        if not target: fight_state.set_target(monster, monster.target_behavior.get_target(game_state))
        game_state = monster.behavior.get_fight_action(game_state).execute(game_state)
        return game_state


class UnderEffects:
    def __init__(self):
        self.temp_shield = None
        self.temp_agility = None

    def set_effects(self, *, temp_shield = None, temp_agility = None):
        self.temp_shield = temp_shield
        self.temp_agility = temp_agility

    def apply_effects(self):
        temp_shield = self.temp_shield
        temp_agility = self.temp_agility
        self.set_effects()
        return temp_shield, temp_agility


class FightAction(Action):
    pass

class Attack(FightAction):
    def execute(self, game_state):
        player = game_state.player
        fight_state = game_state.fight_state
        target = fight_state.take_target(player)
        target.take_damage(player.attack, game_state)
        game_state = fight_state.win_check(game_state)
        return game_state

    def __repr__(self):
        return f'attack the monster'


class ChooseTarget(FightAction):
    def execute(self, game_state):
        ui = game_state.UI
        player = game_state.player
        target_list = game_state.fight_state.take_possible_targets(player)
        ui.say('which monster do you want to attack?')
        target = ui.choose(target_list)
        game_state.fight_state.set_target(player, target)
        return game_state

    def __repr__(self):
        return 'choose target monster'

########################################### TODO

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


class ChangeTarget(FightAction):
    def execute(self, game_state):
        pass

    def __repr__(self):
        return 'change target monster'

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