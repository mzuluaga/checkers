#Minimax-algorhythmus mit Bewertungfunktion
# Colab: https://colab.research.google.com/drive/1FJ2rwYxLjdzZyJRGS4CwQPacruhvl5t2#scrollTo=cnkCeQRZEtNa

import copy
import random
from checkerboard.constants import RED, WHITE
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from PIL import Image

# RED/WHITE/RED KING/WHITE KING
R=1
W=2
RK=3
WK=4

#
# Board functions
#

def empty_board() -> np.array:
  return np.zeros((8,8), np.int8)


def init_board() -> np.array:
  board = empty_board()
  board[0] = [W, 0, W, 0, W, 0, W, 0]
  board[1] = [0, W, 0, W, 0, W, 0, W]
  board[2] = [W, 0, W, 0, W, 0, W, 0]
  board[5] = [0, R, 0, R, 0, R, 0, R]
  board[6] = [R, 0, R, 0, R, 0, R, 0]
  board[7] = [0, R, 0, R, 0, R, 0, R]
  return board


def plot_board(board: np.array):
  array = np.ones([8, 8, 3], dtype=np.uint8)
  array[:] = [64, 96, 255]  #light blue
  array[board == R] = [255, 0, 0]
  array[board == W] = [255, 255, 255]
  array[board == RK] = [255, 125, 0]
  array[board == WK] = [125, 125, 125]
  img = Image.fromarray(array)
  img = img.resize((160, 160), Image.Resampling.NEAREST)
  fig, ax = plt.subplots(1)
  im = ax.imshow(img, origin='lower')
  ax.set_xticks(np.arange(0, 160, 20))
  ax.set_yticks(np.arange(0, 160, 20))
  ax.set_xticklabels(np.arange(0, 8, 1))
  ax.set_yticklabels(np.arange(0, 8, 1))
  plt.show()


def print_board(board: np.array):
  print('Board:')
  print('', f'{board[::-1]}'[1:-1])


def extract_board(game):
  board = empty_board()
  board = np.zeros((8,8), np.int8)
  for game_row in game.board.board:
    for piece in game_row:
      if piece == 0:
        continue
      if piece.king:
        p = RK if piece.color == RED else WK
      else:
        p = R if piece.color == RED else W
      board[piece.row, piece.col] = p
  return board


def move(board, from_coord, to_coord):
  # this doesn't check if the move is valid!
  r, c = from_coord
  piece = board[r, c]
  board[r, c] = 0
  r, c = to_coord

  if piece == W and r == 7:
    piece = WK
  elif piece == R and r == 0:
    piece = RK
  board[r, c] = piece
  return board


def count_red(board):
  return np.count_nonzero((board == R) | (board == RK))


def count_white(board):
  return np.count_nonzero((board == W) | (board == WK))


def check_winner(board):
  if count_white(board) == 0:
    return 'Red won!'
  elif count_red(board) == 0:
    return 'White won!'
  return 'Es ist Unentschieden!'


#
# Mateo tienes que implementar todas estas functiones pero usando el
# board que esta en este archivo.
#

def _get_all_valid_moves(board, turn):
  all_valid_moves = []
  amount_piece_moves = 0
  pieces = board.get_all_pieces(turn)
  # print('pieces:', pieces)

  for row in range(ROWS):
    for col in range(COLS):
      piece = board.get_piece(row, col)
      if piece == 0 or piece.color != turn:
        continue
      # Now check only pieces whose turn is to move.
      valid_moves = board.get_valid_moves(piece)
      # print('piece:', piece.color, piece.row, piece.col, valid_moves)
      for (mr, mc) in valid_moves.keys():
        all_valid_moves.append(((piece.row, piece.col), (mr, mc)))
        amount_piece_moves += 1
  # print('There are', amount_piece_moves, 'pieces that can move')
  return all_valid_moves


def evaluate_board(board, turn):
  w = 1 if turn == WHITE else -1
  p1 = w * (board.white_left  - board.red_left)
  p2 = w * (board.white_kings - board.red_kings)
  # Parameter3 berechnet die durchschnittliche Distanz der Spielsteine vom Anfang
  amount = 0
  p3 = 0
  for row in range(ROWS):
    for col in range(COLS):
      piece = board.get_piece(row, col)
      if piece != 0 and piece.color == turn and piece.king == False:
        p3 = p3 + (turn == WHITE)*row/10 + (turn == RED)*(7-row)/10
        # print(row, col, p3)
        amount += 1
  p3 = p3 / amount
  p4 = random.randint(0, 10) / 1000
  strength = p1 + p2 + p3 + p4
  return strength


def get_best_move(game):
  board = _extract_board(game)
  print_board(board)
  return None

  valid_moves = _get_all_valid_moves(board, turn)
  if not valid_moves:
    return None


  original_game = copy.deepcopy(board)
  max_strength = -500
  max_move = valid_moves[0]
  for i in range(len(valid_moves)):
    (pr, pc), (row, col) = valid_moves[i]
    # game.select(pr, pc)
    # game.select(row, col)
    # game.update()
    strength = evaluate_board(game.board, turn)
    if strength > max_strength:
      max_strength = strength
      max_move = valid_moves[i]
    game = copy.deepcopy(original_game)

  assert game.board == original_game.board
  (pr, pc), (row, col) = max_move
  game.select(pr, pc)
  game.select(row, col)
  game.update()

  print('The strongest move is: (pr, pc, row, col)', max_move, 'with a strength of', max_strength)
  return max_move
