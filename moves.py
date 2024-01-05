import copy
import random

import pygame
from checkerboard.constants import RED, WHITE, ROWS, COLS
from checkerboard.game import Game
import numpy as np

# RED/WHITE/RED KING/WHITE KING
R, W, RK, WK = 1, 2, 3, 4

def get_color(piece):
  if piece in [R or RK]:
    color = RED
  elif piece in [W, WK]:
    color = WHITE
  else:
    color = 0
  return color

def check_bounds(x, y):
  return 0 <= x <= 7 and 0 <= y <= 7

def check_direction(m, piece):
  ((pr, pc), (r, c)) = m
  if piece == R:
    return pr > r
  if piece == W:
    return pr < r
  return piece in [RK, WK]

def check_jump_over_oponent_piece(board, m, piece):
  ((pr, pc), (r, c)) = m
  mr = (r + pr) // 2
  mc = (c + pc) // 2
  color = get_color(piece)
  oponent_color = get_color(board[mr, mc])
  # print(f'color vs. oponent_color = {color} vs. {oponent_color}')
  return (color == RED and oponent_color == WHITE) or (color == WHITE and oponent_color == RED)

def move(board, m):
  """Updates board with a single move."""
  (pr, pc), (r, c) = m
  piece = board[pr, pc]
  capturing_piece = abs(r - pr) > 1 or abs(c - pc) > 1
  if capturing_piece:
    mr = (r + pr) // 2
    mc = (c + pc) // 2
    board[mr, mc] = 0
  board[pr, pc] = 0
  if piece == W and r == 7:
    piece = WK
  elif piece == R and r == 0:
    piece = RK
  board[r, c] = piece
  return board


def filter_piece_moves(board, r, c, candidates, is_jump):
  valid = []
  piece = board[r, c]
  for (cr, cc) in candidates:
    m = ((r, c), (cr, cc))
    if not check_bounds(cr, cc):
      # print(f'Filter bounds {m}')
      continue
    if board[cr, cc] != 0:
      # print(f'Candidate cell is not empty {m}')
      continue
    if not check_direction(m, piece):
      # print(f'Filter direction {m}')
      continue
    if is_jump:
      if not check_jump_over_oponent_piece(board, m, piece):
        # print(f'Filter not jumping over oponent {m} {piece}')
        continue
    valid.append(m)
  return valid

def get_piece_walk_moves(board, r, c):
  candidates = [(r-1, c-1), (r-1, c+1), (r+1, c-1), (r+1, c+1)]
  moves = filter_piece_moves(board, r, c, candidates, is_jump=False)
  #print(moves)
  return moves

def get_piece_jump_moves(board, r, c):
  candidates = [(r-2, c-2), (r-2, c+2), (r+2, c-2), (r+2, c+2)]
  moves = filter_piece_moves(board, r, c, candidates, is_jump=True)
  return moves

def get_piece_moves(board, row, col):
  all_candidates = get_piece_walk_moves(board, row, col)
  all_candidates.extend(get_piece_jump_moves(board, row, col))
  print(all_candidates)
  return all_candidates

def get_moves(board, turn):
  piece_color = get_piece(turn)
  king_color = get_king(turn)
  original_game = board.copy()
  all_moves = []
  piece_moves = 0
  for row in range(ROWS):
    for col in range(COLS):
      piece = board[row][col]
      if piece not in [piece_color, king_color]:
        continue
      # Now it checks only the pieces whose turn it is
      #valid_moves = get_piece_moves(board, piece, row, col, False, row, col)
      valid_moves = get_piece_moves(board, row, col)
      all_moves.extend(valid_moves)
      if valid_moves:
        piece_moves += 1
      board = original_game.copy()
  # print('There are', piece_moves, 'pieces that can move')
  board = original_game.copy()
  return all_moves
