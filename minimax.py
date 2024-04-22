import numpy as np
from ultimate_tictactoe import UltimateTicTacToe

class MinimaxTreeNode:
    def __init__(self, game_state, eval_func, max_depth=3):
        self.game_state = game_state
        self.player = np.argmax(game_state[288:290])
        self.max_depth = max_depth
        self.eval_func = eval_func

        self.minimax_value = None

        self.game_over = self.game_state[-1] != 1

        if self.game_over or self.max_depth == 0:
            self.child_nodes = None
        else:
            self.child_nodes = self.get_child_nodes()
    
    def get_child_nodes(self):
        curr_game = UltimateTicTacToe()
        curr_game.load_game_state(self.game_state.copy())
        move_options = curr_game.enumerate_possible_moves()

        child_nodes = []

        for move in move_options:
            curr_game.load_game_state(self.game_state.copy())
            curr_game.make_move(move)
            child_node = MinimaxTreeNode(curr_game.get_game_state(), self.eval_func, self.max_depth-1)
            child_nodes.append(child_node)
        return child_nodes

    def get_dataset(self):
        state_batch = np.reshape(self.game_state, (1, -1))
        if self.minimax_value is None:
            self.minimax_value = self.get_minimax_value()
        
        if self.child_nodes is None:
            return state_batch, [self.minimax_value]
        
        child_dsets, child_labels = list(zip(*(child.get_dataset() for child in self.child_nodes)))

        return np.concatenate((state_batch,)+child_dsets), np.concatenate(([self.minimax_value],)+child_labels)

    def get_minimax_value(self):

        if self.game_over:
            return 0.5 if self.game_state[-2] else self.game_state[-3]
        if self.max_depth == 0 or len(self.child_nodes) == 0:
            return self.eval_func(self.game_state)

        child_values = []

        for child in self.child_nodes:
            child_values.append(child.get_minimax_value())

        self.minimax_value = np.min(child_values) if self.player == 0 else np.max(child_values)
        
        return self.minimax_value