# Sample colab at https://colab.research.google.com/drive/1FJ2rwYxLjdzZyJRGS4CwQPacruhvl5t2#scrollTo=VjV3eRXCDMmo

def parse_game(game):
    parts = game.split('"]')                #Macht eine Liste aus einem Spiel, die bei einem [ abgetrennt werden
    moves = parts[-1]                       #Nimmt den letzten Eintrag mit all den Spielzügen
    moves = moves.replace('\n',' ')         #Zeilenumbruch wird durch Abstand ersetzt
    individual_moves = moves.split('.')     #Macht eine neue Liste, wo nach jedem Punkt ein neues Element beginnt
    out = []
    for m in individual_moves:
        for p in m.split(' '):
            if '-' in p or 'x' in p:        #For-Schleife ermöglicht, dass in einer neuen Liste alle Elemente mit
                out.append(p)               #einem Bindestrich oder x in die Liste out getan werden.
    game_result = out.pop()                 #Das Resultat ist das letzte Element und wird rausgenommen und gespeichert
    return game_result, out


def parse_games(games_str):
  games = games_str.strip().split('[Event')         #Liste wird gemacht wo jede Zeile ein Spiel ist
  results, moves = [], []
  for g in games:                                   #For-Schleife macht das leere Zeilen übersprungen werden
    if not g:
      continue
    r, m = parse_game(g)                            #Funktion von oben wird für jedes individuelle Spiel ausgeführt
    results.append(r)
    moves.append(m)                                 #Resultate und Spielzüge werden in separaten Listen gespeichert
  return results, moves


# Hauptprogramm ab hier
# Datensortierung
#

def run():
  with open('Data/OCA_2.0.pdn', 'r') as text_file:        # Daten werden als Textfile geöffnet
    games_str = text_file.read()

    results, moves = parse_games(games_str)
    print('Total number of games:', len(results), len(moves))
    assert len(results) == len(moves)
    return results, moves
