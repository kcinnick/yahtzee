import time

import pyautogui

from yahtzee.payoffs import compute_payoff
from yahtzee.dice import dice_to_state, state_to_dice

global dice_str


class InteractiveGame:

    def __init__(self, game_state=None, app_controller=None, turn_state=None):

        if game_state is None:
            game_state = (False,) * 13
        self.game_state = game_state
        self.app_controller = app_controller

        if turn_state is None:
            turn_state = (0, None)
        self.turn_state = turn_state

        self.history = []

    def receive_action(self, action):
        roll = self.turn_state[0]

        if isinstance(action, tuple):
            # Validate action (TODO)
            assert roll <= 2
            assert len(action) == 6
            assert sum(action) <= 5

            # Roll the dice
            dice_ls = self.roll_dice(action=action)
            print(32)
            self.turn_state = (roll + 1, dice_to_state(dice_ls))
        else:
            assert isinstance(action, int)

    def roll_dice(self, action=None):
        global dice_str
        if action is None:
            action = (5,)

        while True:
            if sum(action) == 5:
                print_str = "\tRoll all of your dice! "
                print(print_str)
                self.app_controller.click_resume_button()
                time.sleep(0.1)
                #self.app_controller.click_roll_button()
            else:
                rolled_dice = [str(d) for d in state_to_dice(action)]
                print_str = "\tRe-roll the following dice: {}. ".format(", ".join(rolled_dice))
                print_str += "Press 'Enter' to select the dice you don't want to re-roll. "
                #input(print_str)
                print('Selecting the dice you want to keep. ')
                time.sleep(0.5)
                #self.app_controller.click_resume_button()
                # click the dice you want to keep
                print(dice_str)
                dice_to_click = []
                for position, value in dice_str.items():
                    if str(value) not in rolled_dice:
                        dice_to_click.append(position)

                print('dice_to_click:', dice_to_click)
                # pyautogui.keyDown('alt')
                # pyautogui.keyDown('tab')
                # pyautogui.keyUp('tab')
                # pyautogui.keyUp('alt')
                time.sleep(0.1)
                for i in range(5):
                    if i in dice_to_click:
                        # click the die that has the position of i
                        #input('Click the die that has the position of {} and hit enter when ready'.format(i))
                        print('Clicking die ', i)
                        self.app_controller.click_die(i)
                        time.sleep(0.25)
                    else:
                        pass

                print("Re-rolling the dice you didn't select. ")
                time.sleep(0.5)
                self.app_controller.click_roll_button()

            time.sleep(2)
            print_str += "\n\tEnter all of your dice here: "
            print('Taking a screenshot of the dice')
            #self.app_controller.click_resume_button()
            time.sleep(2)
            self.app_controller.get_dice_screenshots()
            dice_str = self.app_controller.get_dice_str()
            print('dice_str:', dice_str.values())
            dice_str_response = str(input('Is dice_str correct? If not, enter correct dice_str. If so, enter nothing.\n>'))
            pyautogui.keyDown('alt')
            pyautogui.keyDown('tab')
            pyautogui.keyUp('tab')
            pyautogui.keyUp('alt')
            print('Clicking resume')
            time.sleep(0.1)
            self.app_controller.click_resume_button()
            if dice_str_response == '':
                dice_ls = [x for x in dice_str.values()]
            else:
                dice_ls = [int(x) for x in dice_str_response]
            print('dice_ls:', dice_ls)


            # Validate dice (TODO)
            is_valid = (len(dice_ls) == 5 and all([x >= 1 and x <= 6 for x in dice_ls]))
            if is_valid:
                break

            print("Error! '{}' isn't valid input. Let's try this again...".format(dice_str))

        return tuple(dice_ls)

    def start_turn(self):
        print('87')
        self.turn_state = (1, dice_to_state(self.roll_dice()))

    def end_turn(self, action):
        # Update the game history
        dice_state = self.turn_state[1]
        score = compute_payoff(action, dice_state)
        self.history.append((action, score))

        # Update the game state
        self.game_state = self.game_state[:action] \
                          + (True,) \
                          + self.game_state[action + 1:]

        # Reset the turn state
        self.turn_state = (0, None)
