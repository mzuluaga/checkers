import copy
import random

import pygame
from checkerboard.constants import RED, WHITE, ROWS, COLS
from checkerboard.game import Game
import numpy as np

# RED/WHITE/RED KING/WHITE KING
R = 1
W = 2
RK = 3
WK = 4

#
# Board functions
#

def empty_board() -> np.array:
  return np.zeros((8,8), np.int8)


def new_board() -> np.array:
  board = np.zeros((8,8), np.int8)
  board[0] = [0, W, 0, W, 0, W, 0, W]
  board[1] = [W, 0, W, 0, W, 0, W, 0]
  board[2] = [0, W, 0, W, 0, W, 0, W]
  board[5] = [R, 0, R, 0, R, 0, R, 0]
  board[6] = [0, R, 0, R, 0, R, 0, R]
  board[7] = [R, 0, R, 0, R, 0, R, 0]
  return board

def print_board(board):
  print('Board:')
  print('   0 1 2 3 4 5 6 7')
  for i in range(8):
    print(f'{i} {board[i,:]}')


def extract_board(game):
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


def move(board, m):
  # move only moves one move.
  # this move is assumed to be valid!
  (pr, pc), (r, c) = m
  piece = board[pr, pc]
  if abs(r - pr) > 1 or abs(c - pc) > 1:
    mr = (r + pr) // 2
    mc = (c + pc) // 2
    board[mr, mc] = 0

  board[pr, pc] = 0

  # check queen promotion.
  if piece == W and r == 7:
    piece = WK
  elif piece == R and r == 0:
    piece = RK
  board[r, c] = piece
  return board


def count_red(board):
    return np.count_nonzero((board == R) | (board == RK))

def count_red_kings(board):
    return np.count_nonzero((board == RK))

def count_white(board):
    return np.count_nonzero((board == W) | (board == WK))

def count_white_kings(board):
    return np.count_nonzero((board == WK))

def check_piece(turn):
  return W if turn == WHITE else R

def check_king(turn):
  return WK if turn == WHITE else RK

def check_color(piece):
    if piece in [R or RK]:
        color = RED
    elif piece in [W, WK]:
        color = WHITE
    else:
        color = 0
    return color

def check_bounds(x, y):
  return 0 <= x <= 7 and 0 <= y <= 7

def check_winner(board):
    if count_white(board) == 0:
        return 'Red won!'
    elif count_red(board) == 0:
        return 'White won!'
    return 'Es ist Unentschieden!'


def check_moves(board, piece, row, col, jumped, og_row, og_col):
    moves = []
    row = row
    col = col
    color = check_color(piece)
    if piece == R:
        if check_bounds(row-1, col+1) and board[row-1][col+1] == 0 and not jumped:
            moves.append(((og_row, og_col), (row-1, col+1)))
        if check_bounds(row-1, col-1) and board[row-1][col-1] == 0 and not jumped:
            moves.append(((og_row, og_col), (row-1, col-1)))
        if check_bounds(row-2, col+2) and board[row-1][col+1] in [W, WK] and board[row-2][col+2] == 0:
            moves.append(((og_row, og_col), (row-2, col+2)))
            jumped = True
            newboard = board
            newboard[row][col] = 0
            newboard[row-1][col+1] = 0
            newboard[row-2][col+2] = piece
            moves2 = check_moves(newboard, piece, row-2, col+2, jumped, og_row, og_col)
            moves.extend(moves2)
        if check_bounds(row-2, col-2) and board[row-1][col-1] in [W, WK] and board[row-2][col-2] == 0:
            moves.append(((og_row, og_col), (row-2, col-2)))
            jumped = True
            newboard = board
            newboard[row][col] = 0
            newboard[row-1][col-1] = 0
            newboard[row-2][col-2] = piece
            moves2 = check_moves(newboard, piece, row-2, col-2, jumped, og_row, og_col)
            moves.extend(moves2)

    if piece == W:
        if check_bounds(row+1, col+1) and board[row+1][col+1] == 0 and not jumped:
            moves.append(((og_row, og_col), (row+1, col+1)))
        if check_bounds(row+1, col-1) and board[row+1][col-1] == 0 and not jumped:
            moves.append(((og_row, og_col), (row+1, col-1)))
        if check_bounds(row+2, col+2) and board[row+1][col+1] in [R or RK] and board[row+2][col+2] == 0:
            moves.append(((og_row, og_col), (row+2, col+2)))
            jumped = True
            newboard = board
            newboard[row][col] = 0
            newboard[row+1][col+1] = 0
            newboard[row+2][col+2] = piece
            moves2 = check_moves(newboard, piece, row+2, col+2, jumped, og_row, og_col)
            moves.extend(moves2)
        if check_bounds(row+2, col-2) and board[row+1][col-1] in [R or RK] and board[row+2][col-2] == 0:
            moves.append(((og_row, og_col), (row+2, col-2)))
            jumped = True
            newboard = board
            newboard[row][col] = 0
            newboard[row+1][col-1] = 0
            newboard[row+2][col-2] = piece
            moves2 = check_moves(newboard, piece, row+2, col-2, jumped, og_row, og_col)
            moves.extend(moves2)

    if piece == (RK or WK):
        if check_bounds(row-1, col+1) and board[row-1][col+1] == 0 and not jumped:
            moves.append(((og_row, og_col), (row-1, col+1)))
        if check_bounds(row-1, col-1) and board[row-1][col-1] == 0 and not jumped:
            moves.append(((og_row, og_col), (row-1, col-1)))
        if check_bounds(row+1, col+1) and board[row+1][col+1] == 0 and not jumped:
            moves.append(((og_row, og_col), (row+1, col+1)))
        if check_bounds(row+1, col-1) and board[row+1][col-1] == 0 and not jumped:
            moves.append(((og_row, og_col), (row+1, col-1)))
        if check_bounds(row-2, col+2) and check_color(board[row-1][col+1]) != (color and 0) and board[row-2][col+2] == 0:
            moves.append(((og_row, og_col), (row-2, col+2)))
            jumped = True
            newboard = board
            newboard[row][col] = 0
            newboard[row-1][col+1] = 0
            newboard[row-2][col+2] = piece
            moves2 = check_moves(newboard, piece, row-2, col+2, jumped, og_row, og_col)
            moves.extend(moves2)
        if check_bounds(row-2, col-2) and check_color(board[row-1][col-1]) != (color and 0) and board[row-2][col-2] == 0:
            moves.append(((og_row, og_col), (row-2, col-2)))
            jumped = True
            newboard = board
            newboard[row][col] = 0
            newboard[row-1][col-1] = 0
            newboard[row-2][col-2] = piece
            moves2 = check_moves(newboard, piece, row-2, col-2, jumped, og_row, og_col)
            moves.extend(moves2)

        if check_bounds(row+2, col+2) and check_color(board[row+1][col+1]) != (color and 0) and board[row+2][col+2] == 0:
            moves.append(((og_row, og_col), (row+2, col+2)))
            jumped = True
            newboard = board
            newboard[row][col] = 0
            newboard[row+1][col+1] = 0
            newboard[row+2][col+2] = piece
            moves2 = check_moves(newboard, piece, row+2, col+2, jumped, og_row, og_col)
            moves.extend(moves2)
        if check_bounds(row+2, col-2) and check_color(board[row+1][col-1]) == (color and 0) and board[row+2][col-2] == 0:
            moves.append(((og_row, og_col), (row+2, col-2)))
            jumped = True
            newboard = board
            newboard[row][col] = 0
            newboard[row+1][col-1] = 0
            newboard[row+2][col-2] = piece
            moves2 = check_moves(newboard, piece, row+2, col-2, jumped, og_row, og_col)
            moves.extend(moves2)

    moves = list(set(moves))
    return moves


