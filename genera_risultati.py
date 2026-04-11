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
    estrazioni = data[ruota][-50:]

    freq = Counter()
    for estr in estrazioni:
        freq.update(estr)

    numeri = sorted(freq, key=freq.get)[:5]

    if len(numeri) >= 2:
        ambo = [numeri[0], numeri[1]]
        output["ruota"][ruota] = ambo

# ===== TOP =====
for r in list(output["ruota"].keys())[:3]:
    output["top"].append({
        "ruota": r,
        "ambo": output["ruota"][r]
    })

# ===== JOLLY =====
if output["top"]:
    output["jolly"] = output["top"][0]

# ===== SALVA =====
with open("risultati.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print("✅ Motore 3 OK")