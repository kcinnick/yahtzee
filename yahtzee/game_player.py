from .dice import subtract_dice_states
from .solve import solve_turn

import pickle as pkl
from os import path

# Get precomputed game state values
PRECOMP_PATH = r'C:\Users\Nick\PycharmProjects\androidAutomation\games\diceYatzy\yahtzee\yahtzee\game_state_values.pkl'
PRECOMP_STATE_VALUES = pkl.load(open(PRECOMP_PATH, "rb"))


class OptimalPlayer:

    def __init__(self, game_state_values=PRECOMP_STATE_VALUES):

        self.game_state_values = game_state_values
        self.current_game_state = tuple([False] * 13)
        self.current_turn_state = (0, None)
        self.turn_policy = {}
        self.history = []

    def set_game_state(self, game_state):
        print('set_game_state')
        self.current_game_state = game_state

        policy, values = solve_turn(self.current_game_state,
                                    self.game_state_values)
        self.turn_policy = policy
        self.turn_values = values
        print('set_game_state done')

    def set_turn_state(self, turn_state):
        print('set_turn_state')
        print(turn_state)
        self.current_turn_state = turn_state

    def get_action(self):
        print('get_action')
        roll = self.current_turn_state[0]
        print('roll: ', roll)
        if roll > 0:
            action = self.turn_policy[self.current_turn_state]
            print('action: ', action)
        else:
            action = (0, 0, 0, 0, 0, 0)

        if isinstance(action, tuple):
            action = subtract_dice_states(self.current_turn_state[1],
                                          action)

        return action

    def get_value(self):
        roll = self.current_turn_state[0]
        if roll > 0:
            value = self.turn_values[self.current_turn_state]
        else:
            value = self.game_state_values[self.current_game_state]
        return value


