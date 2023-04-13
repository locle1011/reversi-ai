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

def corner_capture(gstate: GameState):
    corners = [(0,0), (0, 7), (7, 0), (7, 7)]
    board = gstate.board
    x_corners, o_corners = 0, 0
    for corner in corners:
        if (board[corner] == 1):
            x_corners += 1
        elif (board[corner] == -1):
            o_corners += 1

    return x_corners - o_corners

def mobility(gstate: GameState):
    pass
    x_move = len(gstate.possible_move(1))
    o_move = len(gstate.possible_move(-1))
    
    if (x_move - o_move == 0):
        return 0
    
    return x_move - o_move

def count_stability(gstate: GameState):
    """
    Đếm số lượng quân cờ ổn định trên bàn cờ
    """
    directions = [(-1, -1), (-1, 0), (0, -1), (1, -1),
              (-1, 1), (0, 1), (1, 0), (1, 1)]
    state = gstate.board
    stability = 0
    for i in range(8):
        for j in range(8):
            if state[i][j] != 0:
                is_stable = True
                for dx, dy in directions:
                    x, y = i + dx, j + dy
                    while (x in range(8)) and (y in range(8)):
                        if state[x][y] == 0:
                            is_stable = False
                            break
                        if state[x][y] == state[i][j]:
                            break
                        x, y = x + dx, y + dy
                    if not is_stable:
                        break
                if is_stable:
                    stability += 1
    return stability


def heuristic_stability(state):
    stability = count_stability(state)
    return stability


def weight_value(gstate: GameState):
    board = gstate.board

    value_matrix = np.array([[100, -20, 10, 5, 5, 10, -20, 100],
                            [-20, -50, -2, -2, -2, -2, -50, -20],
                            [10, -2, -1, 1, 1, -1, -2, 10],
                            [5, -2, 1, 1, 1, 1, -2, 5],
                            [5, -2, 1, 1, 1, 1, -2, 5],
                            [10, -2, -1, 1, 1, -1, -2, 10],
                            [-20, -50, -2, -2, -2, -2, -50, -20],
                            [100, -20, 10, 5, 5, 10, -20, 100]])

    # value_matrix = np.array([[4,-3,2,2,2,2,-3,4],
    #                         [-3,-4,-1,-1,-1,-1,-4,-3],
    #                         [2,-1,1,0,0,1,-1,2],
    #                         [2,-1,0,1,1,0,-1,2],
    #                         [2,-1,0,1,1,0,-1,2],
    #                         [2,-1,1,0,0,1,-1,2],
    #                         [-3,-4,-1,-1,-1,-1,-4,-3],
    #                         [4,-3,2,2,2,2,-3,-4]])

    result = 0
    for i in range(0, 8):
        for j in range(0, 8):
            if board[i][j] == 1:
                mult = 1
            elif board[i][j] == -1:
                mult = -1
            else: mult = 0
            result += mult * value_matrix[i][j]
        # print(result)
    
    return result


class Valuer:
    def __init__(self, use_coin_parity: bool = True, use_weight_value: bool = False, 
                 use_corner_capture: bool = False, use_mobility: bool = False,
                 use_stability: bool = False,
                 weight: list = []):
        self.heuristic_func = []
        if use_coin_parity:
            self.heuristic_func.append(coin_parity)
        if use_weight_value:
            self.heuristic_func.append(weight_value)
        if use_corner_capture:
            self.heuristic_func.append(corner_capture)
        if use_mobility:
            self.heuristic_func.append(mobility)
        if use_stability:
            self.heuristic_func.append(heuristic_stability)
        if weight:
            self.weight = weight
        else:
            self.weight = [1]*len(self.heuristic_func)

    def __call__(self, gstate: GameState):
        value = 0
        for w, f in zip(self.weight, self.heuristic_func):
            value += w*f(gstate)
            # print(f(gstate))
        return value
