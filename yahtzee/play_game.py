import pyautogui

from yahtzee.app_controller import AppController
from yahtzee.game_player import OptimalPlayer
from yahtzee.game import InteractiveGame
from yahtzee.payoffs import PAYOFF_LS
import pickle as pkl

reward_to_coords = {
    "ones": (848, 347),
    "twos": (892, 347),
    "threes": (938, 347),
    "fours": (984, 349),
    "fives": (1028, 349),
    "sixes": (1074, 349),
    "three of a kind": (892, 495),
    "four of a kind": (892, 541),
    "full house": (1020, 450),
    "small straight": (1011, 496),
    "large straight": (1011, 542),
    "Yahtzee": (953, 588),
    "chance": (895, 451)
}
def play_game(player, game, verbose=True):

    if verbose:
        print("\n######## STARTING GAME ########\n")  
 
    # While the game isn't finished...
    turn = 0
    while False in game.game_state:
        turn += 1

        game.start_turn()
        player.set_game_state(game.game_state)
        action = 0
        
        # While the turn isn't finished... 
        while game.game_state[0] < 3:
            player.set_turn_state(game.turn_state)
            action = player.get_action()
            game.receive_action(action)

            if isinstance(action, int):
                print(PAYOFF_LS[action][0])
                from time import sleep
                game.app_controller.click_resume_button()
                sleep(0.5)
                pyautogui.click(reward_to_coords[PAYOFF_LS[action][0]])
                input("\nClaimed the '{}' reward! Press enter\n".format(PAYOFF_LS[action][0]))
                break
        
        game.end_turn(action) 
        if verbose:
            print(make_score_card(game.history))
            print("\n######## FINISHED TURN {} ########\n".format(turn))

    if verbose:
        print("Game is finished!") 
        print(make_score_card(game.history))

    return game.history


def make_score_card(player_history):
    
    scorecard = "Score card:\n"

    score_dict = {payoff_name: "__" for payoff_name, _ in PAYOFF_LS}
    total = 0
    for action, score in player_history:
        score_dict[PAYOFF_LS[action][0]] = score
        total += score

    for payoff_name, _ in PAYOFF_LS:
        scorecard += "\t{}:\t{}\n".format(payoff_name, score_dict[payoff_name])

    scorecard += "\tTOTAL: {}".format(total)

    return scorecard


def play_interactive_game():

    # Initialize an optimal player
    player = OptimalPlayer()

    # Initialize the app controller
    app_controller = AppController()
    
    # Initialize the game
    game = InteractiveGame(app_controller=app_controller)

    play_game(player, game)


if __name__=="__main__":

    play_interactive_game()


