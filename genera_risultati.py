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
    "Venezia",
    "Nazionale"
]


def carica_estrazioni():
    with open("estrazioni.json", "r", encoding="utf-8") as file:
        return json.load(file)


def salva_risultati(risultati):
    with open("risultati.json", "w", encoding="utf-8") as file:
        json.dump(risultati, file, indent=2, ensure_ascii=False)


def prendi_ultime_5_ruota(dati, ruota):
    """
    Il tuo estrazioni.json è strutturato così:

    {
      "Bari": [
        [26, 59, 60, 67, 17],
        [84, 80, 40, 15, 9],
        ...
      ],
      "Cagliari": [...]
    }

    quindi:
    dati[ruota] = lista estrazioni
    """

    ultime = []

    if ruota not in dati:
        return []

    estrazioni_ruota = dati[ruota]

    # dalla più recente alla più vecchia
    for estrazione in reversed(estrazioni_ruota):
        for numero in estrazione:
            if numero not in ultime:
                ultime.append(numero)

            if len(ultime) >= 5:
                return ultime[:5]

    return ultime[:5]


def genera_terno(ultime_5):
    """
    Logica base Motore 8:
    prende i primi 3 numeri più forti
    """

    if len(ultime_5) < 3:
        return [1, 2, 3]

    return ultime_5[:3]


def calcola_score(terno):
    """
    Score semplice:
    più i numeri sono alti, più score alto
    (poi lo miglioriamo, perché la vita ama complicarsi)
    """

    return sum(terno) * 10 + len(set(terno)) * 3


def genera_risultati():
    dati = carica_estrazioni()

    top = []
    terno_forte = []

    for ruota in RUOTE:
        ultime_5 = prendi_ultime_5_ruota(dati, ruota)

        if len(ultime_5) < 3:
            continue

        terno = genera_terno(ultime_5)
        score = calcola_score(terno)

        record = {
            "ruota": ruota,
            "terno": terno,
            "score": score
        }

        top.append(record)
        terno_forte.append(record)

    # ordina per score decrescente
    top.sort(key=lambda x: x["score"], reverse=True)
    terno_forte.sort(key=lambda x: x["score"], reverse=True)

    # TOP = prime 3
    top = top[:3]

    # JOLLY = migliore assoluto
    jolly = top[0] if top else {
        "ruota": "Bari",
        "terno": [1, 2, 3],
        "score": 0
    }

    risultati = {
        "top": top,
        "jolly": jolly,
        "terno_forte": terno_forte
    }

    salva_risultati(risultati)
    print("risultati.json aggiornato correttamente")


if __name__ == "__main__":
    genera_risultati()