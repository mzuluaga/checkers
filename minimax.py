
from checkerboard.constants import RED, WHITE
import state

INF=1e6
DEPTH=4

def end_game(board, turn):
  for m in state.get_moves(board, turn):
    return False
  return True


def succesors(board, turn):
  valid_moves = state.get_moves(board, turn)
  for m in valid_moves:
    yield m, state.move(board.copy(), m)


def max_strength(board, alpha, beta, depth):
  turn = WHITE
  if depth == 0 or end_game(board, turn):
    return state.evaluate(board, turn), None, None
  _s, _move, _board = -INF, None, None
  for m, new_board in succesors(board, turn):
    tmp_s, _, _ = min_strength(new_board, depth-1)
    if _s < tmp_s:
      _s, _move, _board = tmp_s, m, new_board
  return _s, _move, _board


def min_strength(board, alpha, beta, depth):
  turn = RED
  if depth == 0 or end_game(board, turn):
    return state.evaluate(board, turn), None, None
  _s, _move, _board = INF, None, None
  for m, new_board in succesors(board, turn):
    tmp_s, _, _ = max_strength(new_board, depth-1)
    if _s > tmp_s:
      _s, _move, _board = tmp_s, m, new_board
  return _s, _move, _board


def get_best_move(game, depth=DEPTH):
  """MinMax function."""
  board = state.extract_board(game)
  print('Extracted board:\n', board)
  alpha, beta = -INF, INF
  _strength, _move, _board = max_strength(board, depth)
  return _strength, _move, _board
