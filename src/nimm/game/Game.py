from ..board import Board
from ..player import Player


class Game:
    """
    Game-Loop for the nimm game.
    """
    def __init__(self, p1: Player, p2: Player, board: Board) -> None:
        self._p1 = p1
        self._p2 = p2
        self._board = board
        print('Starting Position for nimm game: ')
        print(self._board)

    def play(self) -> None:
        """ gameplay loop """
        while not self._board.is_gameover():
            if self._board.turn():
                self._p1.push()
            else:
                self._p2.push()
            print(self._board)
        print(f'Winner is: {self._board.winner()}')
        return None
