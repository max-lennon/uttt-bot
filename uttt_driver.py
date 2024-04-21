import numpy as np
from ultimate_tictactoe import UltimateTicTacToe
from game_gui import draw_board, draw_text, manual_select

import time

def get_random_move(current_game):
    all_moves = current_game.enumerate_possible_moves()
    if len(all_moves) == 0:
        return None
    move_choice = np.random.default_rng().choice(all_moves)
    return move_choice

def advance_game(current_game, n_moves):

    for _ in range(n_moves):
        if current_game.outcome != 3:
            return
        move = get_random_move(current_game)
        current_game.make_move(move)

def run_game(policy_0, policy_1, move_latency=0.5, gui=True):

    if policy_0 == manual_select or policy_1 == manual_select:
        assert gui

    game = UltimateTicTacToe()
    draw_board(game)

    policies = [policy_0, policy_1]

    while True:

        valid_move = False

        (large_row, large_col, small_row, small_col) = policies[game.current_player](game)

        valid_move = game.make_move((large_row, large_col, small_row, small_col))
        
        if valid_move:
            draw_board(game)
            print(game.get_game_state())
        else:
            print("Move failed.")

        if game.get_winner() != 2:
            draw_text(f"Player {game.get_winner()} wins!")
            break
        else:
            current_player = game.get_current_player()
            draw_text(f"Player {current_player}'s turn")


        time.sleep(move_latency)

if __name__ == "__main__":
    run_game(manual_select, get_random_move)