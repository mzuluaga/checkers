#Checkersprogramm, dass mit einem Minimax-algorithmus programmiert ist

import numpy as np
import pandas as pd
import random
import pygame
from checkerboard.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkerboard.board import Board
from checkerboard.game import Game
from checkerboard.KI import minimax

def parse_game(game):
    parts = game.split('"]')                #Macht eine Liste aus einem Spiel, die bei einem [ abgetrennt werden
    moves = parts[-1]                       #Nimmt den letzten Eintrag mit all den Spielzügen
    moves = moves.replace('\n',' ')         #Zeilenumbruch wird durch Abstand ersetzt
    individual_moves = moves.split('.')     #Macht eine neue Liste, wo nach jedem Punkt ein neues Element beginnt
    out = []
    for m in individual_moves:
        for p in m.split(' '):
            if '-' in p or 'x' in p:        #For-Schleife ermöglicht, dass in einer neuen Liste alle Elemente mit
                out.append(p)               #einem Bindestrich oder x in die Liste out getan werden.
    game_result = out.pop()                 #Das Resultat ist das letzte Element und wird rausgenommen und gespeichert
    return game_result, out


def parse_games(games_str):
  games = games_str.strip().split('[Event')         #Liste wird gemacht wo jede Zeile ein Spiel ist
  results, moves = [], []
  for g in games:                                   #For-Schleife macht das leere Zeilen übersprungen werden
    if not g:
      continue
    r, m = parse_game(g)                            #Funktion von oben wird für jedes individuelle Spiel ausgeführt
    results.append(r)
    moves.append(m)                                 #Resultate und Spielzüge werden in separaten Listen gespeichert
  return results, moves


# Hauptprogramm ab hier
# Datensortierung
#

with open('Data/OCA_2.0.pdn', 'r') as text_file:        # Daten werden als Textfile geöffnet
    games_str = text_file.read()

results, moves = parse_games(games_str)                 # Liste mit Resultaten und Spielen mit Spielzügen aller Spiele
print('Total number of games:', len(moves))
print(results[0])
print(moves[0][2])
print(moves[10][:10])

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
