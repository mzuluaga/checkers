
import state

INF=1e6

def succesors(board, turn):
  for m in state.get_all_valid_moves(board, turn)
    yield m, state.move(board, m)


def max_strength(board):
  turn = WHITE
  if end_game(board):
    return state.evaluate_board(board, turn)
  _s, _move, _board = -INF, None, None
  for m, new_board in succesors(board, turn):
    tmp_s = min_strength(new_board)
    if tmp_s > _s:
      _s, _move, _board = tmp_s, m, new_board
  return _s, _move, _board


def min_strength(board):
  turn = RED
  if end_game(board):
    return state.evaluate_board(board, turn)
  _s, _move, _board = INF, None, None
  for m, new_board in succesors(board, turn):
    tmp_s = max_strength(new_board)
    if tmp_s < _s:
      _s, _move, _board = tmp_s, m, new_board
  return _s, _move, _board


def minimax(board):
  return max_strength(board)
