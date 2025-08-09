'''Options of end game'''

class EndGame():
    def __init__(self, game_state):
        self.state = game_state

    def last_chance(self):
        player = self.state.player
        last_chance_list = list(filter(lambda item: getattr(item, 'mode', None) == 'raise', player.back_pack))
        if last_chance_list:
            game_state = last_chance_list[0].last_chance(self.state)
            print(f'game state: {type(game_state)}')
            return game_state
        return self

class HappyEnd(EndGame):
    def __init__(self, game_state):
        super().__init__(game_state)
        ui = game_state.UI
        player = game_state.player
        ui.say('Congratulations you find an exit!!')
        ui.say(f'hp: {player.hp}')

class IngloriousDeath(EndGame):
    def __init__(self, game_state):
        super().__init__(game_state)
        ui = game_state.UI
        room = game_state.curr_room
        ui.say('You died ingloriously in the dungeon')
        ui.say(f'{room.monster} taste your delicious flesh..')

class MissingInMase(EndGame):
    def __init__(self, game_state):
        super().__init__(game_state)
        ui = game_state.UI
        player = game_state.player
        ui.say(f'{player.name} disappeared into the maze and was never seen again..')