# Binance BTCUSDT Funding Data

Automatischer Abruf der Binance USD-M Futures **BTCUSDT** Funding-Daten via GitHub Actions.

## Was passiert hier?

- Ein Python-Script ruft alle 5 Minuten die aktuelle Funding-Rate von der Binance Futures API ab.
- Die Daten werden in [`data/binance_btcusdt_funding.csv`](data/binance_btcusdt_funding.csv) geschrieben (eine Zeile = aktueller Stand).
- Ein GitHub-Actions-Workflow committet und pusht die CSV automatisch, wenn sich die Daten geändert haben.

## Aktualisierte Datei

| Datei | Inhalt |
|---|---|
| `data/binance_btcusdt_funding.csv` | Aktuelle Funding-Daten (markPrice, fundingRate, nextFundingTime, …) |

## Workflow manuell starten

1. Im Repo auf **Actions** klicken.
2. Links den Workflow **Update Binance Funding** auswählen.
3. Rechts auf **Run workflow** → **Run workflow** klicken.

## Datenquelle

Binance USD-M Futures Premium Index API:  
`GET https://fapi.binance.com/fapi/v1/premiumIndex?symbol=BTCUSDT`

## Projektstruktur

```
scripts/update_funding.py          # Abruf-Script (nur Standardbibliothek)
data/binance_btcusdt_funding.csv   # CSV mit aktuellen Funding-Daten
.github/workflows/update_funding.yml  # GitHub Actions Workflow (alle 5 Min)
```
