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

NUMERO_ESTRAZIONI = 200  # qui il motore usa storico lungo


def carica_estrazioni():
    with open("estrazioni.json", "r", encoding="utf-8") as file:
        return json.load(file)


def salva_risultati(risultati):
    with open("risultati.json", "w", encoding="utf-8") as file:
        json.dump(
            risultati,
            file,
            indent=2,
            ensure_ascii=False
        )


def prendi_ultime_estrazioni(dati, ruota):
    """
    Il tuo JSON è ordinato:
    dal più vecchio → al più recente

    quindi:
    dati[ruota][-1] = ultima estrazione vera
    dati[ruota][-120:] = ultime 120 estrazioni
    """

    if ruota not in dati:
        return []

    lista = dati[ruota]

    if not lista:
        return []

    return lista[-NUMERO_ESTRAZIONI:]


def genera_terno_da_storico(estrazioni):
    """
    Motore 8:
    usa storico lungo + frequenza
    per trovare il terno forte
    """

    frequenze = {}

    for estrazione in estrazioni:
        for numero in estrazione:
            frequenze[numero] = frequenze.get(numero, 0) + 1

    if not frequenze:
        return [1, 2, 3]

    ordinati = sorted(
        frequenze.items(),
        key=lambda x: (-x[1], -x[0])
    )

    terno = [numero for numero, _ in ordinati[:3]]

    while len(terno) < 3:
        terno.append(len(terno) + 1)

    return terno


def calcola_score(terno, estrazioni):
    """
    Score:
    - frequenza presenza
    - peso numerico
    """

    score = 0

    for estrazione in estrazioni:
        for numero in terno:
            if numero in estrazione:
                score += 100

    score += sum(terno) * 3

    return score


def genera_risultati():
    dati = carica_estrazioni()

    terno_forte = []

    for ruota in RUOTE:
        storico = prendi_ultime_estrazioni(dati, ruota)

        if len(storico) < 5:
            continue

        ultima_estrazione = storico[-1]

        terno = genera_terno_da_storico(storico)
        score = calcola_score(terno, storico)

        record = {
            "ruota": ruota,
            "ultima_estrazione": ultima_estrazione,
            "terno": terno,
            "score": score
        }

        terno_forte.append(record)

    # ordina per score decrescente
    terno_forte.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # TOP = prime 3 ruote
    top = terno_forte[:3]

    # JOLLY = migliore assoluto
    if top:
        jolly = top[0]
    else:
        jolly = {
            "ruota": "Bari",
            "ultima_estrazione": [1, 2, 3, 4, 5],
            "terno": [1, 2, 3],
            "score": 0
        }

    risultati = {
        "top": top,
        "jolly": jolly,
        "terno_forte": terno_forte
    }

    salva_risultati(risultati)

    print("Motore 8 aggiornato correttamente")


if __name__ == "__main__":
    genera_risultati()
