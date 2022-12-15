import nimm

board = nimm.board.Board()

p1 = nimm.player.PlayerHuman(board)
p2 = nimm.player.PlayerComputer(board, start=False)

game = nimm.game.Game(p1=p1, p2=p2, board=board)

game.play()

