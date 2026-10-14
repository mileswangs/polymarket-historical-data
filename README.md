# Polymarket Historical Data

Free Polymarket historical order book data: tick-level L2 updates, trades, on-chain fills and the
Chainlink TWAP that crypto Up/Down markets resolve on. Download a full day for free, then get
every market from [PMData](https://pmdata.dev).

| Free sample | Where |
| --- | --- |
| BTC Up/Down 5m, 2026-10-01: 288 markets, 49.9M order book events, 418K trades, 1.1M on-chain fills, Chainlink BTC/USD price and 60s TWAP (519 MB Parquet) | [Hugging Face](https://huggingface.co/datasets/mileswangs/polymarket-btc-updown-5m-orderbook-tick-data) · [Kaggle](https://www.kaggle.com/datasets/sumire2/polymarket-btc-updown-5m-order-book-tick-data) |

## Why this data

Polymarket's API returns the order book as it is now, and price history only as a line. Past
order books exist only if someone recorded the WebSocket feed while the market was live.
PMData records it:

- Every `book` and `price_change` WebSocket message, unmodified, so any book can be rebuilt at
  any moment.
- Polymarket's event time and PMData's receive time on every row, at microsecond precision.
  Collected in AWS London, colocated with Polymarket's exchange (4.6 ms median latency), on a
  clock synced to [AWS PHC](https://aws.amazon.com/blogs/compute/its-about-time-microsecond-accurate-clocks-on-amazon-ec2-instances/).
- Two WebSocket connections per market, on separate networks.
- Chainlink Data Streams and TWAP, collected directly from Chainlink. The 60s TWAP reproduces
  all 288 outcomes in the sample.

## Quick start

```bash
pip install polars huggingface_hub
huggingface-cli download mileswangs/polymarket-btc-updown-5m-orderbook-tick-data --repo-type dataset --local-dir data
cd data && python ../examples/quickstart.py
```

[`examples/quickstart.py`](examples/quickstart.py) measures collection latency, loads one market's
order book events, and reproduces every market's outcome from the Chainlink TWAP.

For fill-level backtests with queue position and latency, use
[pm-hftbacktest](https://github.com/mileswangs/pm-hftbacktest). Across 547 BTC 5-minute markets,
its backtests [matched live trading in 95.32% of markets](https://pmdata.dev/research/polymarket-backtest-accuracy-95-32).

## Full data from PMData

- All Polymarket markets since 2026-05-01 (politics, sports, weather, crypto and more); crypto
  Up/Down markets since 2026-02-01.
- One Parquet file per market, data type and day, or one ZIP per Up/Down series per day:

```python
import pandas as pd

url = "https://api.pmdata.dev/v1/polymarket/l2/2026/10/01/btc-updown-5m-1790812800.parquet"
df = pd.read_parquet(url, storage_options={"api_key": "<YOUR_API_KEY>", "User-Agent": "Mozilla/5.0"})
```

- Free trial with 600 downloads: [pmdata.dev](https://pmdata.dev) ·
  [Docs](https://pmdata.dev/docs) · [Compare providers](https://pmdata.dev/compare)

## License

Sample data: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), credit PMData. Code: MIT.
