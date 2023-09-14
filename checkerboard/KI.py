#Minimax-algorhythmus mit Bewertungfunktion

import pygame
import random
from .constants import ROWS, COLS, RED, WHITE
from .board import Board

class minimax:

    def __init__(self, win):
        self.board = Board()
        self.turn = RED
        self.selected = None
        self.valid_moves = {}
        self.all_valid_moves = []
        self.chosen_move = []
        self.win = win

    def get_random_move(self, move_list):
        n = random.randint(0, len(move_list)-1)
        self.chosen_move = move_list[n]
        return self.chosen_move

    def get_all_valid_moves(self):
        amount_piece_moves = 0
        self.change_turn()
        self.board.get_all_pieces(WHITE)
        for row in range(ROWS):
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    piece = self.board.get_piece(row, col)
                    if piece != 0 and self.turn == WHITE and piece.color == WHITE:
                        self.valid_moves = self.board.get_valid_moves(piece)
                        if self.valid_moves != {}:
                            self.all_valid_moves.append(self.valid_moves)
                            amount_piece_moves += 1
        self.get_random_move(self.all_valid_moves)
        print('There are', amount_piece_moves, 'pieces that can move')
        print(self.chosen_move)
        print(self.all_valid_moves)

    def choose_piece(self):
        # Extract the key(s) from the dictionary
        self.chosen_move = list(self.chosen_move.keys())

        # If you expect multiple keys, you can iterate through the list
        for key in self.chosen_move:
            print(key)
        r = random.randint(0, len(self.chosen_move)-1)
        row, col = self.chosen_move[r]
        print(row, col)
        return row, col, r

    def ai_move(self):
        row, col, r = self.choose_piece()
        if r == 0:
            piece = self.board.get_piece(row-1, col+1)
        else:
            piece = self.board.get_piece(row-1, col-1)
        self.selected = piece
        if self.selected and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)

    def update_ai(self):
        self.board.draw(self.win)
        pygame.display.update()

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED
