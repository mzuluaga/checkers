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

  # def test_successors_for_red(self):
  #   board = np.zeros((8,8), np.int8)
  #   board[4] = [0, 0, 0, WK, 0, 0, 0, 0]
  #   board[5] = [0, 0, 0, 0,  R, 0, 0, 0]
  #   print('original board (RED/BLACK plays):')
  #   state.print_board(board)
  #   successors = list(minimax.successors(board, RED))
  #   for m, mboard in successors:
  #     state.print_board(mboard)
  #     print(f'Utility from WHITE perspective: {minimax.utility(mboard)}')
  #   self.assertEqual(len(successors), 2)
  #   self.assertEqual(successors[0][1].sum(), 1)
  #   self.assertEqual(successors[1][1].sum(), 5)

  # def test_successors_for_white(self):
  #   board = np.zeros((8,8), np.int8)
  #   board[4] = [0, 0, 0, W, 0, 0, 0, 0]
  #   board[5] = [0, 0, 0, 0,  RK, 0, 0, 0]
  #   print('original board (WHITE plays):')
  #   state.print_board(board)
  #   successors = list(minimax.successors(board, WHITE))
  #   for m, mboard in successors:
  #     state.print_board(mboard)
  #     print(f'Utility from WHITE perspective: {minimax.utility(mboard)}')
  #   self.assertEqual(len(successors), 2)
  #   self.assertEqual(successors[0][1].sum(), 5)
  #   self.assertEqual(successors[1][1].sum(), 2)

  def test_successors_for_white(self):
    board = np.zeros((8,8), np.int8)
    board[0] = [0, W, 0, 0, 0, 0, 0, 0]
    board[1] = [0, 0, R, 0, 0, 0, 0, 0]
    print('original board (WHITE plays):')
    state.print_board(board)
    successors = list(minimax.successors(board, WHITE))
    for m, mboard in successors:
      state.print_board(mboard)
      print(f'Utility from WHITE perspective {m}: {minimax.utility(mboard)}')
    self.assertEqual(len(successors), 2)
    self.assertEqual(successors[0][1].sum(), 5)
    self.assertEqual(successors[1][1].sum(), 2)


if __name__ == '__main__':
    unittest.main()
