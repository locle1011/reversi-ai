from reversi import np
from reversi import INIT_BOARD, INIT_MOVE
from reversi import X, O, EMPTY

DIRECTIONS = [(-1, -1), (-1, 0), (0, -1), (1, -1),
              (-1, 1), (0, 1), (1, 0), (1, 1)]


class GameState:
    def __init__(self, board=INIT_BOARD, X_score=2, O_score=2):
        self.board = board.copy()
        self.X_score = X_score
        self.O_score = O_score
        self.X_last_move = INIT_MOVE
        self.O_last_move = INIT_MOVE

    def __call__(self, other):
        self.board = other.board
        self.X_score = other.X_score
        self.O_score = other.O_score
        self.X_last_move = other.X_last_move
        self.O_last_move = other.O_last_move

    def __str__(self) -> str:
        s = self.board.astype(str)
        s = np.char.replace(s, '0', '|')
        s = np.char.replace(s, '-1', 'O')
        s = np.char.replace(s, '1', 'X')
        s = '\n'.join(line for line in map('|'.join, s.tolist()))
        res = f"""{s}
{'-'*30}
X: {self.X_score} - Last move: {self.X_last_move}
O: {self.O_score} - Last move: {self.O_last_move}
"""
        return res

    def __repr__(self) -> str:
        return str(self)

    def copy(self):
        other = GameState(self.board, self.X_score, self.O_score)
        other.X_last_move, other.O_last_move = self.X_last_move, self.O_last_move
        return other

    @property
    def winner(self):
        if self.is_end():
            # Find winner
            if self.X_score > self.O_score:
                return 'X'
            elif self.X_score < self.O_score:
                return 'O'
            else:
                return 'Draw'
        else:
            return None

    def is_end(self):
        if self.X_score + self.O_score == 64:
            return True

        if self.X_last_move is INIT_MOVE is self.O_last_move:
            return not self.possible_move(X) and not self.possible_move(O)
        return not self.X_last_move and not self.O_last_move

    def possible_move(self, player_icon):
        enemy_icon = -player_icon
        res = dict()
        for disc in zip(*np.where(self.board == player_icon)):
            for d in DIRECTIONS:
                coord = disc[0] + d[0], disc[1] + d[1]
                if 0 <= coord[0] < 8 and 0 <= coord[1] < 8 and self.board[coord] == enemy_icon:
                    while self.board[coord] == enemy_icon:
                        coord = coord[0] + d[0], coord[1] + d[1]
                        if coord[0] > 7 or coord[0] < 0 or coord[1] > 7 or coord[1] < 0:
                            break
                    else:
                        if self.board[coord] == EMPTY:
                            res.setdefault(coord, [])
                            res[coord].append(disc)
        if res:
            return res.items()
        else:
            return [None]

    def to_next_state(self, move, player_icon):
        score = 0
        if move:
            start = move[0]
            for end in move[1]:
                if start[0] == end[0]:
                    if start[1] > end[1]:
                        ni = -1
                        score += start[1] - end[1] - 1
                    else:
                        ni = 1
                        score += end[1] - start[1] - 1
                    self.board[start[0], start[1]:end[1]:ni] = player_icon
                elif start[1] == end[1]:
                    if start[0] > end[0]:
                        ni = -1
                        score += start[0] - end[0] - 1
                    else:
                        ni = 1
                        score += end[0] - start[0] - 1
                    self.board[start[0]:end[0]:ni, start[1]] = player_icon
                else:
                    if start[1] > end[1]:
                        ci = -1
                        score += start[1] - end[1] - 1
                    else:
                        ci = 1
                        score += end[1] - start[1] - 1

                    if start[0] > end[0]:
                        ri = -1
                    else:
                        ri = 1

                    self.board[range(start[0], end[0], ri), range(
                        start[1], end[1], ci)] = player_icon

            if player_icon == X:
                self.X_score += score + 1
                self.O_score -= score
                self.X_last_move = move[0]
            else:
                self.X_score -= score
                self.O_score += score + 1
                self.O_last_move = move[0]
        else:
            if player_icon == X:
                self.X_last_move = None
            else:
                self.O_last_move = None

        return self

    def expand(self, player_icon):
        for move in self.possible_move(player_icon):
            yield move, self.copy().to_next_state(move, player_icon)
