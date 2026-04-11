import json
from collections import Counter

RUOTE = [
    "Bari","Cagliari","Firenze","Genova","Milano",
    "Napoli","Palermo","Roma","Torino","Venezia"
]

with open("estrazioni.json", encoding="utf-8") as f:
    data = json.load(f)

def ritardi(estrazioni):
    rit = {n: 0 for n in range(1, 91)}
    for estr in reversed(estrazioni):
        for n in range(1, 91):
            if n not in estr:
                rit[n] += 1
            else:
                rit[n] = 0
    return rit

def frequenti(estrazioni):
    numeri = []
    for estr in estrazioni[-20:]:
        numeri.extend(estr)
    return [n for n, _ in Counter(numeri).most_common(10)]

output = {}
top = []

for ruota in RUOTE:
    estr = data.get(ruota, [])

    if len(estr) < 5:
        continue

    r = ritardi(estr)
    f = frequenti(estr)

    R1 = max(r, key=r.get)

    C1 = None
    for n in f:
        if n != R1:
            C1 = n
            break

    if not C1:
        continue

    ambo = sorted([R1, C1])
    score = r[R1]

    output[ruota] = {
        "ambo": ambo,
        "score": score
    }

    top.append({
        "ruota": ruota,
        "ambo": ambo,
        "score": score
    })

top = sorted(top, key=lambda x: x["score"], reverse=True)[:3]

def next_ruota(r):
    i = RUOTE.index(r)
    return RUOTE[(i + 1) % len(RUOTE)]

jolly = {}
if top:
    jolly = {
        "ruota": next_ruota(top[0]["ruota"]),
        "ambo": top[0]["ambo"]
    }

with open("risultati.json", "w", encoding="utf-8") as f:
    json.dump({
        "ruote": output,
        "top": top,
        "jolly": jolly
    }, f, indent=2)

print("OK GENERATO")
