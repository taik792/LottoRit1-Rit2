import json
from itertools import combinations

RUOTE_ORDINE = [
    "Bari", "Cagliari", "Firenze",
    "Genova", "Milano", "Napoli",
    "Palermo", "Roma", "Torino", "Venezia"
]


def carica_estrazioni():
    with open("estrazioni.json", "r", encoding="utf-8") as f:
        return json.load(f)


def score_numero(n, estrazioni_ruota):
    """
    Score semplice:
    più il numero compare nello storico, più sale il punteggio
    """
    score = 0

    for estrazione in estrazioni_ruota:
        if n in estrazione:
            score += 25

    return score


def trova_ambo_forte(nome_ruota, estrazioni_ruota):
    """
    Regole:
    - usa l'ultima estrazione disponibile
    - NON può scegliere numeri presenti nell'ultima estrazione
    - sceglie l'ambo con score più alto
    """

    if not estrazioni_ruota:
        return None

    ultima_estrazione = estrazioni_ruota[-1]

    # numeri disponibili 1-90 ESCLUSI quelli appena usciti
    candidati = [
        n for n in range(1, 91)
        if n not in ultima_estrazione
    ]

    miglior_ambo = None
    miglior_score = -1

    for n1, n2 in combinations(candidati, 2):

        # doppia sicurezza: mai numeri già usciti
        if n1 in ultima_estrazione or n2 in ultima_estrazione:
            continue

        score = (
            score_numero(n1, estrazioni_ruota)
            + score_numero(n2, estrazioni_ruota)
        )

        if score > miglior_score:
            miglior_score = score
            miglior_ambo = [n1, n2]

    return {
        "ruota": nome_ruota,
        "numeri": miglior_ambo,
        "score": miglior_score,
        "ultima_estrazione": ultima_estrazione
    }


def genera_risultati():
    dati = carica_estrazioni()

    risultati_ruote = []

    for ruota in RUOTE_ORDINE:
        if ruota not in dati:
            continue

        risultato = trova_ambo_forte(
            ruota,
            dati[ruota]
        )

        if risultato:
            risultati_ruote.append(risultato)

    # ordina per score decrescente
    risultati_ordinati = sorted(
        risultati_ruote,
        key=lambda x: x["score"],
        reverse=True
    )

    top = risultati_ordinati[:3]
    jolly = risultati_ordinati[:1]

    output = {
        "top": top,
        "jolly": jolly,
        "ambo_forte": risultati_ruote
    }

    with open("risultati.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("risultati.json aggiornato correttamente")


if __name__ == "__main__":
    genera_risultati()