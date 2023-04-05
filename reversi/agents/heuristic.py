from ..agents import GameState, np


def coin_parity(gstate: GameState):
    winner = gstate.winner

    if winner == 'X':
        return 65
    elif winner == 'O':
        return -65
    elif winner == 'Draw':
        return 0
    else:
        return gstate.X_score - gstate.O_score


class Valuer:
    def __init__(self, use_coin_parity: bool, weight: list = []):
        self.heuristic_func = []
        if use_coin_parity:
            self.heuristic_func.append(coin_parity)
        if weight:
            self.weight = weight
        else:
            self.weight = [1]*len(self.heuristic_func)

    def __call__(self, gstate: GameState):
        value = 0
        for w, f in zip(self.weight, self.heuristic_func):
            value += w*f(gstate)
        return value
