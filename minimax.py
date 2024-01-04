
from checkerboard.constants import RED, WHITE
import state

INF=1e6
DEPTH=5   # will have DEPTH+1 levels. (has to be odd).

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
    tmp_s, _, _ = min_strength(new_board, alpha, beta, depth-1)
    if _s < tmp_s:
      _s, _move, _board = tmp_s, m, new_board
    if _s >= beta:
      print(f'out in max function beta test: {_s} >= {beta}')
      break
    alpha = max(alpha, _s)
    #print(f'alpha = {alpha} {_s} {depth}')
  return _s, _move, _board


def min_strength(board, alpha, beta, depth):
  turn = RED
  if depth == 0 or end_game(board, turn):
    return state.evaluate(board, WHITE), None, None
  _s, _move, _board = INF, None, None
  for m, new_board in succesors(board, turn):
    tmp_s, _, _ = max_strength(new_board, alpha, beta, depth-1)
    if _s > tmp_s:
      _s, _move, _board = tmp_s, m, new_board
    if _s <= alpha:
      print(f'out in min function alha test: {_s} <= {alpha}')
      break
    beta = min(beta, _s)
    print(f'beta = {beta} {_s} {depth}')
  return _s, _move, _board


def get_best_move(game, depth=DEPTH):
  """MinMax function."""
  board = state.extract_board(game)
  _strength, _move, _board = max_strength(board, -INF, INF, depth)
  return _strength, _move, _board
