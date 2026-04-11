import json
from collections import Counter

RUOTE = ["Bari","Cagliari","Firenze","Genova","Milano",
         "Napoli","Palermo","Roma","Torino","Venezia"]

with open("estrazioni.json", encoding="utf-8") as f:
    data = json.load(f)

output = {
    "top": [],
    "ruota": {},
    "jolly": {}
}

# ===== CALCOLO PER RUOTA =====
for ruota in RUOTE:
    estrazioni = data[ruota][-50:]  # ultime 50 estrazioni

    freq = Counter()
    for estr in estrazioni:
        freq.update(estr)

    # numeri meno usciti = più "in ritardo soft"
    numeri = sorted(freq, key=freq.get)[:5]

    if len(numeri) >= 2:
        ambo = [numeri[0], numeri[1]]
    else:
        continue

    output["ruota"][ruota] = ambo

# ===== TOP (migliori 3) =====
sorted_ruote = list(output["ruota"].items())[:3]

for r, ambo in sorted_ruote:
    output["top"].append({
        "ruota": r,
        "ambo": ambo
    })

# ===== JOLLY =====
if output["top"]:
    output["jolly"] = {
        "ruota": output["top"][0]["ruota"],
        "ambo": output["top"][0]["ambo"]
    }

# ===== SALVA =====
with open("risultati.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print("✅ Motore 3 OK")