import json
from collections import Counter

RUOTE = [
    "Bari","Cagliari","Firenze","Genova","Milano",
    "Napoli","Palermo","Roma","Torino","Venezia"
]

# ===== CARICA ESTRAZIONI =====
with open("estrazioni.json", encoding="utf-8") as f:
    data = json.load(f)

# ===== CALCOLO RITARDI =====
def calcola_ritardi(estrazioni):
    ritardi = {n: 0 for n in range(1, 91)}

    for estr in reversed(estrazioni):
        for n in range(1, 91):
            if n not in estr:
                ritardi[n] += 1
            else:
                ritardi[n] = 0

    return ritardi

# ===== NUMERI FREQUENTI RECENTI =====
def numeri_frequenti(estrazioni, ultimi=20):
    recenti = estrazioni[-ultimi:]
    numeri = []

    for estr in recenti:
        numeri.extend(estr)

    conteggio = Counter(numeri)

    return [n for n, _ in conteggio.most_common(15)]

# ===== GENERAZIONE =====
output = {}
top_list = []

for ruota in RUOTE:
    estrazioni = data.get(ruota, [])

    if len(estrazioni) < 10:
        continue

    ritardi = calcola_ritardi(estrazioni)

    # numero più ritardatario
    R1 = max(ritardi, key=ritardi.get)

    # numeri frequenti
    freq = numeri_frequenti(estrazioni)

    # scegli il migliore compatibile
    C1 = None
    for n in freq:
        if n != R1:
            C1 = n
            break

    if not C1:
        continue

    ambo = sorted([R1, C1])

    # score semplice
    score = ritardi[R1] + freq.index(C1)

    output[ruota] = {
        "ambo": ambo,
        "score": score
    }

    top_list.append({
        "ruota": ruota,
        "ambo": ambo,
        "score": score
    })

# ===== ORDINA TOP =====
top_list = sorted(top_list, key=lambda x: x["score"], reverse=True)[:3]

# ===== JOLLY =====
def ruota_successiva(r):
    idx = RUOTE.index(r)
    return RUOTE[(idx + 1) % len(RUOTE)]

jolly = {
    "ruota": ruota_successiva(top_list[0]["ruota"]),
    "ambo": top_list[0]["ambo"]
} if top_list else {}

# ===== SALVA =====
risultato = {
    "ruote": output,
    "top": top_list,
    "jolly": jolly
}

with open("risultati.json", "w", encoding="utf-8") as f:
    json.dump(risultato, f, indent=2)

print("🔥 Generazione completata (Motore 3)")
