import json
import random
from collections import defaultdict

RUOTE = ["Bari","Cagliari","Firenze","Genova","Milano",
         "Napoli","Palermo","Roma","Torino","Venezia"]

with open("estrazioni.json", encoding="utf-8") as f:
    estrazioni = json.load(f)

risultati = {"ruote":{}, "top":[], "jolly":{}}

global_usati = set()

for ruota in RUOTE:

    storico = estrazioni[ruota][-60:]

    ritardi = {}
    frequenze = defaultdict(int)
    range_medio = {}

    # ===== FREQUENZE =====
    for estr in storico:
        for n in estr:
            frequenze[n] += 1

    # ===== RANGE MEDIO =====
    for n in range(1,91):
        pos = []
        for i,estr in enumerate(storico):
            if n in estr:
                pos.append(i)

        if len(pos) >= 2:
            distanze = [pos[i] - pos[i-1] for i in range(1,len(pos))]
            range_medio[n] = sum(distanze)/len(distanze)
        else:
            range_medio[n] = 10

    # ===== RITARDO =====
    for n in range(1,91):
        rit = 0
        for estr in reversed(storico):
            if n in estr:
                break
            rit += 1
        ritardi[n] = rit

    # ===== SCORE =====
    score_numeri = {}
    for n in range(1,91):

        range_score = 0
        if ritardi[n] >= range_medio[n]:
            range_score = 20

        score_numeri[n] = (
            ritardi[n]*2 +
            frequenze[n]*1.5 +
            range_score
        )

    # ===== BONUS AMBO =====
    def bonus_ambo(n1, n2):
        diff = abs(n1 - n2)

        if diff <= 2:
            return -10
        if 5 <= diff <= 30:
            return 10
        if diff > 60:
            return -5

        return 0

    ordinati = sorted(score_numeri.items(), key=lambda x: x[1], reverse=True)

    ultima = estrazioni[ruota][-1]
    ultime_due = estrazioni[ruota][-2:]
    numeri_recenti = set(n for estr in ultime_due for n in estr)

    # ===== POOL DINAMICO =====
    top_pool = ordinati[:40]
    random.shuffle(top_pool)

    candidati = []
    for n,score in top_pool:
        if n not in ultima and n not in numeri_recenti and score > 10:
            candidati.append(n)

    if len(candidati) < 10:
        candidati = [n for n,s in ordinati[:50] if n not in ultima]

    best_ambo = None
    best_score = -1

    # ===== SCELTA AMBO =====
    for _ in range(80):

        n1, n2 = random.sample(candidati, 2)

        if abs(n1 - n2) <= 2:
            continue

        if n1 in global_usati or n2 in global_usati:
            if random.random() < 0.7:
                continue

        score = (
            score_numeri[n1] +
            score_numeri[n2] +
            bonus_ambo(n1, n2)
        )

        if score > best_score:
            best_score = score
            best_ambo = [n1,n2]

    risultati["ruote"][ruota] = {
        "ambo": best_ambo,
        "score": best_score
    }

# ===== TOP =====
top = sorted(risultati["ruote"].items(),
             key=lambda x: x[1]["score"],
             reverse=True)[:3]

for nome, dati in top:
    risultati["top"].append({
        "ruota": nome,
        "ambo": dati["ambo"]
    })
    global_usati.update(dati["ambo"])

# ===== JOLLY INTELLIGENTE =====
jolly_ruota = random.choice(top)[0]

numeri_base = risultati["ruote"][jolly_ruota]["ambo"]

# prendi un numero alternativo forte
storico = estrazioni[jolly_ruota][-60:]
frequenze = defaultdict(int)

for estr in storico:
    for n in estr:
        frequenze[n] += 1

ordinati = sorted(frequenze.items(), key=lambda x: x[1], reverse=True)

extra = None
for n,_ in ordinati:
    if n not in numeri_base:
        extra = n
        break

jolly_ambo = [numeri_base[0], extra]

risultati["jolly"] = {
    "ruota": jolly_ruota,
    "ambo": jolly_ambo
}

# ===== SALVA =====
with open("risultati.json","w",encoding="utf-8") as f:
    json.dump(risultati,f,indent=2)

print("🔥 MOTORE 3 PRO DEFINITIVO ATTIVO")