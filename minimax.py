
from checkerboard.constants import RED, WHITE
import random
import state

INF=1e6
DEPTH=5   # will have DEPTH+1 levels. (has to be odd).

# # simpler utility heuristic for testing.
# # large positive numbers mean they are better for white.
# def utility(board):
#   if state.count_red(board) == 0:
#     return INF
#   if state.count_white(board) == 0:
#     return -INF
#   rc = state.count_red(board)
#   wc = state.count_white(board)
#   return (100 / (rc + 1)) + (-90 / (wc + 1))


def utility(board):
  if state.count_red(board) == 0:
    return INF
  if state.count_white(board) == 0:
    return -INF
  # TODO: return utility when no moves posible.
  return state.evaluate(board, WHITE)


def successors(board, turn):
  original_board = board.copy()
  valid_moves = state.get_moves(board, turn)
  for m in valid_moves:
   yield m, state.move(original_board.copy(), m)


def max_strength(board, alpha, beta, depth):
  turn = WHITE
  if depth == 0:
    return utility(board), None, None
  _strength, _move, _board = -INF, None, None
  for m, mboard in successors(board, turn):
    _strength_tmp, _, _ = min_strength(mboard, alpha, beta, depth-1)
    if _strength_tmp > _strength:  # update max_strength
      _strength, _move, _board = _strength_tmp, m, mboard
    alpha = max(alpha, _strength)
    #print(f'alpha = {alpha} {_strength} {depth}')
    if _strength >= beta:
      #print(f'depth={depth} out in max function beta test: {_strength} >= {beta}')
      break
  return _strength, _move, _board


def min_strength(board, alpha, beta, depth):
  turn = RED
  if depth == 0:
    return utility(board), None, None
  _strength, _move, _board = INF, None, None
  for m, mboard in successors(board, turn):
    _strength_tmp, _, _ = max_strength(mboard, alpha, beta, depth-1)
    if _strength_tmp < _strength: # update min_strength
      _strength, _move, _board = _strength_tmp, m, mboard
    beta = min(beta, _strength)
    #print(f'beta = {beta} {_strength} {depth}')
    if _strength <= alpha:
      #print(f'depth={depth} out in min function alpha test: {_strength} <= {alpha}')
      break
  return _strength, _move, _board


def minimax(game, depth=DEPTH):
  """MinMax function."""
  board = state.extract_board(game)
  state.print_board(board, f'Minimax original board. depth={depth}')
  _strength, _move, _board = max_strength(board, -INF, INF, depth)
  return _strength, _move, _board
