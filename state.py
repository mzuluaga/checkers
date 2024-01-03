# Minimax-Algorithmus mit Bewertungsfunktion
import copy
import random

import pygame
import networkx as nx
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

def new_board() -> np.array:
    board = np.zeros((8,8), np.int8)
    board[0] = [0, W, 0, W, 0, W, 0, W]
    board[1] = [W, 0, W, 0, W, 0, W, 0]
    board[2] = [0, W, 0, W, 0, W, 0, W]
    board[5] = [R, 0, R, 0, R, 0, R, 0]
    board[6] = [0, R, 0, R, 0, R, 0, R]
    board[7] = [R, 0, R, 0, R, 0, R, 0]
    return board


def print_board(board: np.array):
    print('Board:')
    print('', f'{board[::-1]}'[1:-1])


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
    # this doesn't check if the move is valid!
    (r, c), (r1, c1) = m
    piece = board[r, c]
    board[r, c] = 0

    # Jump implemented for 1 and 2, still need 3 or more
    w = 1
    m = 1
    if r1 - r < 0:
        w = -1
    if c1 - c < 0:
        m = -1
    if (r1-r) % 2 == 0:
        if r1 - r == (2 or w*2):
            board[r1-1*w, c1-1*m] = 0
        if r1 - r == (4 or w*4 or 6 or w*6):
            if c1 - c == (4 or w*4 or 6 or w*6):
                board[r1-1*w, c1-1*m] = 0
                board[r1-3*w, c1-3*m] = 0
            else:
                # have to make for all colour!
                if (board[r1-1*w, c1+1] and board[r1-3*w, c1+1]) == (R or RK):
                    board[r1-1*w, c1+1] = 0
                    board[r1-3*w, c1+1] = 0
                else:
                    board[r1-1*w, c1-1] = 0
                    board[r1-3*w, c1-1] = 0

    if piece == W and r == 7:
        piece = WK
    elif piece == R and r == 0:
        piece = RK
    board[r1, c1] = piece
    return board


def count_red(board):
    return np.count_nonzero((board == R) | (board == RK))


def count_red_kings(board):
    return np.count_nonzero((board == RK))


def count_white(board):
    return np.count_nonzero((board == W) | (board == WK))


def count_white_kings(board):
    return np.count_nonzero((board == WK))


# Checks the accepted piece colour this turn
def check_piece(turn):
    if turn == WHITE:
        piece_color = W
    else:
        piece_color = R
    return piece_color


# Checks the accepted King Colour for this turn
def check_king(turn):
    if turn == WHITE:
        king_color = WK
    else:
        king_color = RK
    return king_color


# Checks the color of a piece
def check_color(piece):
    if piece == (R or RK):
        color = RED
    elif piece == (W or WK):
        color = WHITE
    else:
        color = 0
    return color


def check_bounds(x, y):
    if 0 <= x <= 7 and 0 <= y <= 7:
        return True
    else:
        return False


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
        if check_bounds(row-2, col+2) and board[row-1][col+1] == (W or WK) and board[row-2][col+2] == 0:
            moves.append(((og_row, og_col), (row-2, col+2)))
            jumped = True
            newboard = board
            newboard[row][col] = 0
            newboard[row-1][col+1] = 0
            newboard[row-2][col+2] = piece
            moves2 = check_moves(newboard, piece, row-2, col+2, jumped, og_row, og_col)
            moves.extend(moves2)
        if check_bounds(row-2, col-2) and board[row-1][col-1] == (W or WK) and board[row-2][col-2] == 0:
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
        if check_bounds(row+2, col+2) and board[row+1][col+1] == (R or RK) and board[row+2][col+2] == 0:
            moves.append(((og_row, og_col), (row+2, col+2)))
            jumped = True
            newboard = board
            newboard[row][col] = 0
            newboard[row+1][col+1] = 0
            newboard[row+2][col+2] = piece
            moves2 = check_moves(newboard, piece, row+2, col+2, jumped, og_row, og_col)
            moves.extend(moves2)
        if check_bounds(row+2, col-2) and board[row+1][col-1] == (R or RK) and board[row+2][col-2] == 0:
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


