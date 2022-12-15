import numpy as np
from ..board import Board


class Player:
    """
    Base Player Class for nimm game
    """
    def __init__(self, board: Board, name: str='Humy',
                 start: bool=True, difficulty: int=0)->None:
        self._name = name
        self._turn = start
        self._board = board
        self._difficulty = difficulty
        

    def is_turn(self)->bool:
        return self._board.turn()==self._turn


class PlayerHuman:
    """
    Human Player for the nimm game. 
    """
    def __init__(self, board: Board, name: str='Humy',
                 start: bool=True, difficulty: int=0)->None:
        self._name = name
        self._turn = start
        self._board = board
        self._difficulty = difficulty


    def is_turn(self)->bool:
        return self._board.turn()==self._turn


    def push(self)->bool:
        if self.is_turn():
            mv = input('Enter Move as Row, [Start, Stop]: ')
            mv = mv.replace('[', '').replace(']', '').split(',')
            row = int(mv[0])
            col = (int(mv[1]), int(mv[2]))
            print(f'Playing move: {row} {col}')
            self._board.push(row, col)
        else:
            print('Its not your turn to move!')


class PlayerComputer:
    """
    Computer Player for the nimm game.
    """
    def __init__(self, board: Board, name: str='Humy',
                 start: bool=True, difficulty: int=0)->None:
        self._name = name
        self._turn = start
        self._board = board
        self._difficulty = difficulty
        self._pad = len(np.binary_repr(board._board.shape[1]))
        
        
    def is_turn(self)->bool:
        return self._board.turn()==self._turn


    def push(self)->bool:
        if self.is_turn():
            mv = self._choose_move()
            print(f'Playing move: {mv}')
            self._board.push(mv[0], (mv[1], mv[2]))
        else:
            print(f'Its not your turn to move!')
        

    def _choose_move(self):
        """
        choose move based on sum of elements in rows.
        objective is to obtain an even number of elements
        in all rows with your move to generate a winning
        position.
        If difficulty is easy, there is the possibility to
        throw in 'wrong' moves that generate a losing position. 
        """
        mvs = self._board.get_legal_moves()
        good_moves, bad_moves = [], []
        for mv in mvs:
            _board = Board(pos=self._board._board.copy())
            _board.push_mv(mv)
            binary_sum = np.array([self._binsum(val, self._pad) for val
                                   in _board._board.sum(axis=1)])
            xor_sum = binary_sum.sum(axis=0)
            test_statistic = np.sum(xor_sum % 2) == 0
            if test_statistic:
                good_moves.append(mv)
            else:
                bad_moves.append(mv)
            
        if self._difficulty == 0:
            if len(good_moves):
                return good_moves[np.random.choice(len(good_moves))]
            else:
                return bad_moves[np.random.choice(len(bad_moves))]
        else:
            weights = np.random.exponential(self._difficulty, size=len(bad_moves))
            weights = np.append(np.ones_like(good_moves), weights)
            all_moves = good_moves + bad_moves
            return np.random.choice(all_moves, weights=weights)


    @staticmethod
    def _binsum(val: int, pad: int=3)->str:
        """ binary representation """
        binary = np.binary_repr(int(val))
        diff = pad - len(binary)
        return [int(c) for c in '0'*diff + binary]
        
