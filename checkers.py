#Checkersprogramm, dass mit einem Minimax-algorithmus programmiert ist

import time

import numpy as np
import pandas as pd
import random

import minimax
import parser

results, moves = parser.run()

FPS = 60

board = minimax.new_board()


def run():
    while True:
      move = minimax.get_best_move(board)
      if not move:
        break
      (pr, pc), (row, col) = move
      print(f'Minmax Selected: (pr, pc, row, col) = ({pr}, {pc}, {row}, {col})')
      time.sleep(1.0)



def main():
  run()

main()
