import json
from collections import defaultdict

RUOTE = ["Bari","Cagliari","Firenze","Genova","Milano",
         "Napoli","Palermo","Roma","Torino","Venezia"]

with open("estrazioni.json", encoding="utf-8") as f:
    estrazioni = json.load(f)

risultati = {"ruote":{}, "top":[], "jolly":{}}

global_usati = set()

for ruota in RUOTE:

    storico = estrazioni[ruota][-50:]

    ritardi = {}
    frequenze = defaultdict(int)

    # frequenze
    for estr in storico:
        for n in estr:
            frequenze[n] += 1

    # ritardi
    for n in range(1,91):
        ritardo = 0
        for estr in reversed(storico):
            if n in estr:
                break
            ritardo += 1
        ritardi[n] = ritardo

    # score
    score_numeri = {}
    for n in range(1,91):
        score_numeri[n] = ritardi[n]*3 + frequenze[n]

    ordinati = sorted