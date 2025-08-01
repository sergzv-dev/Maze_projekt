'''Options of end game'''

class EndGame():
    pass

class HappyEnd(EndGame):
    def __init__(self, game_state):
        ui = game_state.UI
        player = game_state.player
        ui.say('Congratulations you find an exit!!')
        ui.say(f'hp: {player.hp}')

class IngloriousDeath(EndGame):
    def __init__(self, game_state):
        ui = game_state.UI
        room = game_state.curr_room
        ui.say('You died ingloriously in the dungeon')
        ui.say(f'{room.monster} taste your delicious flesh..')