def get_valid_moves(board, turn):
    piece_color = check_piece(turn)
    king_color = check_king(turn)
    original_game = board.copy()
    all_moves = []
    piece_moves = 0
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece not in [piece_color, king_color]:
                continue
            # Now it checks only the pieces whose turn it is
            valid_moves = check_moves(board, piece, row, col, False, row, col)
            all_moves.extend(valid_moves)
            if valid_moves:
                piece_moves += 1
            board = original_game.copy()
    # print('There are', piece_moves, 'pieces that can move')
    return all_moves


def evaluate(board, turn):
    # Checks the accepted color of piece and king
    piece_color = check_piece(turn)
    king_color = check_king(turn)
    if turn == WHITE:
        # Parameter1 berechnet die Differenz der Anzahl Figuren
        p1 = count_white(board) - count_red(board)
        # Parameter2 berechnet die Differenz der Anzahl Damen
        p2 = count_white_kings(board) - count_red_kings(board)
        # Parameter3 berechnet die durchschnittliche Distanz der Spielsteine vom Anfang
        amount = 0
        p3 = 0
        p4 = 0
        p5 = 0
        for row in range(ROWS):
            for col in range(COLS):
                piece = board[row][col]
                if piece == piece_color or piece == king_color:
                    p3 = p3 + row/10
                    amount += 1
                    # Parameter 4 schaut, ob gegnerische Figuren vor einer unbeschützten Figur stehen
                    if 1 <= row <= 6 and 1 <= col <= 6:
                        if board[row-1][col-1] == 0 and board[row+1][col+1] in [R or RK]:
                            p4 = p4 - 1
                        if board[row-1][col+1] == 0 and board[row+1][col-1] in [R or RK]:
                            p4 = p4 - 1
                # Parameter 5 macht, dass die Damen zu den mittleren Reihen gehen wollen, für Kontrolle
                if piece == king_color:
                    if row <= 3:
                        p5 = p5 + row*0.25
                    else:
                        p5 = p5 + (7-row)*0.25
        if amount != 0:
            p3 = p3/amount
        if count_white_kings(board) != 0:
            p5 = p5/count_white_kings(board)
    else:
        p1 = count_red(board) - count_white(board)
        p2 = count_red_kings(board) - count_white_kings(board)
        amount = 0
        p3 = 0
        p4 = 0
        p5 = 0
        for row in range(ROWS):
            for col in range(COLS):
                piece = board[row][col]
                if piece == piece_color or piece == king_color:
                    p3 = p3 + (7-row)/10
                    amount += 1
                    if 1 <= row <= 6 and 1 <= col <= 6:
                        if board[row+1][col+1] == 0 and board[row-1][col-1] in [W, WK]:
                            p4 = p4 - 1
                        if board[row+1][col-1] == 0 and board[row-1][col+1] in [W, WK]:
                            p4 = p4 - 1
                if piece == king_color:
                    if row <= 3:
                        p5 = p5 + row*0.25
                    else:
                        p5 = p5 + (7-row)*0.25
        if amount != 0:
            p3 = p3/amount
        if count_red_kings(board) != 0:
            p5 = p5/count_red_kings(board)

    p6 = random.randint(0, 10) / 10000

    strength = sum([p1, p2, p3, p4, p5, p6])
    return strength
