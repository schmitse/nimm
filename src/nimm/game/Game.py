import itertools
import tkinter as tk
from PIL import Image, ImageTk
from glob import glob
import numpy as np

from ..board import Board
from ..player import Player, PlayerHuman


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


class NimmGUI(tk.Frame):
    """
    Game with GUI (to be used with one of the play functions)
    """
    def __init__(self, root: tk.Tk, p1: Player,
                 p2: Player, board: Board) -> None:
        self._p1 = p1
        self._p2 = p2
        self._board = board
        self._clicked_buttons = []
        self.move = None

        self.window = root

        self._setup_window()

    def _submit(self) -> None:
        """ submit the move you have selected, action will be taken on button press """
        assert len(self._clicked_buttons), 'Please select buttons. '
        rows = np.array([pair[0] for pair in self._clicked_buttons])
        cols = np.sort([pair[1] for pair in self._clicked_buttons])
        assert np.all(rows == rows[0]), \
            f'Error, you may only choose from one row! {rows}'
        self.move = [rows[0], cols[0], cols[-1]]
        print(self.move)
        if self._board.turn():
            if self._p1.is_human():
                mv = self.move
            else:
                mv = []
            mv = self._p1.push_gui(mv)
        else:
            if self._p2.is_human():
                mv = self.move
            else:
                mv = []
            mv = self._p2.push_gui(mv)
        print(self._board)
        if self._board.is_gameover():
            print(f'Winner is {self._board.winner()}')
            label = tk.Label(text=f'Winner is {self._board.winner()}')
            label.grid(row=0, column=4)
        self._clicked_buttons.clear()
        return None

    def _clicked(self, i, j) -> None:
        """ save and disable the button """
        self._clicked_buttons.append([i, j])
        self._buttons[i * self._board._board.shape[1] + j]['state'] = 'disabled'
        print(self._clicked_buttons)
        return None

    def _setup_window(self) -> None:
        """
        creates window with all buttons and texts
        depending on size of playing board
        """
        rows, columns = self._board._board.shape
        print(self.window.winfo_geometry())
        msize = int(1150 / columns)

        b_sub = tk.Button(text='Submit Selection', width=20,
                          height=4, bg='white', fg='black',
                          command=self._submit)
        b_sub.grid(row=0, column=int(columns / 2))

        self._buttons = []
        self._images = []
        files = glob(r'src/nimm/backgrounds/*jpg')
        for ff in files:
            image = Image.open(ff)
            image = image.resize((msize, int(msize * 1.5)))
            image = ImageTk.PhotoImage(image)
            self._images.append(image)

        for i, j in itertools.product(range(rows), range(columns)):
            _button = tk.Button(self.window, width=msize, height=int(msize * 1.5),
                                image=np.random.choice(self._images), bd=0,
                                command=lambda i=i, j=j: self._clicked(i, j))
            if not (j > i * 2):
                print(i + 1, j + rows - i - 1)
                _button.grid(row=i + 1, column=j + rows - i - 1)

            self._buttons.append(_button)

        return None


def play_1v1():
    root = tk.Tk()
    root.title('NIMM')
    root.geometry('1200x1200')

    board = Board()
    p1 = PlayerHuman(board)
    p2 = PlayerHuman(board, start=False)

    NimmGUI(root, p1, p2, board)

    root.mainloop()
