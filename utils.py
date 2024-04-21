import numpy as np

class BoardTransformation:
    def __init__(self):
        self.identity = np.arange(284)
        self.board = self.identity[0:243].reshape((3,3,3,3,3))
        self.large_board = self.identity[243:270].reshape((3,3,3))
        self.legal_zones = self.identity[270:279].reshape((3,3))

        self.perms = {}
    
    def compute_transforms(self):
        raise NotImplementedError

    def transform(self, *args):
        raise NotImplementedError

class ClockwiseRotation(BoardTransformation):
    def __init__(self):        
        super().__init__()

        self.compute_transforms()

    def compute_transforms(self):
        for i, angle in enumerate([90, 180, 270]):
            permutation = self.identity.copy()
            permutation[0:243] = np.rot90(np.rot90(self.board, k=-(i+1), axes=(0,1)), k=-(i+1), axes=(2,3)).flatten()
            permutation[243:270] = np.rot90(self.large_board, k=-(i+1), axes=(0,1)).flatten()
            permutation[270:279] = np.rot90(self.legal_zones, k=-(i+1), axes=(0,1)).flatten()

            self.perms[angle] = permutation

    def transform(self, game_state, angle):
        return game_state[self.perms[angle]]
    
class Reflection(BoardTransformation):
    def __init__(self):
        super().__init__()

        self.compute_transforms()

    def compute_transforms(self):
        for i, direction in enumerate(["vert", "horiz"]):
            permutation = self.identity.copy()
            permutation[0:243] = np.flip(self.board, axis=(i,i+2)).flatten()
            permutation[243:270] = np.flip(self.large_board, axis=i).flatten()
            permutation[270:279] = np.flip(self.legal_zones, axis=i).flatten()

            self.perms[direction] = permutation
        
        diag_reflection = self.identity.copy()
        diag_reflection[0:243] = np.transpose(self.board, axes=(1,0,3,2,4)).flatten()
        diag_reflection[243:270] = np.transpose(self.large_board, axes=(1,0,2)).flatten()
        diag_reflection[270:279] = np.transpose(self.legal_zones, axes=(1,0)).flatten()

        self.perms["diag"] = diag_reflection

        self.perms["opp_diag"] = diag_reflection[self.perms["vert"]][self.perms["horiz"]]
    
    def transform(self, game_state, direction):
        return game_state[self.perms[direction]]