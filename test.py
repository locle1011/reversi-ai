from time import time
from multiprocessing import Pool
from reversi import X, O
from reversi.state import GameState
from reversi.agents.base import Agent, RandomAgent, GreedyAgent
from reversi.agents.minimax import AlphaBetaAgent
from reversi.agents.heuristic import Valuer
from reversi.agents.mcts import MCTSAgent



def fight(X_player: Agent, O_player: Agent, X_first=True):
    gs = GameState()
    X_player(gs, X)
    O_player(gs, O)

    if X_first:
        X_player.move()
        # print(gs)
    O_player.move()
    # print(gs)

    while not gs.is_end():
        X_player.move()
        # print(gs)
        if gs.is_end():
            break
        O_player.move()
        # print(gs)

    return gs.winner


def make_stats(X_player: Agent, O_player: Agent, times=100):
    freq = {'X': 0, 'O': 0, 'Draw': 0}
    param = X_player, O_player, True
    res = []
    with Pool(6) as p:
        res += p.starmap(fight, (param for i in range(times//2)), chunksize=1)
    param = X_player, O_player, False
    with Pool(6) as p:
        res += p.starmap(fight,
                         (param for i in range(times-times//2)), chunksize=1)
    for r in res:
        freq[r] += 1
    return freq


if __name__ == "__main__":
    valuer = Valuer(use_coin_parity=True, use_weight_value=False,
                    use_corner_capture=True, use_mobility=False,
                    use_stability=False,
                    weight=[1, 1000])
    
    begin = time()
    winner = fight(AlphaBetaAgent(None, None, depth=4, valuer=valuer),
                   RandomAgent(None, None), X_first=True)
    t = time() - begin
    print(t, winner)
    begin = time()
    res = make_stats(AlphaBetaAgent(None, None, depth=4, valuer=valuer),
                   RandomAgent(None, None), times=100)
    t = time() - begin
    print(t, res)
    # begin = time()
    # winner = fight(MCTSAgent(None, None, valuer=valuer, simulation_time=100),
    #                RandomAgent(None, None), X_first=True)
    # t = time() - begin
    # print(t, winner)
    # begin = time()
    # res = make_stats(MCTSAgent(None, None, valuer=valuer, simulation_time=10),
    #                RandomAgent(None, None), times=100)
    # t = time() - begin
    # print(t, res)
    # begin = time()
    # res = make_stats(RandomAgent(None, None),
    #                  AlphaBetaAgent(None, None, depth=2, valuer=valuer) , times=100)
    # t = time() - begin
    # print(t, res)
    # begin = time()
    # res = make_stats(GreedyAgent(None, None),
    #                  RandomAgent(None, None), times=100)
    # t = time() - begin
    # print(t, res)
