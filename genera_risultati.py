import json
import random
from collections import defaultdict

# ===== CONFIG =====
NUM_ESTRAZIONI = 80

RUOTE_GEMELLE = {
    "Bari": "Napoli",
    "Napoli": "Bari",
    "Cagliari": "Roma",
    "Roma": "Cagliari",
    "Firenze": "Genova",
    "Genova": "Firenze",
    "Milano": "Torino",
    "Torino": "Milano",
    "Palermo": "Venezia",
    "Venezia": "Palermo"
}

# ===== CARICA ESTRAZIONI =====
with open("estrazioni.json", "r") as f:
    estrazioni = json.load(f)

risultati = {"ruote": {}}

# ===== CALCOLO AMBI =====
for ruota, estrazioni_ruota in estrazioni.items():
    ultime = estrazioni_ruota[-NUM_ESTRAZIONI:]

    frequenze = defaultdict(int)

    for estr in ultime:
        for n in estr:
            frequenze[n] += 1

    ordinati = sorted(frequenze.items(), key=lambda x: x[1], reverse=True)

    top_numeri = [n for n, _ in ordinati[:12]]

    migliori_ambi = []
    for i in range(len(top_numeri)):
        for j in range(i+1, len(top_numeri)):
            n1 = top_numeri[i]
            n2 = top_numeri[j]

            score = frequenze[n1] + frequenze[n2]

            migliori_ambi.append(((n1, n2), score))

    migliori_ambi.sort(key=lambda x: x[1], reverse=True)

    ambo = list(migliori_ambi[0][0])
    score_finale = round(migliori_ambi[0][1] * 1.7, 2)

    risultati["ruote"][ruota] = {
        "ambo": ambo,
        "score": score_finale
    }

# ===== TOP =====
top = sorted(
    [(r, risultati["ruote"][r]["score"]) for r in risultati["ruote"]],
    key=lambda x: x[1],
    reverse=True
)[:3]

risultati["top"] = [r[0] for r in top]

# ===== JOLLY PRO =====
jolly_ruota = random.choice(risultati["top"])
ambo_top = risultati["ruote"][jolly_ruota]["ambo"]

usa_gemella = random.random() < 0.3

if usa_gemella:
    # ===== RUOTA GEMELLA =====
    gemella = RUOTE_GEMELLE.get(jolly_ruota, jolly_ruota)

    storico = estrazioni[gemella][-60:]
    frequenze = defaultdict(int)

    for estr in storico:
        for n in estr:
            frequenze[n] += 1

    ordinati = sorted(frequenze.items(), key=lambda x: x[1], reverse=True)
    candidati = [n for n,_ in ordinati]

    jolly_ambo = random.sample(candidati[:12], 2)

    risultati["jolly"] = {
        "ruota": gemella + " (gemella)",
        "ambo": jolly_ambo
    }

else:
    # ===== STESSA RUOTA MA DIVERSO =====
    storico = estrazioni[jolly_ruota][-60:]
    frequenze = defaultdict(int)

    for estr in storico:
        for n in estr:
            frequenze[n] += 1

    ordinati = sorted(frequenze.items(), key=lambda x: x[1], reverse=True)

    candidati = [n for n,_ in ordinati if n not in ambo_top]

    if len(candidati) >= 2:
        jolly_ambo = random.sample(candidati[:12], 2)
    else:
        jolly_ambo = random.sample(range(1,91), 2)

    risultati["jolly"] = {
        "ruota": jolly_ruota,
        "ambo": jolly_ambo
    }

# ===== SALVA JSON =====
with open("risultati.json", "w") as f:
    json.dump(risultati, f, indent=2)

print("✅ Risultati generati correttamente")