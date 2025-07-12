''' Module contains states of current game'''

class GameState():
    def __init__(self, master, world, player, curr_room):
        self.UI = master
        self.player = player
        self.world = world
        self.curr_room = curr_room

    def possible_actions(self):
        return self.player.actions + self.curr_room.actions


