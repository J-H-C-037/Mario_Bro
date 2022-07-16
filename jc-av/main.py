from board import Board
import pyxel

board = Board(255, 255) #create a board giving its width and height

# The first thing to do is to create the screen, see API for more parameters
pyxel.init(board.width, board.height)

# Loading the pyxel file with the sprites
pyxel.load("my_resource.pyxres")

# To start the game we invoke the run method with the update and draw functions
pyxel.run(board.update, board.draw)
