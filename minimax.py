
from checkerboard.constants import RED, WHITE
import random
import state

INF=1e6
DEPTH=1   # will have DEPTH+1 levels. (has to be odd).

# def utility(board):
#   if state.count_red(board) == 0:
#     return INF
#   return state.evaluate(board, WHITE)

# simple utility from white's perspective.
# large positive numbers mean they are better for white.
def utility(board):
  if state.count_red(board) == 0:
    return INF
  rc = state.count_red(board)
  wc = state.count_white(board)
  return (100 / (rc + 1)) + (-90 / (wc + 1))


def end_game(board, turn):
  for m in state.get_moves(board, turn):
    return False
  return True


def successors(board, turn):
  original_board = board.copy()
  valid_moves = state.get_moves(board, turn)
  for m in valid_moves:
   board = original_board.copy()
   yield m, state.move(board, m)


def max_strength(board, alpha, beta, depth):
  turn = WHITE
  if depth == 0 or end_game(board, turn):
    u = utility(board)
    state.print_board(board)
    print('Candidate MAX utility: ', u)
    return u, None, None
  _s, _move, _board = -INF, None, None
  for m, mboard in successors(board, turn):
    tmp_s, _, _ = min_strength(mboard, alpha, beta, depth-1)
    if tmp_s > _s:
      _s, _move, _board = tmp_s, m, mboard
    alpha = max(alpha, _s)
    #print(f'alpha = {alpha} {_s} {depth}')
    if _s >= beta:
      print(f'out in max function beta test: {_s} >= {beta}')
      break
  assert _move is not None
  return _s, _move, _board


def min_strength(board, alpha, beta, depth):
  turn = RED
  if depth == 0 or end_game(board, turn):
    u = utility(board)
    state.print_board(board)
    print('Candidate MIN utility:', u)
    return u, None, None
  _s, _move, _board = INF, None, None
  for m, mboard in successors(board, turn):
    tmp_s, _, _ = max_strength(mboard, alpha, beta, depth-1)
    if tmp_s < _s:
      _s, _move, _board = tmp_s, m, mboard
    beta = min(beta, _s)
    #print(f'beta = {beta} {_s} {depth}')
    if _s <= alpha:
      print(f'out in min function alpha test: {_s} <= {alpha}')
      break
  assert _move is not None
  return _s, _move, _board


def get_best_move(game, depth=DEPTH):
  """MinMax function."""
  board = state.extract_board(game)
  _strength, _move, _board = max_strength(board, -INF, INF, depth)
  return _strength, _move, _board
