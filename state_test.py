import unittest
import state

class StateTest(unittest.TestCase):

  def test_pieve_corner_moves_no_jumps(self):
    # 0,0
    board = state.empty_board()
    board[0, 0] = state.W
    state.print_board(board)
    moves = state.get_piece_moves(board, 0, 0)
    self.assertEqual(moves[0][1], (1, 1))
    # 0,7
    board = state.empty_board()
    board[0, 7] = state.W
    state.print_board(board)
    moves = state.get_piece_moves(board, 0, 7)
    self.assertEqual(moves[0][1], (1, 6))
    # 7,0
    board = state.empty_board()
    board[7, 0] = state.R
    state.print_board(board)
    moves = state.get_piece_moves(board, 7, 0)
    self.assertEqual(moves[0][1], (6, 1))
    # 7,7
    board = state.empty_board()
    board[7, 7] = state.R
    state.print_board(board)
    moves = state.get_piece_moves(board, 7, 7)
    self.assertEqual(moves[0][1], (6, 6))


  # def test_moves_without_jump(self):
  #   board = state.new_board()
  #   state.print_board(board)
  #   m = ((5, 2), (4, 3))
  #   board = state.move(board, m)
  #   self.assertEqual(board[5,2], 0)
  #   self.assertEqual(board[4,3], state.R)

  # def test_moves_white_jumps_over_red(self):
  #   board = state.empty_board()
  #   board[3, 4] = state.W
  #   board[4, 3] = state.R
  #   m = ((3, 4), (5, 2))
  #   # state.print_board(board)
  #   board = state.move(board, m)
  #   # state.print_board(board)
  #   self.assertEqual(board.sum(), 2)

  # def test_moves_red_jumps_over_white(self):
  #   board = state.empty_board()
  #   board[3, 4] = state.W
  #   board[4, 3] = state.R
  #   m = ((4, 3), (2, 5))
  #   #state.print_board(board)
  #   board = state.move(board, m)
  #   #state.print_board(board)
  #   self.assertEqual(board.sum(), 1)

  # def test_moves_white_jumps_over_red_queen(self):
  #   board = state.empty_board()
  #   board[1, 0] = state.W
  #   board[2, 1] = state.RK
  #   #state.print_board(board)
  #   m = ((1, 0), (3, 2))
  #   board = state.move(board, m)
  #   #state.print_board(board)
  #   self.assertEqual(board.sum(), 2)

  # def test_captures_and_promotes_to_red_queen(self):
  #   board = state.empty_board()
  #   board[1, 2] = state.W
  #   board[2, 1] = state.R
  #   #state.print_board(board)
  #   m = ((2, 1), (0, 3))
  #   board = state.move(board, m)
  #   #state.print_board(board)
  #   self.assertEqual(board.sum(), 3)

if __name__ == '__main__':
    unittest.main()
