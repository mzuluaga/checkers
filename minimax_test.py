import unittest
import numpy as np

import state
import minimax
from checkerboard.constants import RED, WHITE

R = state.R
RK = state.RK
W = state.W
WK = state.WK

class MinimaxTest(unittest.TestCase):

  #   Board:
  #   0 1 2 3 4 5 6 7
  # 0 □ □ □ □ □ □ □ □
  # 1 □ □ □ □ □ □ □ □
  # 2 □ □ □ □ □ □ □ □
  # 3 □ □ □ □ □ □ □ □
  # 4 □ □ □ ♛ □ □ □ □
  # 5 □ □ □ □ ♙ □ □ □
  # 6 □ □ □ □ □ □ □ □
  # 7 □ □ □ □ □ □ □ □
  #
  # candidate 0 ((5, 4), (3, 2))
  #
  # Board:
  #   0 1 2 3 4 5 6 7
  # 0 □ □ □ □ □ □ □ □
  # 1 □ □ □ □ □ □ □ □
  # 2 □ □ □ □ □ □ □ □
  # 3 □ □ ♙ □ □ □ □ □
  # 4 □ □ □ □ □ □ □ □
  # 5 □ □ □ □ □ □ □ □
  # 6 □ □ □ □ □ □ □ □
  # 7 □ □ □ □ □ □ □ □
  #
  # candidate 1 ((5, 4), (4, 5))
  #
  # Board:
  #   0 1 2 3 4 5 6 7
  # 0 □ □ □ □ □ □ □ □
  # 1 □ □ □ □ □ □ □ □
  # 2 □ □ □ □ □ □ □ □
  # 3 □ □ □ □ □ □ □ □
  # 4 □ □ □ ♛ □ ♙ □ □
  # 5 □ □ □ □ □ □ □ □
  # 6 □ □ □ □ □ □ □ □
  # 7 □ □ □ □ □ □ □ □
  # def test_successors_for_red(self):
  #   board = np.zeros((8,8), np.int8)
  #   board[4] = [0, 0, 0, WK, 0, 0, 0, 0]
  #   board[5] = [0, 0, 0, 0,  R, 0, 0, 0]
  #   print('original board')
  #   state.print_board(board)
  #   successors = list(minimax.successors(board, RED))
  #   self.assertEqual(len(successors), 2)
  #   self.assertEqual(successors[0][1].sum(), 1)
  #   self.assertEqual(successors[1][1].sum(), 5)

  def test_successors_for_white(self):
    board = np.zeros((8,8), np.int8)
    board[4] = [0, 0, 0, W, 0, 0, 0, 0]
    board[5] = [0, 0, 0, 0,  RK, 0, 0, 0]
    print('original board')
    state.print_board(board)
    successors = list(minimax.successors(board, WHITE))
    for m, mboard in successors:
      state.print_board(mboard)
    self.assertEqual(len(successors), 2)
    # self.assertEqual(successors[0][1].sum(), 1)
    # self.assertEqual(successors[1][1].sum(), 5)

if __name__ == '__main__':
    unittest.main()
