import json
from collections import Counter

RUOTE = ["Bari","Cagliari","Firenze","Genova","Milano",
         "Napoli","Palermo","Roma","Torino","Venezia"]

with open("estrazioni.json", encoding="utf-8") as f:
    data = json.load(f)

output = {
    "ruota": {},
    "top": [],
    "jolly": {}
}

for ruota in RUOTE:
    estrazioni = data[ruota][-80:]

    freq = Counter()
    last_seen = {}

    # ===== ANALISI =====
    for idx, estr in enumerate(estrazioni[::-1]):  # dalla più recente
        for n in estr:
            freq[n] += 1
            if n not in last_seen:
                last_seen[n] = idx

    punteggi = {}

    for n in range(1, 91):
        ritardo = last_seen.get(n, 80)  # se mai uscito
        frequenza = freq.get(n, 0)

        # ===== SCORE INTELLIGENTE =====
        score = (ritardo * 1.5) + (10 - frequenza)

        # filtro anti schifezze
        if frequenza == 0:
            score -= 20  # troppo morto

        punteggi[n] = score

    # prendi migliori
    migliori = sorted(punteggi, key=punteggi.get, reverse=True)[:5]

    if len(migliori) >= 2:
        output["ruota"][ruota] = [migliori[0], migliori[1]]

# ===== TOP =====
top_ruote = list(output["ruota"].items())[:3]

for r, ambo in top_ruote:
    output["top"].append({
        "ruota": r,
        "ambo": ambo
    })

# ===== JOLLY =====
if output["top"]:
    output["jolly"] = output["top"][0]

# ===== SALVA =====
with open("risultati.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print("🔥 Motore 3 PRO pronto")