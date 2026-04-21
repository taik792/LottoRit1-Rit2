import json
from collections import Counter
from itertools import combinations

RUOTE = [
    "Bari", "Cagliari", "Firenze", "Genova", "Milano",
    "Napoli", "Palermo", "Roma", "Torino", "Venezia"
]

ANALISI_ESTRAZIONI = 18
DISTANZA_MIN = 6
DISTANZA_MAX = 28


def carica_estrazioni():
    with open("estrazioni.json", "r", encoding="utf-8") as f:
        return json.load(f)


def distanza(a, b):
    d = abs(a - b)
    return min(d, 90 - d)


def frequenze_recenti(storico):
    freq = Counter()

    recenti = storico[-ANALISI_ESTRAZIONI:]

    for estrazione in recenti:
        for numero in estrazione:
            freq[numero] += 1

    return freq


def ritardo(numero, storico):
    delay = 0

    for estrazione in reversed(storico):
        if numero in estrazione:
            return delay
        delay += 1

    return delay


def coppia_valida(a, b, ultima):
    if a == b:
        return False

    dist = distanza(a, b)

    if dist < DISTANZA_MIN:
        return False

    if dist > DISTANZA_MAX:
        return False

    # evita doppio numero appena uscito
    if a in ultima and b in ultima:
        return False

    return True


def trova_ambo_reale(storico):
    ultima = storico[-1]
    freq = frequenze_recenti(storico)

    candidati = []

    # top 20 numeri più forti
    numeri_forti = [
        n for n, _ in sorted(
            freq.items(),
            key=lambda x: x[1],
            reverse=True
        )[:20]
    ]

    for a, b in combinations(numeri_forti, 2):

        if not coppia_valida(a, b, ultima):
            continue

        freq_score = (freq[a] + freq[b]) * 12

        rit_score = (
            ritardo(a, storico) +
            ritardo(b, storico)
        ) * 6

        dist = distanza(a, b)

        bonus = 0

        if 8 <= dist <= 16:
            bonus += 30

        if str(a)[-1] == str(b)[-1]:
            bonus += 12

        if abs((a // 10) - (b // 10)) == 1:
            bonus += 10

        score = freq_score + rit_score + bonus

        candidati.append({
            "numeri": sorted([a, b]),
            "score": round(score, 2)
        })

    if not candidati:
        return {
            "numeri": [7, 29],
            "score": 0
        }

    candidati.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return candidati[0]


def genera():
    dati = carica_estrazioni()

    risultati = []

    for ruota in RUOTE:
        if ruota not in dati:
            continue

        storico = dati[ruota]

        if len(storico) < 5:
            continue

        previsione = trova_ambo_reale(storico)

        risultati.append({
            "ruota": ruota,
            "numeri": previsione["numeri"],
            "score": previsione["score"],
            "ultima_estrazione": storico[-1]
        })

    risultati.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    top = risultati[:2]  # più selettivo
    jolly = top[0] if top else {}

    output = {
        "top": top,
        "jolly": jolly,
        "ambo_forte": risultati
    }

    with open("risultati.json", "w", encoding="utf-8") as f:
        json.dump(
            output,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("MOTORE 6 aggiornato correttamente")


if __name__ == "__main__":
    genera()