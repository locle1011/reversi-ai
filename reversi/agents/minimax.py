from .base import Agent
from .heuristic import Valuer
from ..agents import random
from ..agents import GameState, INT_MAX, INT_MIN


class MinimaxAgent(Agent):
    def __init__(self, gstate: GameState, player_icon, depth: int, valuer: Valuer):
        super().__init__(gstate, player_icon)
        self.depth = depth
        self.valuer = valuer

    def minimax(self, gstate: GameState, depth, player):
        if depth == 0 or gstate.is_end():
            return None, player*self.valuer(gstate)

        best_score = INT_MIN
        candidates = []
        for move, state in gstate.expand(player):
            score = -self.minimax(state, depth-1, -player)[-1]
            if best_score < score:
                best_score = score
                candidates = [move]
                if score == 65:
                    break
            elif score == best_score:
                candidates.append(move)

        best_move = random.choice(candidates) if candidates else None
        return best_move, best_score

    def find_best_move(self):
        return self.minimax(self.gstate, self.depth, self.player_icon)[0]


class AlphaBetaAgent(MinimaxAgent):
    def minimax_alpha_beta(self, gstate: GameState, depth, player, alpha=INT_MIN, beta=INT_MAX):
        if depth == 0 or gstate.is_end():
            return None, player*self.valuer(gstate)

        best_score = INT_MIN
        candidates = []
        for move, state in gstate.expand(player):
            score = - \
                self.minimax_alpha_beta(
                    state, depth-1, -player, -beta, -alpha)[-1]
            if best_score < score:
                best_score = score
                candidates = [move]
                alpha = max(alpha, score)
                if alpha > beta:
                    break
            elif score == best_score:
                candidates.append(move)

        best_move = random.choice(candidates) if candidates else None
        return best_move, best_score

    def find_best_move(self):
        return self.minimax_alpha_beta(self.gstate, self.depth, self.player_icon)[0]


class NegaScoutAgent(MinimaxAgent):
    def pvs(self, gstate: GameState, depth, player, alpha=INT_MIN, beta=INT_MAX):
        if depth == 0 or gstate.is_end():
            return None, player*self.valuer(gstate)

        candidates = []
        best_score = INT_MIN
        first_child = True
        for move, state in gstate.expand(player):
            if first_child:
                first_child = False
                score = -self.pvs(state,
                                  depth-1, -player, -beta, -alpha)[-1]
            else:
                score = - \
                    self.pvs(
                        state, depth-1, -player, -alpha-1, -alpha)[-1]
                if alpha < score < beta:
                    score = -self.pvs(state, depth-1, -
                                      player, -beta, -score)[-1]

            if best_score < score:
                best_score = score
                candidates = [move]
                alpha = max(alpha, score)
                if alpha > beta:
                    break
            elif score == best_score:
                candidates.append(move)

        best_move = random.choice(candidates) if candidates else None
        return best_move, best_score

    def find_best_move(self):
        return self.pvs(self.gstate, self.depth, self.player_icon)[0]
