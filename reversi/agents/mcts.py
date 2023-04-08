import numpy as np

from .base import Agent, RandomAgent
from .heuristic import Valuer
from ..agents import random
from ..agents import GameState, INT_MAX, INT_MIN


class MCTSNode:
    def __init__(self, game_state: GameState, valuer: Valuer, parent=None):
        self.gameState = game_state
        self.simulationNumber = 0
        self.totalPoints = 0
        self.parent = parent
        self.children = None
        self.moves = None
        self.unexpanded_actions = None
        self.get_result = valuer

    @property
    def n(self):
        return self.simulationNumber

    @property
    def q(self):
        return self.totalPoints

    def is_terminal_node(self):
        return self.gameState.is_end()

    def is_fully_expanded(self):
        if self.unexpanded_actions is not None and len(self.unexpanded_actions) == 0:
            return True
        return False

    def get_unexpanded_child(self, player_icon):
        if self.unexpanded_actions is None:
            self.children = list()
            self.moves = list()
            self.unexpanded_actions = [(game_state, move) for move, game_state
                                       in self.gameState.expand(player_icon)]

        expanded_action = self.unexpanded_actions.pop()
        self.moves.append(expanded_action[1])
        child = MCTSNode(expanded_action[0], self.get_result, self)
        self.children.append(child)
        return child

    def get_best_child(self, c=1.4):
        weights = [(child.q / child.n) + c * np.sqrt((2 * np.log(self.n)) / child.n)
                   for child in self.children]
        return self.children[np.argmax(weights)]

    def get_best_move(self, c=1.4):
        weights = [(child.q / child.n) + c * np.sqrt((2 * np.log(self.n)) / child.n)
                   for child in self.children]
        return self.moves[np.argmax(weights)]

    def do_rollout_policy(self):
        pass

    def simulate(self, player_icon):
        current_game_state = self.gameState.copy()

        while not current_game_state.is_end():
            RandomAgent(current_game_state, player_icon).move()
            player_icon = -player_icon

        return self.get_result(current_game_state)

    def backpropagate(self, reward):
        self.simulationNumber += 1
        self.totalPoints += reward
        if self.parent:
            self.parent.backpropagate(reward)

    def clean(self):
        self.simulationNumber = 0
        self.totalPoints = 0
        self.parent = None
        del self.children
        self.children = None
        del self.moves
        self.moves = None
        del self.unexpanded_actions
        self.unexpanded_actions = None


class MCTSAgent(Agent):
    def __init__(self, game_state: GameState, player_icon, valuer: Valuer):
        super().__init__(game_state, player_icon)
        self.root = None
        if game_state:
            self.root = MCTSNode(game_state, valuer)
        self.playerIcon = None
        if player_icon:
            self.playerIcon = player_icon
        self.valuer = valuer

    def __call__(self, game_state: GameState, player_icon):
        self.root = MCTSNode(game_state, self.valuer)
        self.playerIcon = player_icon

    def do_tree_policy(self):
        player_icon = self.playerIcon
        current_node = self.root
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                next_player_icon = -player_icon
                return current_node.get_unexpanded_child(player_icon), next_player_icon
            else:
                player_icon = -player_icon
                current_node = current_node.get_best_child()

        return current_node, player_icon

    def find_best_move(self, simulation_number=100):
        for _ in range(simulation_number):
            child, player_icon = self.do_tree_policy()
            reward = child.simulate(player_icon) * self.playerIcon
            child.backpropagate(reward)
        return self.root.get_best_move()

    def move(self):
        move = self.find_best_move(100)
        self.root.gameState.to_next_state(move, self.playerIcon)
        self.root.clean()
