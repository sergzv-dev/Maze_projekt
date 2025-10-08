import random

class Behavior:
    def get_fight_action(self, game_state)-> 'MonsterFightAction':
        pass

class BasicBehaviour(Behavior):
    def get_fight_action(self, game_state):
        return BasicAttack()

class AggressiveBehavior(Behavior):
    def get_fight_action(self, game_state):
        action = random.choice([BasicAttack(), StrongAttack()])
        if game_state.fight_condition.current_attacker.hp < 15: action = BasicAttack()
        return action

class PlayerBehavior(Behavior):
    pass

class DefenceBehavior(Behavior):
    pass

class MageBehavior(Behavior):
    pass


class TargetBehaviour:
    def get_target(self, game_state) -> 'Creature':
        pass


class BasicChooseTarget(TargetBehaviour):
    def get_target(self, game_state) -> 'Creature':
        return game_state.player



class MonsterFightAction:
    def execute(self, game_state) -> 'GameState':
        pass

    @staticmethod
    def make_hit(game_state, attack_mult = 1, set_shield = None, set_agility = None):
        fight_state = game_state.fight_state
        attacker = fight_state.current_attacker
        defender = fight_state.take_target(attacker)

        attacker_effect = fight_state.take_effects(attacker)
        attacker_effect.set_effects(temp_shield = set_shield, temp_agility = set_agility)

        damage = int(attacker.attack * attack_mult)
        defender_effect = fight_state.take_effects(defender)
        def_temp_shield, def_temp_agility = defender_effect.apply_effects()
        game_state = defender.take_damage(damage, game_state, temp_shield=def_temp_shield,
                                          temp_agility=def_temp_agility)
        return game_state


class BasicAttack(MonsterFightAction):
    def execute(self, game_state) -> 'GameState':
        game_state = self.make_hit(game_state)
        return game_state

class StrongAttack(MonsterFightAction):
    def execute(self, game_state) -> 'GameState':
        attacker = game_state.fight_state.current_attacker
        game_state = self.make_hit(game_state, attack_mult = 2, set_shield = attacker.shield/2)
        return game_state