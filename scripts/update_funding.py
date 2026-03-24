#!/usr/bin/env python3
"""Fetch Binance USD-M Futures BTCUSDT funding data and write to CSV."""

import csv
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone

API_URL = "https://fapi.binance.com/fapi/v1/premiumIndex?symbol=BTCUSDT"
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "binance_btcusdt_funding.csv")

HEADERS = [
    "time",
    "symbol",
    "markPrice",
    "indexPrice",
    "estimatedSettlePrice",
    "lastFundingRate",
    "interestRate",
    "nextFundingTime",
    "nextFundingTimeUtc",
    "exchangeTime",
    "exchangeTimeUtc",
]


def ms_to_utc_iso(ms: int) -> str:
    """Convert milliseconds timestamp to UTC ISO-8601 string."""
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch_funding_data() -> dict:
    """Fetch current funding data from Binance API with retries."""
    for attempt in range(1, 4):
        try:
            req = urllib.request.Request(API_URL, headers={"User-Agent": "Python/3"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as exc:
            print(f"[WARN] Attempt {attempt}/3 failed: {exc}")
            if attempt < 3:
                time.sleep(5 * attempt)
    print("[ERROR] All 3 attempts to reach Binance API failed.")
    sys.exit(1)


def build_row(data: dict) -> dict:
    """Build a CSV row dict from the API response."""
    return {
        "time": data["time"],
        "symbol": data["symbol"],
        "markPrice": data["markPrice"],
        "indexPrice": data["indexPrice"],
        "estimatedSettlePrice": data["estimatedSettlePrice"],
        "lastFundingRate": data["lastFundingRate"],
        "interestRate": data["interestRate"],
        "nextFundingTime": data["nextFundingTime"],
        "nextFundingTimeUtc": ms_to_utc_iso(data["nextFundingTime"]),
        "exchangeTime": data["time"],
        "exchangeTimeUtc": ms_to_utc_iso(data["time"]),
    }


def write_csv(row: dict) -> None:
    """Write a single row to the CSV file (overwrite with header + one data row)."""
    path = os.path.normpath(CSV_PATH)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerow(row)


def main() -> None:
    data = fetch_funding_data()
    row = build_row(data)
    write_csv(row)
    print(f"[OK] binance_btcusdt_funding.csv updated — {row['exchangeTimeUtc']}")


if __name__ == "__main__":
    main()
