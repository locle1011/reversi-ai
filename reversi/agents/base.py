from ..agents import random
from ..agents import GameState, INIT_MOVE, INT_MIN, X, O


class Agent:
    def __init__(self, gstate: GameState, player_icon):
        self.gstate = gstate
        self.player_icon = player_icon

    def __call__(self, gstate: GameState, player_icon):
        self.gstate = gstate
        self.player_icon = player_icon

    def find_best_move(self):
        return INIT_MOVE, [INIT_MOVE]

    def move(self):
        move = self.find_best_move()
        self.gstate.to_next_state(move, self.player_icon)


class RandomAgent(Agent):
    def find_best_move(self):
        return random.choice(list(self.gstate.possible_move(self.player_icon)))


class GreedyAgent(Agent):
    def __init__(self, gstate: GameState, player_icon):
        super().__init__(gstate, player_icon)

        if player_icon == X:
            self.get_candidates = GreedyAgent.get_candidates_X
        else:
            self.get_candidates = GreedyAgent.get_candidates_O

    def __call__(self, gstate: GameState, player_icon):
        self.gstate = gstate
        self.player_icon = player_icon
        if player_icon == X:
            self.get_candidates = GreedyAgent.get_candidates_X
        else:
            self.get_candidates = GreedyAgent.get_candidates_O

    @staticmethod
    def get_candidates_X(gstate: GameState):
        candidates = []
        best_score = INT_MIN
        for move, state in gstate.expand(X):
            if best_score < state.X_score:
                best_score = state.X_score
                candidates = [move]
            elif best_score == state.X_score:
                candidates.append(move)
        return candidates

    @staticmethod
    def get_candidates_O(gstate: GameState):
        candidates = []
        best_score = INT_MIN
        for move, state in gstate.expand(O):
            if best_score < state.O_score:
                best_score = state.O_score
                candidates = [move]
            elif best_score == state.O_score:
                candidates.append(move)
        return candidates

    def find_best_move(self):
        return random.choice(self.get_candidates(self.gstate))
