from game_endings import IngloriousDeath
import random
from abstractions import Action

class FightCondition:
    def __init__(self, game_state):
        self.state = game_state
        self.team1 = self.state.player
        self.team2 = self.state.curr_room.monster
        self.repr = None
        self.target = None

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

    def start_fight(self):
        return self.state

    def __repr__(self):
        return self.repr

    def get_action(self):
        actions =[]
        self.target_chek()
        actions += [ShowMonstersSpecs(), EscapeAction()]
        return actions

    def target_chek(self):
        if self.target not in self.state.monster: self.target = None


class ChooseTarget(Action):
    def execute(self, game_state):
        ui = game_state.UI
        target_list = game_state.fight_action.team2
        ui.say('choose target monster..')
        target = ui.choose(target_list)
        game_state.fight_action.target = target
        return game_state

class ShowMonstersSpecs(Action):
    def execute(self, game_state):
        mon = game_state.curr_room.monster
        specs = f'name: {mon.name}\nHP: {mon.hp}\nattack: {mon.attack}\nshield: {mon.shield}\nagility: {mon.agility}\n'
        game_state.UI.say(specs)
        return game_state

    def __repr__(self):
        return 'Show monsters specs'

class EscapeAction(Action):
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