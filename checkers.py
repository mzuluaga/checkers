#Checkersprogramm, dass mit einem Minimax-algorithmus programmiert ist

import time

import numpy as np
import pandas as pd
import random
import pygame
from checkerboard.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkerboard.board import Board
from checkerboard.game import Game
import minimax
import parser

results, moves = parser.run()


# Flussdiagramm zu Minimax machen!
# Checkerboard

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Macht ein Window, wo wir das Checkerbrett hineinversetzen können
pygame.display.set_caption('Checkers')


def get_row_col_from_mouse(pos):
  x, y = pos
  row = y // SQUARE_SIZE
  col = x // SQUARE_SIZE
  return row, col

def run():
    clock = pygame.time.Clock()
    game = Game(WIN)
    while True:
      clock.tick(FPS)
      (pr, pc), (row, col) = minimax.move(game.board, game.turn, game)
      print(f'Minmax Selected: (pr, pc, row, col) = ({pr}, {pc}, {row}, {col})')
      game.select(pr, pc)
      game.select(row, col)
      time.sleep(1.0)
      game.update()
    pygame.quit()
    print(game.winner())


def run_gui():
  run = True
  clock = pygame.time.Clock()
  game = Game(WIN)
  while run:
    clock.tick(FPS)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
        break
      if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        row, col = get_row_col_from_mouse(pos)
        if game.turn == RED:
          game.select(row, col)
        else:
          (pr, pc), (row, col) = minimax.move(game.board, game.turn, game)
          print(f'Minmax Selected: (pr, pc, row, col) = ({pr}, {pc}, {row}, {col})')
          game.select(pr, pc)
          game.select(row, col)
      game.update()
  pygame.quit()
  print(game.winner())


def main():
  run()
  #run_gui()

main()
