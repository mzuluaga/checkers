#Minimax-algorhythmus mit Bewertungfunktion

import pygame
import random
from .constants import ROWS, COLS, RED, WHITE
from .board import Board

class Minimax:

    def __init__(self):
        self.board = None
        self.turn = None
        self.selected = None
        self.valid_moves = {}
        self.all_valid_moves = []
        self.chosen_move = []

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
        print('Chosen piece:', self.chosen_move)
        print('Valid Moves:', self.all_valid_moves)

    def choose_random_piece(self):
        # Extract the key(s) from the dictionary
        self.chosen_move = list(self.chosen_move.keys())

        # If you expect multiple keys, you can iterate through the list
        for key in self.chosen_move:
            print(key)
        r = random.randint(0, len(self.chosen_move)-1)
        row, col = self.chosen_move[r]
        print(f'Chosen: (row, col) = ({row}, {col})')
        return row, col

    def move(self, board, turn):
        self.board = board
        self.turn = turn
        # implement
        return (2, 3), (3, 2)
