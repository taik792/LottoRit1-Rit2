import json

RUOTE = ["Bari","Cagliari","Firenze","Genova","Milano",
         "Napoli","Palermo","Roma","Torino","Venezia"]

def calcola_ritardi(estrazioni):
    ritardi = {n: 0 for n in range(1, 91)}

    for estr in reversed(estrazioni):
        usciti = set(estr)
        for n in ritardi:
            if n in usciti:
                ritardi[n] = 0
            else:
                ritardi[n] += 1

    return ritardi

with open("estrazioni.json", encoding="utf-8") as f:
    data = json.load(f)

output = {
    "ruota": {},
    "top": [],
    "jolly": {}
}

for ruota in RUOTE:
    estrazioni = data[ruota][-120:]  # più storico = meglio

    ritardi = calcola_ritardi(estrazioni)

    # top 6 ritardatari
    top = sorted(ritardi, key=ritardi.get, reverse=True)[:6]

    # combinazioni intelligenti
    coppie = [
        (top[0], top[2]),
        (top[1], top[3]),
        (top[0], top[4])
    ]

    # scegli quella con ritardo totale più alto
    best = max(coppie, key=lambda x: ritardi[x[0]] + ritardi[x[1]])

    output["ruota"][ruota] = list(best)

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

print("🔥 Motore 3 migliorato (ritardatari intelligenti)")