import numpy as np

class UltimateTicTacToe:
    def __init__(self, board_size=(3,3,3,3)):
        self.board_size = board_size
        self.board = np.concatenate([np.zeros(board_size+(2,)), np.ones(board_size+(1,))], axis=-1).astype(np.float32)
        self.large_board = np.concatenate([np.zeros(board_size[:2]+(2,)), np.ones(board_size[:2]+(1,))], axis=-1).astype(np.float32)

        self.eye3 = np.eye(3).astype(np.float32)
        self.eye2 = np.eye(2).astype(np.float32)
        self.eye9 = np.eye(9).astype(np.float32)

        self.current_player = 0
        self.move_count = 0
        self.legal_zones = np.ones(board_size[:2])
        self.winner = None

    def display_board(self):
        for i in range(self.board_size[0]):
            for j in range(self.board_size[1]):
                print(f"Large Board [{i}][{j}]:")
                for k in range(self.board_size[2]):
                    for l in range(self.board_size[3]):
                        cell_value = self.board[i][j][k][l]
                        print(self.board_symbol(cell_value), end=" ")
                    print()
                print()

    def board_symbol(self, cell):
        if cell[0] == 1:
            return "X"
        elif cell[1] == 1:
            return "O"
        else:
            return "-"

    def make_move(self, move):
        large_row, large_col, small_row, small_col = move

        # Check if the move is valid
        game_over = self.winner is not None
        spot_taken = self.board[large_row, large_col, small_row, small_col, 2] == 0
        # sub_game_over = self.large_board[large_row, large_col, 2] == 0
        # prev_sub_game_over = self.large_board[self.last_move[0], self.last_move[1], 2] == 0 if self.last_move is not None else False
        legal_zone = self.legal_zones[large_row, large_col] == 1

        if (
            game_over
            or spot_taken
            or not legal_zone
        ):
            print("Invalid move. Try again.")
            return False

        # Make the move
        self.board[large_row, large_col, small_row, small_col, self.current_player] = 1
        self.board[large_row, large_col, small_row, small_col, 2] = 0

        # Check for a win in the small board
        if self.check_small_board_win(large_row, large_col, small_row, small_col):
            self.large_board[large_row, large_col, self.current_player] = 1
            self.large_board[large_row, large_col, 2] = 0

            # Check for a win in the large board
            if self.check_large_board_win(large_row, large_col):
                self.winner = self.current_player
                print(f"Player {self.current_player} wins!!!")
            
        if self.large_board[small_row, small_col, 2] == 0:
            self.legal_zones = self.large_board[..., 2]
        else:
            self.legal_zones = np.zeros((3,3))
            self.legal_zones[small_row, small_col] = 1
        # Switch to the other player
        self.current_player = 1 - self.current_player
        
        self.move_count += 1 

        return True

    def check_small_board_win(self, large_row, large_col, small_row, small_col):
        # Check row, column, and diagonal
        row = self.board[large_row, large_col, small_row, :, self.current_player]
        col = self.board[large_row, large_col, :, small_col, self.current_player]
        diag1 = np.diag(self.board[large_row, large_col, :, :, self.current_player])
        diag2 = np.diag(np.fliplr(self.board[large_row, large_col, :, :, self.current_player]))

        win_array = np.stack([row, col, diag1, diag2])

        return np.any(
            np.all(win_array, axis=-1)
        )

    def check_large_board_win(self, large_row, large_col):
        # Check row, column, and diagonal
        row = self.large_board[large_row, :, self.current_player]
        col = self.large_board[:, large_col, self.current_player]
        diag1 = np.diag(self.large_board[:, :, self.current_player])
        diag2 = np.diag(np.fliplr(self.large_board[:, :, self.current_player]))

        win_array = np.stack([row, col, diag1, diag2])

        return np.any(
            np.all(win_array, axis=-1)
        )
    
    def get_winner(self):
        return self.winner
    
    def get_current_player(self):
        return self.current_player
    
    def flat_game_state(self):
        return np.concatenate([
            self.board.flatten(),
            self.large_board.flatten(),
            self.legal_zones.flatten(),
            self.eye2[self.current_player]
        ], axis=0).astype(np.float32)
        

if __name__ == "main": # Example usage:
    game = UltimateTicTacToe()
    game.display_board()

    while not game.winner:
        move = tuple(map(int, input("Enter your move (large_row, large_col, small_row, small_col): ").split()))
        game.make_move(move)
        game.display_board()

    print(f"Player {game.winner} wins!")
