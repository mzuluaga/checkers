#Checkersprogramm, dass mit einem Minimax-algorithmus programmiert ist

import numpy as np
import pandas as pd
import random
import pygame
from checkerboard.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkerboard.board import Board
from checkerboard.game import Game
from checkerboard.KI import minimax

import parser

results, moves = parser.run()


# Flussdiagramm zu Minimax machen!
# Checkerboard

FPS = 30

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
    minimax_instance = minimax(WIN)

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
                elif game.turn == WHITE:
                    minimax_instance.get_all_valid_moves()
                    minimax_instance.ai_move()

        game.update()

    pygame.quit()
    game.winner()


main()
