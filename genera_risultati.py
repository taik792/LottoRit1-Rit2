import json

RUOTE = [
    "Bari",
    "Cagliari",
    "Firenze",
    "Genova",
    "Milano",
    "Napoli",
    "Palermo",
    "Roma",
    "Torino",
    "Venezia"
]


def carica_estrazioni():
    with open("estrazioni.json", "r", encoding="utf-8") as f:
        return json.load(f)


def score_numero(storico, numero):
    score = 0

    # Frequenza pesata sulle ultime 30 estrazioni
    ultime_30 = storico[-30:]

    for i, estrazione in enumerate(reversed(ultime_30), start=1):
        peso = 31 - i

        if numero in estrazione:
            score += peso * 3

    # Bonus decina forte
    decina = numero // 10

    for estrazione in storico[-15:]:
        for n in estrazione:
            if n // 10 == decina:
                score += 2

    # Bonus numeri forti/speculari
    numeri_forti = [9, 18, 27, 36, 45, 54, 63, 72, 81, 90]

    if numero in numeri_forti:
        score += 12

    return score


def genera_previsione_ruota(storico):
    ultima = storico[-1]

    candidati = []

    for numero in range(1, 91):
        # Evita numeri già usciti nell’ultima estrazione
        if numero not in ultima:
            score = score_numero(storico, numero)
            candidati.append((numero, score))

    candidati.sort(key=lambda x: x[1], reverse=True)

    top3 = [
        candidati[0][0],
        candidati[1][0],
        candidati[2][0]
    ]

    score_totale = (
        candidati[0][1] +
        candidati[1][1] +
        candidati[2][1]
    )

    return {
        "ultima": ultima,
        "terno": top3,
        "score": score_totale
    }


def main():
    dati = carica_estrazioni()

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
                "ruota": ruota,
                "terno": valori["terno"],
                "score": valori["score"]
            }
            for ruota, valori in top
        ],

        "jolly": {
            "ruota": top[0][0],
            "terno": top[0][1]["terno"]
        },

        "ruote": risultati
    }

    with open("risultati.json", "w", encoding="utf-8") as f:
        json.dump(
            finale,
            f,
            indent=2,
            ensure_ascii=False
        )

    print("Motore 8 generato correttamente")


if __name__ == "__main__":
    main()