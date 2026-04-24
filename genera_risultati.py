import json

RUOTE = ["Bari","Cagliari","Firenze","Genova","Milano","Napoli","Palermo","Roma","Torino","Venezia"]

# ===== CARICA DATI =====
with open("estrazioni.json", encoding="utf-8") as f:
    estrazioni = json.load(f)

risultati = {
    "top": [],
    "ruote": {}
}

# ===== CICLO RUOTE =====
for ruota in RUOTE:

    if ruota not in estrazioni:
        continue

    estrazioni_ruota = estrazioni[ruota]

    if not isinstance(estrazioni_ruota, list) or len(estrazioni_ruota) == 0:
        continue

    # ultime estrazioni
    ultime = estrazioni_ruota[-1]
    storico = estrazioni_ruota[-500:]  # ultime 500

    # ===== FREQUENZE =====
    freq = {}
    for estr in storico:
        for n in estr:
            freq[n] = freq.get(n, 0) + 1

    # ===== RITARDI =====
    ritardi = {}
    for n in range(1, 91):
        ritardo = 0
        for estr in reversed(estrazioni_ruota):
            if n in estr:
                break
            ritardo += 1
        ritardi[n] = ritardo

    # ===== SCORE =====
    score_num = {}
    for n in range(1, 91):
        score_num[n] = freq.get(n, 0) + (ritardi[n] / 2)

    # ===== FILTRO =====
    candidati = [n for n in range(1, 91) if n not in ultime]

    candidati.sort(key=lambda x: score_num[x], reverse=True)

    if len(candidati) >= 2:
        ambo = [candidati[0], candidati[1]]
        score = round(score_num[ambo[0]] + score_num[ambo[1]])
    else:
        ambo = []
        score = 0

    risultati["ruote"][ruota] = {
        "ultima": ultime,
        "ambo": ambo,
        "score": score
    }

# ===== TOP 5 =====
top_sorted = sorted(
    risultati["ruote"].items(),
    key=lambda x: x[1]["score"],
    reverse=True
)

risultati["top"] = [t[0] for t in top_sorted[:5]]

# ===== SALVA =====
with open("risultati.json", "w", encoding="utf-8") as f:
    json.dump(risultati, f, indent=2)

print("✅ RISULTATI GENERATI")
