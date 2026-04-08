import json
import random

RUOTE = ["Bari","Cagliari","Firenze","Genova","Milano","Napoli","Palermo","Roma","Torino","Venezia","Nazionale"]

# ===== CARICA DATI =====
with open("estrazioni.json", encoding="utf-8") as f:
    estrazioni = json.load(f)

risultati = {
    "top": [],
    "ruote": {},
    "giocate": [],
    "jolly": {}
}

# ===== FREQUENZE =====
def calcola_freq(lista):
    freq = {}
    for estr in lista:
        for n in estr:
            freq[n] = freq.get(n, 0) + 1
    return freq

# ===== ANALISI RUOTE =====
for ruota in RUOTE:

    if ruota not in estrazioni:
        continue

    estrazioni_ruota = estrazioni[ruota]

    if len(estrazioni_ruota) < 20:
        continue

    ultime = estrazioni_ruota[-1]

    breve = estrazioni_ruota[-20:]
    medio = estrazioni_ruota[-100:]
    lungo = estrazioni_ruota[-500:]

    freq_breve = calcola_freq(breve)
    freq_medio = calcola_freq(medio)
    freq_lungo = calcola_freq(lungo)

    # ===== RITARDI =====
    ritardi = {}
    for n in range(1, 91):
        ritardo = 0
        for estr in reversed(estrazioni_ruota):
            if n in estr:
                break
            ritardo += 1
        ritardi[n] = ritardo

    score_num = {}
    ultime_5 = estrazioni_ruota[-5:]

    for n in range(1, 91):

        penalita = 10 if n in ultime else 0
        presenze_recenti = sum(1 for estr in ultime_5 if n in estr)
        bonus_vicini = 1 if (n-1 in ultime or n+1 in ultime) else 0

        score = (
            freq_breve.get(n, 0) * 3 +
            freq_medio.get(n, 0) * 1.5 +
            freq_lungo.get(n, 0) * 1 +
            (ritardi[n] ** 1.2) * 0.5 +
            presenze_recenti * 2 +
            bonus_vicini -
            penalita
        )

        if ritardi[n] > 20:
            score += ritardi[n] * 0.3

        if freq_breve.get(n, 0) > 2 and freq_lungo.get(n, 0) > 15:
            score += 5

        score += random.uniform(0, 0.5)

        score_num[n] = score

    # ===== SCELTA AMBO =====
    candidati = [n for n in range(1, 91) if n not in ultime]
    candidati.sort(key=lambda x: score_num[x], reverse=True)

    ambo = [candidati[0], candidati[1]]
    score_ambo = score_num[ambo[0]] + score_num[ambo[1]]

    risultati["ruote"][ruota] = {
        "ultima": ultime,
        "ambo": ambo,
        "score": score_ambo
    }

# ===== TOP 3 =====
top_sorted = sorted(
    risultati["ruote"].items(),
    key=lambda x: x[1]["score"],
    reverse=True
)

top3 = top_sorted[:3]

risultati["top"] = [t[0] for t in top3]

giocate = []
for ruota, dati in top3:
    giocate.append({
        "ruota": ruota,
        "ambo": dati["ambo"]
    })

risultati["giocate"] = giocate

# ===== JOLLY INTELLIGENTE =====

gemelle = {
    "Bari": "Napoli",
    "Napoli": "Bari",
    "Milano": "Torino",
    "Torino": "Milano",
    "Palermo": "Cagliari",
    "Cagliari": "Palermo",
    "Firenze": "Genova",
    "Genova": "Firenze"
}

# 1. miglior ambo globale
miglior_ambo = None
miglior_score = 0
ruota_origine = None

for ruota, dati in risultati["ruote"].items():
    if dati["score"] > miglior_score:
        miglior_score = dati["score"]
        miglior_ambo = dati["ambo"]
        ruota_origine = ruota

ruote_top = [g["ruota"] for g in risultati["giocate"]]

# ===== TEST NAZIONALE =====
usa_nazionale = False

if "Nazionale" in estrazioni:

    ultime_20_naz = estrazioni["Nazionale"][-20:]
    presenza = 0

    for estr in ultime_20_naz:
        for n in miglior_ambo:
            if n in estr:
                presenza += 1

    if presenza >= 1:
        usa_nazionale = True

# ===== SCELTA RUOTA JOLLY =====

if usa_nazionale and "Nazionale" not in ruote_top:
    ruota_jolly = "Nazionale"

else:
    ruota_jolly = gemelle.get(ruota_origine)

    if ruota_jolly not in risultati["ruote"] or ruota_jolly in ruote_top:
        candidati = [
            r for r in risultati["ruote"]
            if r != ruota_origine and r not in ruote_top
        ]

        if candidati:
            ruota_jolly = max(candidati, key=lambda r: risultati["ruote"][r]["score"])
        else:
            ruota_jolly = ruota_origine

# ===== ASSEGNA JOLLY =====
risultati["jolly"] = {
    "ruota": ruota_jolly,
    "ambo": miglior_ambo
}

# ===== SALVA =====
with open("risultati.json", "w", encoding="utf-8") as f:
    json.dump(risultati, f, indent=2)

print("🔥 PRO MAX ATTIVO (TOP + JOLLY SMART + NAZIONALE INTELLIGENTE)")