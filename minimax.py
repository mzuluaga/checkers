#Minimax-algorhythmus mit Bewertungfunktion

import pygame
import random
from checkerboard.constants import ROWS, COLS, RED, WHITE
from checkerboard.board import Board

class Minimax:

    def get_all_valid_moves(self, board, turn):
      all_valid_moves = []
      amount_piece_moves = 0
      pieces = board.get_all_pieces(turn)
      print('pieces:', pieces)

      for row in range(ROWS):
        for col in range(COLS):
          piece = board.get_piece(row, col)
          if piece == 0 or piece.color != turn:
            continue
          # Now check only pieces whose turn is to move.
          valid_moves = board.get_valid_moves(piece)
          print('piece:', piece.color, piece.row, piece.col, valid_moves)
          for (mr, mc) in valid_moves.keys():
            all_valid_moves.append(((piece.row, piece.col), (mr, mc)))
            amount_piece_moves += 1
      print('There are', amount_piece_moves, 'pieces that can move')
      return all_valid_moves

    def move(self, board, turn):
      valid_moves = self.get_all_valid_moves(board, turn)
      print('Valid Moves:', valid_moves)
      return random.choice(valid_moves)
