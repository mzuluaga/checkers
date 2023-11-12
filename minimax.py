#Minimax-algorhythmus mit Bewertungfunktion

import copy
import random
from checkerboard.constants import ROWS, COLS, RED, WHITE
import numpy as np

from enum import Enum

class Cell(Enum):
  EMPTY = 0
  RED = 1
  WHITE = 2


def _extract_board(game):
  board  = np.array((ROWS, COLS), np.int32)
  print(board)
  for r, game_row in enumerate(game.board.board):
    for c, piece in enumerate(game_row):
      print(r,c)
      if piece == RED:
        board[r,c] = 1
      elif piece == WHITE:
        board[r,c] = 2
      else:
        board[r, c] = 0
  return board


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
  print('Exracted numpy board:', board)
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
