import json
from collections import Counter

RUOTE = [
    "Bari", "Cagliari", "Firenze", "Genova", "Milano",
    "Napoli", "Palermo", "Roma", "Torino", "Venezia"
]


def carica_estrazioni():
    with open("estrazioni.json", "r", encoding="utf-8") as f:
        return json.load(f)


def score_numero(storico, numero):
    score = 0

    # frequenza pesata sulle ultime estrazioni
    for i, estrazione in enumerate(reversed(storico[-30:]), start=1):
        peso = 31 - i
        if numero in estrazione:
            score += peso * 3

    # bonus decina forte
    decina = numero // 10
    for estrazione in storico[-15:]:
        for n in estrazione:
            if n // 10 == decina:
                score += 2

    # bonus finale per numeri speculari
    if numero in [9, 18, 27, 36, 45, 54, 63, 72, 81, 90]:
        score += 12

    return score


def genera_previsione_ruota(storico):
    ultima = storico[-1]

    candidati = []
    for n in range(1, 91):
        if n not in ultima:  # mai numeri già usciti subito
            s = score_numero(storico, n)
            candidati.append((n, s))

    candidati.sort(key=lambda x: x[1], reverse=True)

    top3 = [c[0] for c in candidati[:3]]
    score = sum(c[1] for c in candidati[:3])

    return {
        "ultima": ultima,
        "terno": top3,
        "score": score
    }


def main():
    dati = carica_estrzioni = carica_estrazioni()

    risultati = {}

    for ruota in RUOTE:
        storico = dati.get(ruota, [])
        if len(storico) < 5:
            continue
        risultati[ruota] = genera_previsione_ruota(storico)

    top = sorted(
        risultati.items(),
        key=lambda x: x[1]["score"],
        reverse=True
    )[:3]

    finale = {
        "top": [
            {
                "ruota": r,
                "terno": v["terno"],
                "score": v["score"]
            }
            for r, v in top
        ],
        "jolly": {
    main()
