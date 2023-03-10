import os
import itertools
from functools import partial
import tkinter as tk
from PIL import Image, ImageTk
from glob import glob
import numpy as np

from ..board import Board
from ..player import Player, PlayerHuman, PlayerComputer


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
        self.window = root

        self._setup_window()

    def _click_buttons(self, move: list) -> None:
        row = move[0]
        start, stop = move[1:]
        for j in range(start, stop + 1):
            self._buttons[row * self._board._board.shape[1] + j]['state'] = 'disabled'

    def _clicked(self, i, j) -> None:
        """ save and disable the button """
        self._clicked_buttons.append([i, j])
        self._buttons[i * self._board._board.shape[1] + j]['state'] = 'disabled'
        return None

    def _popup_error(self) -> None:
        window = tk.Toplevel()
        window.wm_title('Illegal Move!')
        rows = np.array([pair[0] for pair in self._clicked_buttons])
        label = tk.Label(window, text=f'You may only choose one row at a time but chose: {rows}')
        label.grid(row=0, column=0)
        btn = tk.Button(window, text='Alright!', command=window.destroy)
        btn.grid(row=0, column=1)

    def _setup_window(self) -> None:
        """
        creates window with all buttons and texts
        depending on size of playing board
        """
        self._board.reset()
        rows, columns = self._board._board.shape
        msize = int(1150 / columns)
        self.player_turn = tk.Label(text='Player 1 Turn')
        self.player_turn.grid(row=0, column=2)
        b_sub = tk.Button(text='Submit Selection', width=20,
                          height=4, bg='white', fg='black',
                          command=self._submit)
        b_sub.grid(row=0, column=int(columns / 2))

        self._buttons = []
        self._images = []
        _td = os.path.dirname(os.path.realpath(__file__))
        files = glob(f'{_td}/../backgrounds/*jpg')
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
                _button.grid(row=i + 1, column=j + rows - i - 1)
            self._buttons.append(_button)
        return None

    def _submit(self) -> None:
        """ submit the move you have selected, action will be taken on button press """
        # assert len(self._clicked_buttons), 'Please select buttons. '
        rows = np.array([pair[0] for pair in self._clicked_buttons])
        cols = np.sort([pair[1] for pair in self._clicked_buttons])
        if (self._board.turn() and self._p1.is_human()) or \
           (not self._board.turn() and self._p2.is_human()):
            assert len(self._clicked_buttons), 'Please select buttons. '
            if not np.all(rows == rows[0]):
                print(f'Error, you may only choose from one row! {rows}')
                self._unclick_buttons()
                return None
            move = [rows[0], cols[0], cols[-1]]
        else:
            move = []
        if self._board.turn():
            mv = self._p1.push_gui(move)
        else:
            mv = self._p2.push_gui(move)
        self._click_buttons(mv)
        turntext = 'Player 1 Turn' if self._board.turn() else 'Player 2 Turn'
        self.player_turn.config(text=turntext)
        if self._board.is_gameover():
            label = tk.Label(text=f'Winner is {self._board.winner()}')
            label.grid(row=0, column=4)
            replay_button = tk.Button(text='Replay', width=20, height=4,
                                      bg='white', fg='black',
                                      command=self._setup_window)
            replay_button.grid(row=0, column=5)
        self._clicked_buttons.clear()
        return None

    def _unclick_buttons(self) -> None:
        self._popup_error()
        for i, j in self._clicked_buttons:
            self._buttons[i * self._board._board.shape[1] + j]['state'] = 'active'
        self._clicked_buttons.clear()


def play_1v1():
    root = tk.Tk()
    root.title('NIMM')
    root.geometry('1200x1200')

    board = Board()
    p1 = PlayerHuman(board)
    p2 = PlayerHuman(board, start=False)

    NimmGUI(root, p1, p2, board)

    root.mainloop()


def play_gui():
    root = tk.Tk()
    root.title('NIMM')
    root.geometry('1200x1200')

    board = Board()

    player_opts = ['human', 'computer']

    p1_cls_str = tk.StringVar(root)
    p1_cls_str.set(player_opts[0])
    p1_menu = tk.OptionMenu(root, p1_cls_str, *player_opts)
    p1_menu.grid(row=0, column=0)

    p2_cls_str = tk.StringVar(root)
    p2_cls_str.set(player_opts[1])
    p2_menu = tk.OptionMenu(root, p2_cls_str, *player_opts)
    p2_menu.grid(row=1, column=0)

    player_classes = {'human': PlayerHuman, 'computer': PlayerComputer}

    dfcs = [int(i) for i in range(10)]
    dfc1 = tk.IntVar(root)
    dfc1.set(dfcs[0])
    dfc1_menu = tk.OptionMenu(root, dfc1, *dfcs)
    dfc1_menu.grid(row=0, column=1)

    dfc2 = tk.IntVar(root)
    dfc2.set(dfcs[0])
    dfc2_menu = tk.OptionMenu(root, dfc2, *dfcs)
    dfc2_menu.grid(row=1, column=1)

    def startfcn() -> None:
        p1fcn = partial(player_classes[p1_cls_str.get()], board=board, start=True,
                        difficulty=dfc1.get())
        p2fcn = partial(player_classes[p2_cls_str.get()], board=board, start=False,
                        difficulty=dfc2.get())
        p1_menu.grid_remove()
        p2_menu.grid_remove()
        dfc1_menu.grid_remove()
        dfc2_menu.grid_remove()
        start_button.grid_remove()
        p1 = p1fcn()
        p2 = p2fcn()

        print(p1, p1.is_human(), p1.is_turn())
        print(p2, p2.is_human(), p2.is_turn())

        NimmGUI(root, p1, p2, board)

    start_button = tk.Button(text='Start Game', command=startfcn)
    start_button.grid(row=0, column=2)

    root.mainloop()
