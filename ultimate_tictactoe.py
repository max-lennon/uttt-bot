import numpy as np

class UltimateTicTacToe:
    def __init__(self, board_size=(3,3,3,3)):
        self.board_size = board_size
        self.board = np.concatenate([np.zeros(board_size+(2,)), np.ones(board_size+(1,))], axis=-1).astype(np.float32)
        self.large_board = np.concatenate([np.zeros(board_size[:2]+(2,)), np.ones(board_size[:2]+(1,))], axis=-1).astype(np.float32)

        self.eye3 = np.eye(3).astype(np.float32)
        self.eye2 = np.eye(2).astype(np.float32)
        self.eye9 = np.eye(9).astype(np.float32)

        self.completed_square = [
            np.concatenate([np.ones(board_size[2:4]+(1,)), np.zeros(board_size[2:4]+(2,))], axis=-1).astype(np.float32), 
            np.concatenate([np.zeros(board_size[2:4]+(1,)), np.ones(board_size[2:4]+(1,)), np.zeros(board_size[2:4]+(1,))], axis=-1).astype(np.float32)
        ]

        self.current_player = 0
        self.move_count = 0
        self.legal_zones = np.ones(board_size[:2])
        self.winner = 2

        self.move_history = []

    def display_board(self):
        large_rows = [[] for _ in range(9)]
        for i in range(self.board_size[0]):
            for j in range(self.board_size[1]):
                for k in range(self.board_size[2]):
                    sub_row = " ".join([self.board_symbol(cell) for cell in self.board[i][j][k]])
                    large_rows[i*3+k].append(sub_row)

        for i in range(9):
            print("   ".join(large_rows[i]))
            if i % 3 == 2:
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
        game_over = self.winner < 2
        spot_taken = self.board[large_row, large_col, small_row, small_col, 2] == 0
        illegal_zone = self.legal_zones[large_row, large_col] == 0

        if (
            game_over
            or spot_taken
            or illegal_zone
        ):
            print("Invalid move. Try again.")
            return False

        # Make the move
        self.board[large_row, large_col, small_row, small_col, self.current_player] = 1
        self.board[large_row, large_col, small_row, small_col, 2] = 0

        self.move_history.append(move)

        # Check for a win in the small board
        if self.check_small_board_win(large_row, large_col, small_row, small_col):
            self.large_board[large_row, large_col, self.current_player] = 1
            self.large_board[large_row, large_col, 2] = 0
            self.board[large_row, large_col, ...] = self.completed_square[self.current_player]

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
    
    def get_game_state(self):
        return np.concatenate([
            self.board.flatten(),
            self.large_board.flatten(),
            self.legal_zones.flatten(),
            self.eye2[self.current_player],
            self.eye3[self.winner]
        ], axis=0).astype(np.float32)
    
    def load_game_state(self, game_state):
        assert len(game_state) == 284
        self.board = game_state[0:243].reshape(self.board.shape)
        self.large_board = game_state[243:270].reshape(self.large_board.shape)
        self.legal_zones = game_state[270:279].reshape(self.legal_zones.shape)
        self.current_player = np.argmax(game_state[279:281])
        self.winner = np.argmax(game_state[281:])

    def enumerate_possible_moves(self):
        move_list = []
        for large_row in range(3):
            for large_col in range(3):
                if self.legal_zones[large_row, large_col]:
                    for small_coords in zip(*np.nonzero(self.board[large_row, large_col, ..., 2])):
                        move_list.append((large_row, large_col) + small_coords)

        return move_list
            

if __name__ == "main": # Example usage:
    game = UltimateTicTacToe()
    game.display_board()

    while not game.winner:
        move = tuple(map(int, input("Enter your move (large_row, large_col, small_row, small_col): ").split()))
        game.make_move(move)
        game.display_board()

    print(f"Player {game.winner} wins!")
