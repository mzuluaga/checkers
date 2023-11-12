# Minimax-algorhythmus mit Bewertungfunktion
import random
from checkerboard.constants import ROWS, COLS, RED, WHITE
from checkerboard.game import Game


def get_all_valid_moves(board, turn):
    all_valid_moves = []
    amount_piece_moves = 0
    pieces = board.get_all_pieces(turn)
    for row in range(ROWS):
        for col in range(COLS):
            piece = board.get_piece(row, col)
            if piece == 0 or piece.color != turn:
                continue
            # Now it checks only the pieces whose turn it is
            valid_moves = board.get_valid_moves(piece)
            # If a piece has more than one valid move, the for-loop checks all of them
            for (mr, mc) in valid_moves.keys():
                all_valid_moves.append(((piece.row, piece.col), (mr, mc)))
            if len(valid_moves) != 0:
                amount_piece_moves += 1
    print(all_valid_moves)
    print('There are', amount_piece_moves, 'pieces that can move')
    return all_valid_moves


def evaluate_board(board, turn):
    if turn == WHITE:
        # Parameter1 berechnet die Differenz der Anzahl Figuren
        p1 = board.white_left - board.red_left
        # Parameter2 berechnet die Differenz der Anzahl Damen
        p2 = board.white_kings - board.red_kings
        # Parameter3 berechnet die durchschnittliche Distanz der Spielsteine vom Anfang
        amount = 0
        p3 = 0
        for row in range(ROWS):
            for col in range(COLS):
                piece = board.get_piece(row, col)
                if piece != 0 and piece.color == turn and piece.king == False:
                    p3 = p3 + row/10
                    print(row, col, p3)
                    amount += 1
        p3 = p3/amount
    else:
        p1 = board.red_left - board.white_left
        p2 = board.red_kings - board.white_kings
        amount = 0
        p3 = 0
        for row in range(ROWS):
            for col in range(COLS):
                piece = board.get_piece(row, col)
                if piece != 0 and piece.color == turn and piece.king == False:
                    p3 = p3 + (7-row)/10
                    amount += 1
        p3 = p3/amount
    p4 = random.randint(0, 10)
    p4 = p4/1000

    strength = p1 + p2 + p3 + p4
    return strength


def move(board, turn, game):
    all_valid_moves = get_all_valid_moves(board, turn)
    original_board = board
    max_strength = -500
    max_move = all_valid_moves[0]
    for i in range(len(all_valid_moves)):
        # Nimmt jeden validen Zug und spielt ihn auf dem Brett, dieses Brett wird dann bewertet.
        (pr, pc), (row, col) = all_valid_moves[i]
        print(all_valid_moves)
        print((pr, pc), (row, col))
        game.select(pr, pc)
        game.select(row, col)
        game.update()
        strength = evaluate_board(game.board, turn)
        game.change_turn()
        print('The move: (pr, pc, row, col)', (pr, pc), (row, col), 'has a strength of', strength)
        # Falls dieser Zug eine bessere Bewertung hat als der vorher beste, wird dieser ersetzt
        if strength > max_strength:
            max_strength = strength
            max_move = all_valid_moves[i]
        #game.board = board
        # How can I reset without resetting the actual board?
        game.reset()
    game.change_turn()
    print('The strongest move is: (pr, pc, row, col)', max_move, 'with a strength of', max_strength)
    return max_move

# Funktion für einen Bot der zufällige Züge macht
#def move2(board, turn):
    #valid_moves = get_all_valid_moves(board, turn)
    #print('Valid Moves:', valid_moves)
    #return random.choice(valid_moves)



