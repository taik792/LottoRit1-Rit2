# genera_risultati.py
# VERSIONE CORRETTA — salva SOLO ambo calcolato (non i 5 numeri estratti)

import json
from collections import Counter


def carica_estrazioni():
    with open("estrazioni.json", "r", encoding="utf-8") as f:
        return json.load(f)


def calcola_ambo(estrazione):
    """
    Logica semplice e stabile:
    prende i 2 numeri più forti dalla ruota
    (qui esempio: primo + ultimo numero della cinquina)
    """

    if len(estrazione) < 5:
        return [estrazione[0], estrzione[1]]

    n1 = estrazione[0]
    n2 = estrazione[4]

    if n1 == n2:
        n2 = estrazione[1]

    return sorted([n1, n2])


def calcola_score(ambo, storico_ruota):
    """
    Score migliorato:
    più il numero ricorre nello storico → più sale
    """

    score = 0

    for estrazione in storico_ruota[-50:]:
        for numero in ambo:
            if numero in estrazione:
                score += 25

        if all(n in estrazione for n in ambo):
            score += 100

    return score


def genera():
    dati = carica_estrazioni()

    risultati = []

    for ruota, storico in dati.items():

        if not storico:
            continue

        ultima_estrazione = storico[-1]

        ambo = calcola_ambo(ultima_estrazione)

        score = calcola_score(ambo, storico)

        risultati.append({
            "ruota": ruota,
            "numeri": ambo,  # SOLO 2 NUMERI
            "score": score,
            "ultima_estrazione": ultima_estrazione
        })

    risultati.sort(key=lambda x: x["score"], reverse=True)

    top = risultati[:3]

    jolly = top[0] if top else {}

    output = {
        "top": top,
        "jolly": {
            "ruota": jolly.get("ruota", ""),
            "numeri": jolly.get("numeri", [])
        },
        "ambo_forte": risultati
    }

    with open("risultati.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("risultati.json aggiornato correttamente")


if __name__ == "__main__":
    genera()