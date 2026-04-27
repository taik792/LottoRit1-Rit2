# Motore 8 – genera_risultati.py + index.html

## genera_risulti.py

```python
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
            "ruota": top[0][0],
            "terno": top[0][1]["terno"]
        },
        "ruote": risultati
    }

    with open("risultati.json", "w", encoding="utf-8") as f:
        json.dump(finale, f, indent=2, ensure_ascii=False)

    print("Motore 8 generato correttamente")


if __name__ == "__main__":
    main()
```

---

## index.html

```html
<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Lotto Elite PRO - Motore 8</title>

<style>
body {
    margin: 0;
    background: #031b2f;
    color: white;
    font-family: Arial, sans-serif;
    text-align: center;
}

h1 {
    color: #00eaff;
    margin-top: 30px;
    font-size: 42px;
}

h2 {
    margin-top: 40px;
    font-size: 38px;
}

.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 20px;
    padding: 30px;
}

.card {
    background: #0d2f4f;
    border: 4px solid #00f0ff;
    border-radius: 28px;
    padding: 20px;
    box-shadow: 0 0 18px rgba(0,255,255,0.4);
}

.top-card {
    background: #3b2a00;
    border-color: gold;
}

.jolly-card {
    background: #8b0000;
    border-color: red;
}

.numeri {
    font-size: 42px;
    color: #00f0ff;
    font-weight: bold;
    margin: 20px 0;
}

.score {
    color: pink;
    font-size: 26px;
}
</style>
</head>
<body>

<h1>🔥 LOTTO ELITE PRO</h1>
<h2>Motore 8</h2>

<div id="app"></div>

<script>
fetch("risultati.json")
.then(r => r.json())
.then(data => {
    const app = document.getElementById("app");

    let html = `<h2>🎯 TOP</h2><div class="grid">`;

    data.top.forEach(item => {
        html += `
        <div class="card top-card">
            <h3>${item.ruota}</h3>
            <div class="numeri">${item.terno.join(" — ")}</div>
            <div class="score">Score: ${item.score}</div>
        </div>`;
    });

    html += `</div>`;

    html += `
    <h2>💣 JOLLY</h2>
    <div class="grid">
        <div class="card jolly-card">
            <h3>${data.jolly.ruota}</h3>
            <div class="numeri">${data.jolly.terno.join(" — ")}</div>
        </div>
    </div>`;

    html += `<h2>📊 TERNO FORTE</h2><div class="grid">`;

    Object.entries(data.ruote).forEach(([ruota, v]) => {
        html += `
        <div class="card">
            <h3>${ruota}</h3>
            <p><strong>Ultima Estrazione</strong><br>${v.ultima.join(" • ")}</p>
            <p><strong>Terno Forte</strong></p>
            <div class="numeri">${v.terno.join(" — ")}</div>
            <div class="score">Score: ${v.score}</div>
        </div>`;
    });

    html += `</div>`;
    app.innerHTML = html;
});
</script>

</body>
</html>
```
