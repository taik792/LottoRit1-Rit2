import json
from collections import Counter

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

FILE_ESTRAZIONI = "estrazioni.json"
FILE_RISULTATI = "risultati.json"


def normalizza_numero(n):
    """
    Mantiene i numeri tra 1 e 90
    perché il lotto, con raro buon senso,
    non accetta il 147.
    """
    while n > 90:
        n -= 90
    while n < 1:
        n += 90
    return n


def carica_estrazioni():
    with open(FILE_ESTRAZIONI, "r", encoding="utf-8") as f:
        return json.load(f)


def prendi_ultime_5_ruota(dati, ruota):
    """
    Prende le ultime 5 estrazioni della ruota
    """
    ultime = []

    for estrazione in reversed(dati):
        if ruota in estrazione:
            valori = estrazione[ruota]

            if isinstance(valori, list) and len(valori) >= 5:
                ultime.append(valori[:5])

        if len(ultime) == 5:
            break

    return ultime


def calcola_terno(ultime_5):
    """
    Logica Motore 8:
    usa frequenze + somme + ritardo implicito
    senza affidarsi agli astri.
    """

    tutti = []
    for estrazione in ultime_5:
        tutti.extend(estrazione)

    frequenze = Counter(tutti)

    # più frequenti
    frequenti = [
        numero for numero, _ in frequenze.most_common(6)
    ]

    # se pochi numeri disponibili
    while len(frequenti) < 6:
        frequenti.append(normalizza_numero(len(frequenti) * 11 + 7))

    base = frequenti[:3]

    # trasformazione numerica
    n1 = normalizza_numero(base[0] + base[1])
    n2 = normalizza_numero(base[1] + base[2])
    n3 = normalizza_numero(base[0] + base[2])

    terno = list(set([
        n1,
        n2,
        n3,
        base[0],
        base[1],
        base[2]
    ]))

    # ordina e prende i migliori 3
    terno = sorted(terno)[:3]

    # score semplice
    score = (
        frequenze.get(base[0], 0) * 100 +
        frequenze.get(base[1], 0) * 100 +
        frequenze.get(base[2], 0) * 100 +
        sum(terno)
    )

    return {
        "terno": terno,
        "score": score
    }


def genera_risultati():
    dati = carica_estrazioni()

    previsioni = []

    for ruota in RUOTE:
        ultime_5 = prendi_ultime_5_ruota(dati, ruota)

        if len(ultime_5) < 3:
            continue

        risultato = calcola_terno(ultime_5)

        previsioni.append({
            "ruota": ruota,
            "terno": risultato["terno"],
            "score": risultato["score"]
        })

    # ordina per score
    previsioni.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    top = previsioni[:3]

    jolly = top[0] if top else {
        "ruota": "-",
        "terno": [],
        "score": 0
    }

    risultati_finali = {
        "top": top,
        "jolly": jolly,
        "terno_forte": previsioni
    }

    with open(FILE_RISULTATI, "w", encoding="utf-8") as f:
        json.dump(
            risultati_finali,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("risultati.json generato correttamente")


if __name__ == "__main__":
    genera_risultati()