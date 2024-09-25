import pyautogui
from time import sleep

import cv2


class AppController:
    def __init__(self):
        return

    def click_die(self, die_position):
        # die_position is an integer from 1 to 5
        # click on the die in the corresponding position
        if die_position == 1:
            pyautogui.click(833, 677)
        elif die_position == 2:
            pyautogui.click(886, 677)
        elif die_position == 3:
            pyautogui.click(940, 677)
        elif die_position == 4:
            pyautogui.click(994, 677)
        elif die_position == 5:
            pyautogui.click(1048, 677)
        else:
            print('Invalid die position')
        return

    def get_dice_screenshots(self):
        # left, top, width, and height
        pyautogui.screenshot(
            r'C:\Users\Nick\PycharmProjects\yahtzee\images\dice_position_1.png',
            region=(833, 677, 44, 44)
        )
        pyautogui.screenshot(
            r'C:\Users\Nick\PycharmProjects\yahtzee\images\dice_position_2.png',
            region=(886, 677, 44, 44)
        )
        pyautogui.screenshot(
            r'C:\Users\Nick\PycharmProjects\yahtzee\images\dice_position_3.png',
            region=(940, 677, 44, 44)
        )
        pyautogui.screenshot(
            r'C:\Users\Nick\PycharmProjects\yahtzee\images\dice_position_4.png',
            region=(994, 677, 44, 44)
        )
        pyautogui.screenshot(
            r'C:\Users\Nick\PycharmProjects\yahtzee\images\dice_position_5.png',
            region=(1048, 677, 44, 44)
        )

        return

    def click_roll_button(self):
        pyautogui.click(958, 828)
        return

    def click_resume_button(self):
        pyautogui.click(1046, 805)
        return

    def get_dice_str(self):
        # use cv2 to read each dice_position image and compare it to each dice_value image
        # use the matchTemplate function to compare the two images and save the best match
        # return the best match as a string

        die_dict = {}
        for i in range(1, 6):
            #print('Checking value of die in position ' + str(i))
            dice_position_image_path = r'C:\Users\Nick\PycharmProjects\yahtzee\images\dice_position_' + str(i) + '.png'
            #print(dice_position_image_path)
            dice_position = cv2.imread(r'C:\Users\Nick\PycharmProjects\yahtzee\images\dice_position_' + str(i) + '.png')
            # compare to each dice value image and save the highest match
            highest_match = 0
            for j in range(1, 7):
                dice_value_image_path = r'C:\Users\Nick\PycharmProjects\yahtzee\images\static\dice_value_' + str(j) + '.png'
                #print(dice_value_image_path)
                dice_value = cv2.imread(r'C:\Users\Nick\PycharmProjects\yahtzee\images\static\dice_value_' + str(j) + '.png')
                result = cv2.matchTemplate(dice_position, dice_value, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                if max_val > highest_match:
                    highest_match = max_val
                    highest_match_dice = j

            print(highest_match_dice)
            die_dict[i] = highest_match_dice

        return die_dict
