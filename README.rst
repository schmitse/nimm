nimm
====

game `nimm` which is a turn based game with the objective to not pick up the last straw from the table.

Install dependencies with ::

  pip install -e $THIS_DIRECTORY/nimm

====

How to play the game? Create a Board, Player, and a Game instance and play :) ::

  import nimm

  board = nimm.board.Board()
  p1 = nimm.player.PlayerHuman(board)
  p2 = nimm.player.PlayerComputer(board, start=False)

  game = nimm.game.Game(p1=p1, p2=p2, board=board)
  game.play()

Or use the `Play.py` script for inspiration. 

====

Pre-commit setup ::

  python -m pip install pre-commit
  pre-commit install
