import json
from collections import Counter

RUOTE = ["Bari","Cagliari","Firenze","Genova","Milano",
         "Napoli","Palermo","Roma","Torino","Venezia"]

# ===== CARICA ESTRAZIONI =====
with open("estrazioni.json", encoding="utf-8") as f:
    data = json.load(f)

risultati = {"ruote": {}, "top": [], "jolly": {}}

def ritardi(lista):
    rit = {}
    ultimi = lista[-200:]  # storico corto = più preciso
    for n in range(1, 91):
        rit[n] = 0
        for estr in reversed(ultimi):
            if n in estr:
                break
            rit[n] += 1
    return rit

def frequenze(lista):
    ultimi = lista[-20:]
    flat = [n for estr in ultimi for n in estr]
    return Counter(flat)

def genera_ambo(ruota, estrazioni):
    r = ritardi(estrazioni)
    f = frequenze(estrazioni)

    # top ritardatari
    top_r = sorted(r.items(), key=lambda x: x[1], reverse=True)[:5]

    base = top_r[0][0]  # ritardatario più forte

    candidati = []

    for n in range(1, 91):
        if n == base:
            continue

        score = 0

        # ritardo
        score += r[n] * 2

        # frequenza recente
        score += f[n] * 5

        # vicinanza
        if abs(n - base) <= 2:
            score += 10
        if abs(n - base) == 10:
            score += 6

        candidati.append((n, score))

    candidati.sort(key=lambda x: x[1], reverse=True)

    secondo = candidati[0][0]

    return [base, secondo], candidati[0][1]


# ===== GENERAZIONE =====
for ruota in RUOTE:
    estrazioni = data[ruota]

    ambo, score = genera_ambo(ruota, estrazioni)

    risultati["ruote"][ruota] = {
        "ambo": ambo,
        "score": score
    }

# ===== TOP =====
top3 = sorted(risultati["ruote"].items(),
              key=lambda x: x[1]["score"],
              reverse=True)[:3]

for nome, dati in top3:
    risultati["top"].append({
        "ruota": nome,
        "ambo": dati["ambo"]
    })

# ===== JOLLY =====
best = top3[0]
risultati["jolly"] = {
    "ruota": best[0],
    "ambo": best[1]["ambo"]
}

# ===== SALVA =====
with open("risultati.json", "w", encoding="utf-8") as f:
    json.dump(risultati, f, indent=2)

print("🔥 Motore 3 PRO creato")