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

    # score migliorato
    score_numeri = {}
    for n in range(1,91):
        score_numeri[n] = ritardi[n]*3 + frequenze[n]

    ordinati = sorted(score_numeri.items(), key=lambda x: x[1], reverse=True)

    ultima = estrazioni[ruota][-1]

    candidati = [n for n,s in ordinati if n not in ultima]

    best_ambo = None
    best_score = -1

    # prova combinazioni TOP 12 numeri
    for i in range(12):
        for j in range(i+1,12):

            n1 = candidati[i]
            n2 = candidati[j]

            # ❌ evita numeri troppo vicini
            if abs(n1 - n2) <= 2:
                continue

            # ❌ evita duplicati globali
            if n1 in global_usati or n2 in global_usati:
                continue

            score = score_numeri[n1] + score_n