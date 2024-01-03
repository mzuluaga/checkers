#Checkersprogramm, dass mit einem Minimax-algorithmus programmiert ist

import time
import pygame
import math
import networkx as nx
from checkerboard.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkerboard.game import Game
from checkerboard.board import Board
import minimax

# Flussdiagramm zu Minimax machen!
# Checkerboard

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Macht ein Window, wo wir das Checkerbrett hineinversetzen können
pygame.display.set_caption('Checkers')


def get_row_col_from_mouse(pos):        # Aus der Position der Maus wird berechnet auf welchem Feld wir sind
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    run = True
    clock = pygame.time.Clock()             # Das ermöglicht, dass die Zeit für einen Spielzug vom Computer reguliert ist
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():    #Diese For-Schleife wird gemacht um auszuwählen, ob man aufhören will zu spielen oder etwas anderes machen will
            if event.type == pygame.QUIT:
                run = False                 #Falls man den Quit button drückt wird die ganze while schleife gestoppt und das Spiel endet

            if event.type == pygame.MOUSEBUTTONDOWN:    #Falls man seine Maus klickt wird hier alles definiert zur Spielzugausführung
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)  #Wenn wir also die Maus auf einem Feld klicken, dann wird es uns diesen Code ausführen und wissen welche Spielfigur, wir gedrückt haben
                if game.turn == RED:
                    game.select(row, col)
                else:
                    # Meine Funktion nimmt das jetztige Brett und wählt einen zufälligen Spielzug und gibt die Reihe und Spalte der Figur sowie den Zug zurück
                    (pr, pc), (row, col) = minimax.get_best_move(game, game.turn)
                    #(pr, pc), (row, col) = minimax.move2(game.board, game.turn)
                    print(f'Minimax Selected: (pr, pc, row, col) = ({pr}, {pc}, {row}, {col})')
                    game.select(pr, pc)
                    game.select(row, col)

        game.update()

    pygame.quit()
    print(game.winner())


main()

