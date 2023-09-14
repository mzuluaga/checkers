#Checkersprogramm, dass mit einem Minimax-algorithmus programmiert ist

import numpy as np
import pandas as pd
import pypdn
import matplotlib.pyplot as plt

# Öffne die Textdatei zum Lesen
with open("Data/practicedata.txt", "r") as file:
    # Lies die Zeilen der Datei
    lines = file.readlines()

# Extrahiere das erste Zeichen jeder Zeile
first_characters = [line[0] for line in lines]
n = len(first_characters)
# Gib die extrahierten ersten Zeichen aus
char = np.zeros(n)
num = 0
for x,i in enumerate(first_characters):
    if i != "[":
        char[x] = 0
        num = num + 1
    else:
        char[x] = 1
print(char)
print(num)

data = pd.read_csv("Data/practicedata.txt", delimiter='\t')
for i in range(212):
    while char[i] == 1:
        data = data[i,j]

#for i in data.iterrows():


