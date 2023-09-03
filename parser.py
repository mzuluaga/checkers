
def parse_game(game):
  parts = game.split('"]')
  moves = parts[-1]
  moves = moves.replace('\n',' ')
  individual_moves = moves.split('.')
  out = []
  for m in individual_moves:
    for p in m.split(' '):
      if '-' in p or 'x' in p:
        out.append(p)
  game_result = out.pop()
  return game_result, out


def parse_games(games_str):
  games = games_str.strip().split('[Event')
  results, moves = [], []
  for g in games:
    if not g:
      continue
    r, m = parse_game(g)
    results.append(r)
    moves.append(m)
  return results, moves


with open('OCA_2.0.pdn', 'r') as text_file:
  games_str = text_file.read()

#print(games_str)

results, moves = parse_games(games_str)
print(results[:3])
print(moves[0][:10])
print(moves[1][:10])
print(moves[2][:10])
