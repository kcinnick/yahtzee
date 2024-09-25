from yahtzee.app_controller import AppController
from time import sleep

def test_get_dice_screenshots():
    sleep(1)
    app_controller = AppController()
    app_controller.get_dice_screenshots()

def test_get_dice_str():
    app_controller = AppController()
    assert app_controller.get_dice_str()
