import itertools
import numpy as np


def _make_board(size: int=5)->np.ndarray:
    """ initialise board with size <size> """
    board = np.ones((size, size*2-1))
    for row in range(size):
        board[row,0:row*2] = 0
    return board[::-1,::-1]
    

class Board:
    """
    Playing Board class for the nimm game.
    Object to interact with when playing the game
    """
    def __init__(self, pos: np.ndarray=None, size: int=4)->None:
        self._moves = []
        self._board = _make_board(size) if pos is None else pos.copy()
        self._turn = True
        return None


    def push_mv(self, mv: list)->bool:
        """ quick push fcn compatible with legal moves """
        return self.push(mv[0], (mv[1], mv[2]))
    

    def push(self, row: int, col: tuple)->bool:
        """
        push a move given by the row index and the
        column specified by a tuple from start to end
         Example:
         Board:
          1
          1 1
          1 1 1 
          1 1 1 0
          0 0 0 0 0
         Move:
          row = 2, col = (0,2)
         Board:
          1
          1 1
          0 0 0
          1 1 1 0
          0 0 0 0 0

        Returns: True if move was processed. 
        """
        assert len(col)==2, f'column argument needs to be tuple with '+\
            f'length 2, but is: {col}'
        _lm = self.get_legal_moves()
        if [row, *col] not in _lm.tolist():
            raise ValueError(f'Move: {row=} {col=} not in legal moves: {_lm}')
        assert np.sum(self._board[row, col[0]:col[1]+1])>0, \
            f'sum of board elements zero: {self._board[row, col[0]:col[1]+1]}'
        self._board[row, col[0]:col[1]+1] = 0
        self._moves.append([row, col])
        self._turn = not self._turn
        # if self.is_gameover():
        #     print(f'Game Over!')
        #     print(f'Winner is: {self.winner()}')
        return True
    
    
    def get_legal_moves(self)->list:
        """
        get all legal moves in the current position as a list.
        Okay ive overthought this, just get all moves and
        check if theyre actually changing the board is fast enough. 
        """
        rws = np.linspace(0, self._board.shape[0]-1,
                          self._board.shape[0], dtype=int)
        cls = np.linspace(0, self._board.shape[1]-1,
                          self._board.shape[1], dtype=int)
        mvs = np.array([[rw, lwr, upr] for rw, lwr, upr in itertools.product(
            rws, cls, cls) if lwr<=upr])
        msk = np.array([np.sum(self._board[mvs[i,0], mvs[i,1]:mvs[i,2]+1])>0
                        for i in range(len(mvs))])
        return mvs[msk]


    def winner(self)->str:
        if self.is_gameover():
            return 'Player 1' if self._turn else 'Player 2'
        else:
            return 'Game not terminated yet!'

    
    def is_gameover(self)->bool:
        return np.sum(self._board)==0
    

    def turn(self)->bool:
        return self._turn
    

    def __repr__(self)->str:
        _lst = [''.join([' X ' if self._board[i,j] else ' O '
                         for j in range(self._board.shape[1])])
                for i in range(self._board.shape[0])]
        _str = '\n'.join(_lst)
        return _str
