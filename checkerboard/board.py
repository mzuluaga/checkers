#Hier werde ich alle Spielzüge definieren und wie sie auf das Brett gezeichnet werden
import pygame
from .constants import BLACK, ROWS, WHITE, SQUARE_SIZE, COLS, RED
from .piece import Piece
import numpy as  np

R, W, RK, WK = 1, 2, 3, 4


class Board:
    def __init__(self):
        self.create_board()
        print('Board at Creation time:', self.board)

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):                     #Modulo ermöglicht, dass bei geradener Reihe nur geradene Spalten gefüllt werden
            for col in range(row % 2, ROWS, 2):     #Der ganze Bildschirm ist schwarz und jetzt füllen wir die weissen Felder ein
                pygame.draw.rect(win, WHITE, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        if row == (ROWS - 1) or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def new_board(self) -> np.array:
      board = np.zeros((8,8), np.int8)
      board[0] = [0, W, 0, W, 0, W, 0, W]
      board[1] = [W, 0, W, 0, W, 0, W, 0]
      board[2] = [0, W, 0, W, 0, W, 0, W]
      board[5] = [R, 0, R, 0, R, 0, R, 0]
      board[6] = [0, R, 0, R, 0, R, 0, R]
      board[7] = [R, 0, R, 0, R, 0, R, 0]

      # White will lose.
      # board[4] = [0, 0, 0, RK, 0, 0, 0, 0]
      # board[5] = [WK, 0, 0, 0, 0, 0, 0, 0]

      # uncomment for end-game testing.
      # board[0] = [0, W, 0, W, 0, W, 0, W]
      # board[2] = [0, 0, 0, R, 0, 0, 0, 0]
      # board[5] = [0, 0, R, 0, 0, 0, 0, 0]
      # board[6] = [0, W, 0, 0, 0, 0, 0, WK]

      # board[0] = [0, W, 0, W, 0, 0, 0, 0]
      # board[2] = [0, 0, 0, R, 0, 0, 0, 0]
      # board[5] = [0, 0, R, 0, 0, 0, 0, 0]
      # board[6] = [0, WK, 0, 0, 0, 0, 0, 0]

      # board[0] = [0, 0, 0, 0, 0, 0, 0, 0]
      # board[1] = [0, 0, W, 0, 0, 0, 0, 0]
      # board[2] = [0, 0, 0, 0, 0, W, 0, 0]
      # board[3] = [0, 0, W, 0, W, 0, 0, 0]
      # board[4] = [0, 0, 0, R, 0, W, 0, 0]
      # board[5] = [0, 0, 0, 0, R, 0, 0, 0]

      return board

    def create_board(self):
      b = self.new_board()
      self.red_left = np.count_nonzero((b == R) | (b == RK))
      self.white_left = np.count_nonzero((b == W) | (b == WK))
      self.red_kings = np.count_nonzero((b == RK))
      self.white_kings = np.count_nonzero((b == WK))
      self.board = []
      for i in range(ROWS):
        self.board.append([])
        for j in range(COLS):
          piece = 0
          if b[i, j] == R:
            piece = Piece(i, j, RED)
          elif b[i, j] == W:
            piece = Piece(i, j, WHITE)
          elif b[i, j] == RK:
            piece = Piece(i, j, RED, king=True)
          elif b[i, j] == WK:
            piece = Piece(i, j, WHITE, king=True)
          self.board[i].append(piece)
      print(f'red_left: {self.red_left} white_left: {self.white_left}')
      print(f'red_kings: {self.red_kings} white_kings: {self.white_kings}')

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def get_valid_moves(self, piece):
        print()
        moves = {}
        r, c = piece.row, piece.col
        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(r-1, max(r-3, -1), -1, piece.color, c-1))
            moves.update(self._traverse_right(r-1, max(r-3, -1), -1, piece.color, c+1))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(r+1, min(r+3, ROWS), 1, piece.color, c-1))
            moves.update(self._traverse_right(r+1, min(r+3, ROWS), 1, piece.color, c+1))
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                moves[(r, left)] = last + skipped
                if last:
                    row = max(r-3, -1) if step == -1 else min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            left -= 1
        if moves:
          print(f'tl: row_range({start}:{stop}:{step})={list(range(start, stop, step))}, color={color}, left={left}, skipped={skipped}')
          print(f'>> tl: moves={moves}')
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                moves[(r, right)] = last + skipped
                if last:
                    row = max(r-3, -1) if step == -1 else min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        if moves:
          print(f'tr: row_range({start}:{stop}:{step})={list(range(start, stop, step))}, color={color}, right={right}, skipped={skipped}')
          print(f'>> tr: moves={moves}')
        return moves
