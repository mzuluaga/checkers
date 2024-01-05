
from checkerboard.constants import RED, WHITE
import random
import state

INF=1e6
DEPTH=3   # will have DEPTH+1 levels. (has to be odd).

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
  for m in state.get_moves(board.copy(), turn):
    return False
  return True


def successors(board, turn):
  original_board = board.copy()
  #state.print_board(original_board, 'succ original board:')
  valid_moves = state.get_moves(board, turn)
  #state.print_board(original_board, 'succ after get valid_moves')
  for m in valid_moves:
   mboard = state.move(original_board.copy(), m)
   #state.print_board(mboard, f'succ move: {m}')
   yield m, mboard


def max_strength(board, alpha, beta, depth):
  turn = WHITE
  #state.print_board(board, f'max original board depth={depth}')
  if depth == 0 or end_game(board, turn):
    u = utility(board)
    return u, None, None
  _s, _move, _board = -INF, None, None
  for m, mboard in successors(board, turn):
    #state.print_board(board, f'max move orginal board')
    #state.print_board(mboard, f'max move: {m}')
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
  #state.print_board(board, f'min original board depth={depth}')
  if depth == 0 or end_game(board, turn):
    u = utility(board)
    #state.print_board(board)
    #state.print_board(board, f'Candidate MIN utility: {u}')
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
  #state.print_board(board, 'get best move board')
  _strength, _move, _board = max_strength(board, -INF, INF, depth)
  return _strength, _move, _board
