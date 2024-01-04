
from checkerboard.constants import RED, WHITE
import state

INF=1e6


def end_game(board, turn):
  for m in state.get_valid_moves(board, turn):
    return False
  print(f'EndGame: {turn}')
  # print(board)
  return True


def succesors(board, turn):
  # print(board)
  for m in state.get_valid_moves(board, turn):
    yield m, state.move(board, m)


def max_strength(board, depth):
  # turn = RED
  turn = WHITE
  if depth == 0 or end_game(board, turn):
    return state.evaluate(board, turn), None, None
  _s, _move, _board = -INF, None, None
  for m, new_board in succesors(board, turn):
    tmp_s, _, _ = min_strength(new_board, depth-1)
    if _s < tmp_s:
      _s, _move, _board = tmp_s, m, new_board
  return _s, _move, _board


def min_strength(board, depth):
  # turn = WHITE
  turn = RED
  if depth == 0 or end_game(board, turn):
    return state.evaluate(board, turn), None, None
  _s, _move, _board = INF, None, None
  for m, new_board in succesors(board, turn):
    tmp_s, _, _ = max_strength(new_board, depth-1)
    if _s > tmp_s:
      _s, _move, _board = tmp_s, m, new_board
  return _s, _move, _board


def get_best_move(game):
  """MinMax function."""
  _strength, _move, _board = max_strength(state.extract_board(game), depth=5)
  print(f'Found max-move: {_strength}, {_move} \n {_board}')
  return _strength, _move, _board
