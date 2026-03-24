# Binance BTCUSDT Funding Data

Automatischer Abruf der Binance USD-M Futures **BTCUSDT** Funding-Daten.  
Läuft als Kinsta Cron Job und pusht die CSV optional zurück ins GitHub-Repo.

## Was passiert hier?

- `scripts/update_funding.py` ruft die aktuelle Funding-Rate von der Binance Futures API ab.
- Die Daten werden in [`data/binance_btcusdt_funding.csv`](data/binance_btcusdt_funding.csv) geschrieben (eine Zeile = aktueller Stand).
- Optional: das Script committet und pusht die CSV automatisch zurück ins Repo.

## Aktualisierte Datei

| Datei | Inhalt |
|---|---|
| `data/binance_btcusdt_funding.csv` | Aktuelle Funding-Daten (markPrice, fundingRate, nextFundingTime, …) |

## Kinsta Cron Job

Cron-Kommando:

```
python scripts/update_funding.py
```

Einfach als Cron Job in Kinsta eintragen (z.B. alle 5 Minuten).

## Environment Variables (optional, für Git-Push)

| Variable | Beschreibung | Default |
|---|---|---|
| `ENABLE_GIT_PUSH` | `true` aktiviert auto-commit & push | *(deaktiviert)* |
| `GITHUB_TOKEN` | GitHub Personal Access Token (für Push-Auth) | *(keiner)* |
| `GIT_USER_NAME` | Git-Commit-Autor Name | `funding-bot` |
| `GIT_USER_EMAIL` | Git-Commit-Autor E-Mail | `funding-bot@users.noreply.github.com` |
| `GIT_BRANCH` | Branch für Push | `main` |

Wenn `ENABLE_GIT_PUSH` nicht gesetzt ist, wird nur die lokale CSV aktualisiert.

## Datenquelle

Binance USD-M Futures Premium Index API:  
`GET https://fapi.binance.com/fapi/v1/premiumIndex?symbol=BTCUSDT`

## Projektstruktur

```
scripts/update_funding.py          # Haupt-Script (nur Standardbibliothek)
data/binance_btcusdt_funding.csv   # CSV mit aktuellen Funding-Daten
requirements.txt                   # Nixpacks Python-Erkennung
runtime.txt                        # Python-Version (3.11)
Procfile                           # Kinsta worker-Prozess
```
