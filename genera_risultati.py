import json
from collections import defaultdict

RUOTE = ["Bari","Cagliari","Firenze","Genova","Milano",
         "Napoli","Palermo","Roma","Torino","Venezia"]

# ===== CARICA STORICO =====
with open("estrazioni.json", encoding="utf-8") as f:
    estrazioni = json.load(f)

risultati = {"ruote":{}, "top":[], "jolly":{}}

global_usati = set()

# ===== ANALISI =====
for ruota in RUOTE:

    storico = estrazioni[ruota][-50:]  # ultime 50

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
        score = ritardi[n]*2 + frequenze[n]
        score_numeri[n] = score

    # ordina numeri
    ordinati = sorted(score_numeri.items(), key=lambda x: x[1], reverse=True)

    # evita numeri ultima estrazione
    ultima = estrazioni[ruota][-1]

    candidati = [n for n,s in ordinati if n not in ultima]

    # crea ambi
    best_ambo = None
    best_score = -1

    for i in range(10):
        for j in range(i+1,10):
            n1 = candidati[i]
            n2 = candidati[j]

            # evita duplicati globali nei TOP
            if n1 in global_usati or n2 in global_usati:
                continue

            score = score_numeri[n1] + score_numeri[n2]

            if score > best_score:
                best_score = score
                best_ambo = [n1,n2]

    risultati["ruote"][ruota] = {
        "ambo": best_ambo,
        "score": best_score
    }

# ===== CREA TOP =====
top = sorted(risultati["ruote"].items(),
             key=lambda x: x[1]["score"],
             reverse=True)[:3]

for nome, dati in top:
    risultati["top"].append({
        "ruota": nome,
        "ambo": dati["ambo"]
    })

    global_usati.update(dati["ambo"])

# ===== JOLLY =====
jolly_ruota = top[0][0]
risultati["jolly"] = {
    "ruota": jolly_ruota,
    "ambo": risultati["ruote"][jolly_ruota]["ambo"]
}

# ===== SALVA =====
with open("risultati.json","w",encoding="utf-8") as f:
    json.dump(risultati,f,indent=2)

print("✅ MOTORE 3 PRO GENERATO")