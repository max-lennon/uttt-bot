import numpy as np

def enumerate_possible_moves(current_game):
    move_list = []
    for large_row in range(3):
        for large_col in range(3):
            if current_game.legal_zones[large_row, large_col]:
                for small_coords in zip(*np.nonzero(current_game.board[large_row, large_col, ..., 2])):
                    move_list.append((large_row, large_col) + small_coords)

    return move_list

def get_random_move(current_game):
    all_moves = enumerate_possible_moves(current_game)
    move_choice = np.random.default_rng().choice(all_moves)
    return move_choice