def get_all_valid_moves(board, turn):
    piece_color = check_piece(turn)
    king_color = check_king(turn)
    original_game = board.copy()
    all_valid_moves = []
    amount_piece_moves = 0
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != (piece_color and king_color):
                continue
            # Now it checks only the pieces whose turn it is
            valid_moves = check_moves(board, piece, row, col, False, row, col)
            board = original_game.copy()
            # If a piece has more than one valid move, the for-loop checks all of them
            for ((pr, pc), (mr, mc)) in valid_moves:
                all_valid_moves.append(((pr, pc), (mr, mc)))
            if len(valid_moves) != 0:
                amount_piece_moves += 1
    print('There are', amount_piece_moves, 'pieces that can move')
    return all_valid_moves


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
                        if board[row-1][col-1] == 0 and board[row+1][col+1] == (R or RK):
                            p4 = p4 - 1
                        if board[row-1][col+1] == 0 and board[row+1][col-1] == (R or RK):
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
                        if board[row+1][col+1] == 0 and board[row-1][col-1] == (W or WK):
                            p4 = p4 - 1
                        if board[row+1][col-1] == 0 and board[row-1][col+1] == (W or WK):
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

    p6 = random.randint(0, 10)
    p6 = p6/10000

    x_value = [p1, p2, p3, p4, p5, p6]
    return x_value


def get_best_move(game, turn):
    board = extract_board(game)
    valid_moves = get_all_valid_moves(board, turn)
    if not valid_moves:
        return None

    original_game = board.copy()
    max_strength = -500
    max_move = valid_moves[0]
    for i in range(len(valid_moves)):
        # Nimmt jeden validen Zug und spielt ihn auf der Kopie des Brettes, dieses Brett wird dann bewertet.
        (pr, pc), (row, col) = valid_moves[i]
        place_board = move(board, (pr, pc), (row, col))
        parameter = evaluate_board(place_board, turn)
        strength = sum(parameter)
        print(f'For move: {(pr, pc), (row, col)} ; There is Strength = {strength} : p1 = {parameter[0]}, p2 = {parameter[1]}, p3 = {parameter[2]}, p4 = {parameter[3]}, p5 = {parameter[4]}, p6 = {parameter[5]}')
        # Falls dieser Zug eine bessere Bewertung hat als der vorher beste, wird dieser ersetzt
        if strength > max_strength:
            max_strength = strength
            max_move = valid_moves[i]
        board = original_game.copy()

    print('The strongest move is: (pr, pc, row, col)', max_move, 'with a strength of', max_strength)
    return max_move


# Funktion für einen Bot der zufällige Züge macht
def move2(board, turn):
    valid_moves = get_all_valid_moves(board, turn)
    print('Valid Moves:', valid_moves)
    return random.choice(valid_moves)


def get_all_valid_moves2(board, turn):
    all_valid_moves = []
    amount_piece_moves = 0
    for row in range(ROWS):
        for col in range(COLS):
            piece = board.get_piece(row, col)
            if piece == 0 or piece.color != turn:
                continue
            # Now it checks only the pieces whose turn it is
            valid_moves = board.get_valid_moves(piece)
            print(valid_moves)
            # If a piece has more than one valid move, the for-loop checks all of them
            for (mr, mc) in valid_moves.keys():
                all_valid_moves.append(((piece.row, piece.col), (mr, mc)))
            if len(valid_moves) != 0:
                amount_piece_moves += 1
    print('There are', amount_piece_moves, 'pieces that can move')
    return all_valid_moves


'''
board = new_board()
board[5][4] = 0
board[4][3] = RK
board[2][1] = 0
board[3][2] = W
board[0][3] = 0
board[3][4] = W
board[2][5] = 0
board[0][7] = 0
print(board)
moves = check_moves(board, RK, 4, 3, False, 4, 3)
print(moves)
'''
