import base64
import time
import cv2
import pyautogui

from .payoffs import compute_payoff
from .dice import dice_to_state, state_to_dice
from tqdm import tqdm


def click_roll_button(driver):
    print(driver.swipe(738, 2915, 738, 2915, duration=1000))
    return


def crop_and_save_screenshot(X, Y, H, W, source_file_name, dest_file_name):
    img = cv2.imread(source_file_name)

    crop_img = img[Y:Y + H, X:X + W]
    cv2.imwrite(
        dest_file_name,
        crop_img
    )

    return


def screenshot_dice():
    # left, top, width, and height

    # first die
    pyautogui.screenshot(r'C:\Users\Nick\PycharmProjects\yahtzee\screenshots\first_dice.png',
                         region=(835, 680, 35, 40))

    # second die
    pyautogui.screenshot(r'C:\Users\Nick\PycharmProjects\yahtzee\screenshots\second_dice.png',
                         region=(890, 680, 35, 40))

    # third die
    pyautogui.screenshot(r'C:\Users\Nick\PycharmProjects\yahtzee\screenshots\third_dice.png',
                         region=(943, 680, 35, 40))

    # fourth die
    pyautogui.screenshot(r'C:\Users\Nick\PycharmProjects\yahtzee\screenshots\fourth_dice.png',
                         region=(997, 680, 35, 40))

    # fifth die
    pyautogui.screenshot(r'C:\Users\Nick\PycharmProjects\yahtzee\screenshots\fifth_dice.png',
                         region=(1050, 680, 35, 40))
    return


class InteractiveGame:

    def __init__(self, game_state=None, turn_state=None, driver=None):
        self.driver = driver
        if game_state is None:
            game_state = (False,) * 13
        self.game_state = game_state

        if turn_state is None:
            turn_state = (0, None)
        self.turn_state = turn_state

        self.history = []

    def receive_action(self, action):
        print('receive_action')
        print('Action: {}'.format(action))
        roll = self.turn_state[0]


        if isinstance(action, tuple):
            # Validate action (TODO)
            print('Validating action.')
            assert roll <= 2
            assert len(action) == 6
            assert sum(action) <= 5
            print('Assertions passed.')

            # Roll the dice
            dice_ls = self.roll_dice(action=action)
            print('78')
            self.turn_state = (roll + 1, dice_to_state(dice_ls))
        else:
            assert isinstance(action, int)

    def roll_dice(self, action=None):
        print('Rolling dice. Action: {}'.format(action))
        if action:
            print('Sum of action: {}'.format(sum(action)))
        else:
            print('No action.')

        if action is None:
            action = (5,)

        while True:
            if sum(action) == 5:
                print_str = "\tRoll all of your dice! "
                # check for roll button
            else:
                if action:
                    print('Action: {}'.format(action))
                    print('Sum of action: {}'.format(sum(action)))
                    rolled_dice = [str(d) for d in state_to_dice(action)]
                    print_str = "\tRe-roll the following dice: {}. ".format(", ".join(rolled_dice))
                    print_str += 'Press enter when finished.\n>'
                    input(print_str)
                    # click unpause button after this input
                    pyautogui.click(1047, 806)
                else:
                    print_str = ""
                    print('No action.')

            print_str += "\n\tEnter all of your dice here: "

            for _ in tqdm(range(0, 5), desc='Rolling dice.'):
                time.sleep(1)

            print_str += "\n\tEnter all of your dice here: "
            print('Screenshotting dice.')
            # screenshot the dice
            screenshot_dice()
            print('Dice screenshot complete.')
            # get individual dice values
            dice_str = self.get_dice_str()
            print('Dice string: {}'.format(dice_str))
            dice_ls = [int(x) for x in dice_str if x.isdigit()]

            # Validate dice (TODO)
            is_valid = (len(dice_ls) == 5 and all([x >= 1 and x <= 6 for x in dice_ls]))
            if is_valid:
                break

            print("Error! '{}' isn't valid input. Let's try this again...".format(dice_str))

        return tuple(dice_ls)

    def start_turn(self):
        self.turn_state = (1, dice_to_state(self.roll_dice()))
        print('117')

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

    def get_dice_str(self):
        print('Getting dice string.')
        dice_str = ''
        # check the value of each screenshot compared to the canonical image of each die
        # the highest similarity value is the value of the die
        die_dict = {1: 'first', 2: 'second', 3: 'third', 4: 'fourth', 5: 'fifth'}
        for i in range(1, 6):
            die_value = None
            max_value = 0
            die_name = die_dict[i]
            for canonical_image in range(1, 7):
                canonical_image_path = r'C:\Users\Nick\PycharmProjects\yahtzee\canonical_images\{}.png'.format(
                    canonical_image)
                screenshot_path = r'C:\Users\Nick\PycharmProjects\yahtzee\screenshots\{}_dice.png'.format(die_name)
                canonical_image = cv2.imread(canonical_image_path)
                screenshot = cv2.imread(screenshot_path)
                # compare the canonical image to the screenshot using matchTemplate
                result = cv2.matchTemplate(screenshot, canonical_image, cv2.TM_CCOEFF_NORMED)
                # get the highest similarity value
                max_val = cv2.minMaxLoc(result)[1]
                #print('Max value: {}'.format(max_val))
                # if the similarity value is higher than the previous highest value, update the max_value
                if max_val > max_value:
                    max_value = max_val
                    die_value = [i for i in canonical_image_path if i.isdigit()][0]
            # get the value of the die
            #print('Die value for die {}: {}'.format(i, die_value))
            dice_str += die_value

        return dice_str
