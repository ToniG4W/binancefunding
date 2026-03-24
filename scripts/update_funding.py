#!/usr/bin/env python3
"""Fetch Binance USD-M Futures BTCUSDT funding data and write to CSV.

Optionally push the updated CSV back to GitHub when ENABLE_GIT_PUSH=true.

Environment variables:
  ENABLE_GIT_PUSH  - set to "true" to commit & push after update
  GIT_USER_NAME    - git commit author name  (default: bot)
  GIT_USER_EMAIL   - git commit author email (default: bot@noreply)
  GIT_BRANCH       - branch to push to       (default: main)
"""

import csv
import json
import os
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone

API_URL = "https://fapi.binance.com/fapi/v1/premiumIndex?symbol=BTCUSDT"
REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
CSV_PATH = os.path.join(REPO_ROOT, "data", "binance_btcusdt_funding.csv")

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
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerow(row)


def git_push() -> None:
    """Commit and push the CSV if ENABLE_GIT_PUSH=true and the file changed."""
    if os.environ.get("ENABLE_GIT_PUSH", "").lower() != "true":
        print("[INFO] Git push disabled (ENABLE_GIT_PUSH != true)")
        return

    token = os.environ.get("GITHUB_TOKEN", "")
    user = os.environ.get("GIT_USER_NAME", "funding-bot")
    email = os.environ.get("GIT_USER_EMAIL", "funding-bot@users.noreply.github.com")
    branch = os.environ.get("GIT_BRANCH", "main")

    def run(cmd: list[str]) -> subprocess.CompletedProcess:
        return subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)

    # Set authenticated remote URL if token is provided
    if token:
        origin = run(["git", "remote", "get-url", "origin"])
        url = origin.stdout.strip()
        # Replace https://github.com/... with https://x-access-token:{token}@github.com/...
        if url.startswith("https://") and "github.com" in url:
            repo_path = url.split("github.com/", 1)[-1]
            auth_url = f"https://x-access-token:{token}@github.com/{repo_path}"
            run(["git", "remote", "set-url", "origin", auth_url])
            print("[INFO] Remote URL updated with token auth")
    else:
        print("[WARN] GITHUB_TOKEN not set — push may fail without auth")

    run(["git", "config", "user.name", user])
    run(["git", "config", "user.email", email])
    run(["git", "add", "data/binance_btcusdt_funding.csv"])

    diff = run(["git", "diff", "--cached", "--quiet"])
    if diff.returncode == 0:
        print("[INFO] CSV unchanged — nothing to push")
        return

    commit = run(["git", "commit", "-m", "Update BTCUSDT funding data"])
    if commit.returncode != 0:
        print(f"[ERROR] git commit failed: {commit.stderr.strip()}")
        sys.exit(1)

    push = run(["git", "push", "origin", branch])
    if push.returncode != 0:
        print(f"[ERROR] git push failed: {push.stderr.strip()}")
        sys.exit(1)

    print(f"[OK] Pushed to origin/{branch}")


def main() -> None:
    data = fetch_funding_data()
    row = build_row(data)
    write_csv(row)
    print(f"[OK] binance_btcusdt_funding.csv updated — {row['exchangeTimeUtc']}")
    git_push()


if __name__ == "__main__":
    main()
