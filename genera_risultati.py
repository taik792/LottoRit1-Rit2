import json
from collections import Counter

RUOTE = ["Bari","Cagliari","Firenze","Genova","Milano",
         "Napoli","Palermo","Roma","Torino","Venezia"]

# ===== CARICA DATI =====
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

def numeri_frequenti_recenti(estrazioni, n=20):
    recenti = estrazioni[-n:]
    tutti = []
    for estr in recenti:
        tutti.extend(estr)
    count = Counter(tutti)
    return [num for num, _ in count.most_common(10)]

output = {}
giocate_top = []

for ruota in RUOTE:
    estrazioni = data[ruota]

    rit = ritardi(estrazioni)
    top_rit = sorted(rit.items(), key=lambda x: x[1], reverse=True)

    R1 = top_rit[0][0]

    frequenti = numeri_frequenti_recenti(estrazioni)

    # scegli numero compatibile diverso da R1
    C1 = None
    for n in frequenti:
        if n != R1:
            C1 = n
            break

    ambo = sorted([R1, C1])

    output[ruota] = {
        "ambo": ambo
    }

    giocate_top.append((ruota, ambo))

# ===== TOP 3 GIOCATE =====
giocate_top = giocate_top[:3]

# ===== JOLLY = RUOTA SUCCESSIVA =====
def ruota_jolly(ruota):
    idx = RUOTE.index(ruota)
    return RUOTE[(idx + 1) % len(RUOTE)]

jolly = {
    "ruota": ruota_jolly(giocate_top[0][0]),
    "ambo": giocate_top[0][1]
}

# ===== SALVA =====
with open("risultati.json", "w", encoding="utf-8") as f:
    json.dump({
        "ruote": output,
        "top": giocate_top,
        "jolly": jolly
    }, f, indent=2)

print("🔥 Motore 3 generato")