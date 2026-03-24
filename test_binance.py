import json
import sys
import urllib.request
import urllib.error

URL = "https://fapi.binance.com/fapi/v1/premiumIndex?symbol=BTCUSDT"

def main():
    print("Testing Binance endpoint...")
    print(f"URL: {URL}")

    req = urllib.request.Request(
        URL,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = resp.read().decode("utf-8", errors="replace")

            print("")
            print("=== RESULT ===")
            print(f"HTTP Status: {resp.status}")
            print("")
            print("=== HEADERS ===")
            for k, v in resp.headers.items():
                print(f"{k}: {v}")

            print("")
            print("=== BODY (raw, first 1000 chars) ===")
            print(body[:1000])

            print("")
            print("=== BODY (parsed JSON) ===")
            try:
                parsed = json.loads(body)
                print(json.dumps(parsed, indent=2))
            except json.JSONDecodeError:
                print("Response is not valid JSON.")

            sys.exit(0)

    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")

        print("")
        print("=== HTTP ERROR ===")
        print(f"Status: {e.code}")
        print(f"Reason: {e.reason}")

        print("")
        print("=== HEADERS ===")
        for k, v in e.headers.items():
            print(f"{k}: {v}")

        print("")
        print("=== BODY ===")
        print(error_body[:1000])

        sys.exit(1)

    except Exception as e:
        print("")
        print("=== GENERAL ERROR ===")
        print(repr(e))
        sys.exit(2)

if __name__ == "__main__":
    main()