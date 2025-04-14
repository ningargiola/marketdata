import requests
import os
import json
from datetime import datetime
from pathlib import Path
from time import sleep

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

TICKER_FILE = Path("shared/tickers.txt")
STATIC_FILE = Path("static_data.json")
MARKET_FILE = Path("market_data.json")
COMBINED_FILE = Path("combined_data.json")

BASE_URL = "https://finnhub.io/api/v1/quote"
RATE_LIMIT = 60
BATCH_DELAY = 60


def load_tickers():
    if not TICKER_FILE.exists():
        raise FileNotFoundError("tickers.txt not found.")
    return [line.strip() for line in TICKER_FILE.read_text().splitlines() if line.strip()]


def fetch_market_data(tickers):
    market_data = {}
    for i, symbol in enumerate(tickers):
        try:
            url = f"{BASE_URL}?symbol={symbol}&token={FINNHUB_API_KEY}"
            response = requests.get(url)
            response.raise_for_status()
            quote = response.json()

            market_data[symbol] = {
                "symbol": symbol,
                "currentPrice": quote.get("c"),
                "change": quote.get("d"),
                "percentChange": quote.get("dp"),
                "open": quote.get("o"),
                "high": quote.get("h"),
                "low": quote.get("l"),
                "previousClose": quote.get("pc"),
                "lastUpdated": datetime.now().isoformat()
            }

        except Exception as e:
            print(f"❌ Error fetching {symbol}: {e}")

        if (i + 1) % RATE_LIMIT == 0:
            print("⏳ Sleeping to respect Finnhub rate limits...")
            sleep(BATCH_DELAY)

    return market_data


def merge_with_static_data(market_data):
    if not STATIC_FILE.exists():
        raise FileNotFoundError("static_data.json not found.")

    static_data = json.loads(STATIC_FILE.read_text())
    combined_data = {}

    for symbol, static_entry in static_data.items():
        market_entry = market_data.get(symbol, {})
        combined_data[symbol] = {
            **static_entry,
            **market_entry  # market data overrides or supplements static
        }

    return combined_data


def save_json(data, path, label):
    path.write_text(json.dumps(data, indent=2))
    print(f"✅ Saved {label} for {len(data)} tickers → {path.name}")


def main():
    tickers = load_tickers()
    print(f"📈 Fetching real-time market data for {len(tickers)} tickers...")

    market_data = fetch_market_data(tickers)
    save_json(market_data, MARKET_FILE, "market data")

    combined_data = merge_with_static_data(market_data)
    save_json(combined_data, COMBINED_FILE, "combined data")


if __name__ == "__main__":
    main()
