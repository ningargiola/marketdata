# 📊 Stock Data Fetcher (Finnhub + Static Merge)

This project fetches **real-time market data** using the [Finnhub API](https://finnhub.io) and merges it with static company information to create clean, structured JSON files for use in apps or APIs.

---

## 🔧 Features

- ✅ Fetches current stock prices and metadata via Finnhub
- ✅ Merges with static data (e.g., company name, sector)
- ✅ Handles Finnhub rate limits (60 requests/minute)
- ✅ Produces three output files:
  - `market_data.json` – Real-time quote data
  - `static_data.json` – Static company information
  - `combined_data.json` – Final merged output
- ✅ Supports up to ~900 tickers on free tier
- ✅ GitHub Actions compatible for 15-minute updates

---

## 📁 Project Structure

```
marketdata/
├── backend/
│   └── fetch_market/
│       └── get_market_data.py     # Main script for fetching + merging
├── shared/
│   └── tickers.txt                # List of stock tickers to fetch
├── static_data.json               # Static stock data (pre-fetched or cached)
├── market_data.json               # Real-time market quotes
├── combined_data.json             # Final merged output
├── requirements.txt               # Python dependencies
└── .github/
    └── workflows/
        └── fetch-market.yml       # GitHub Actions workflow (15-min cron)
```

---

## 🚀 Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Your API Key

Set the `FINNHUB_API_KEY` as an environment variable:

```bash
export FINNHUB_API_KEY=your_finnhub_key
```

> **Optional**: You can also manage secrets through `.env` using `python-dotenv`.

### 3. Run the Script

```bash
python backend/fetch_market/get_market_data.py
```

---

## 🤖 GitHub Actions Automation

To automate updates every 15 minutes:

1. Add `FINNHUB_API_KEY` to your **GitHub repository secrets**
2. Place the workflow in `.github/workflows/fetch-market.yml`
3. GitHub will run the script and update your data every 15 minutes

---

## 📌 Notes

- Free tier of Finnhub allows 60 requests/minute. Script batches accordingly.
- You can store and serve JSON files from a CDN (e.g., Cloudflare R2 or Firebase).



