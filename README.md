# Polymarket Historical Data: BTC Up/Down 5m Research Dataset

**Everything you need to research Polymarket BTC Up/Down 5m markets in one dataset: tick-level L2 order books, on-chain trades, and the Chainlink price they settle on.**

14 consecutive days (2026-08-08 to 2026-08-21), all 4,032 BTC Up/Down 5m markets. Every order book update as Polymarket sent it, every trade and on-chain fill, plus Chainlink Data Streams and the 60s TWAP that decides each market. Collected colocated with Polymarket in AWS London at 4.6 ms median latency, over two redundant WebSocket connections per market.

## Get any other day or market

- **Same code, any day.** Swap the file path for an API URL with your key in the `api_key` header (example at the end of
  Quick start): one Parquet file per market, data type and UTC day, or one ZIP per Up/Down series per day.
  [API reference](https://pmdata.dev/docs/api-reference?utm_source=github&utm_medium=dataset&utm_campaign=btc5m-sample)
- **Every market and date.** Crypto Up/Down markets from 2026-03-28 and every other Polymarket market (politics, sports,
  weather, crypto and more) from 2026-05-01. The free [markets catalog](https://pmdata.dev/docs/schemas/polymarket/markets-catalog?utm_source=github&utm_medium=dataset&utm_campaign=btc5m-sample)
  lists each market with the first and last day recorded: `https://public-data.pmdata.dev/v1/polymarket/markets.parquet`,
  no API key, updated daily.
- **Free account.** 600 downloads at sign-up, then 50 per month, for data older than 3 weeks; students and academic
  projects get 30 days of Plus free with brief proof of the course or project.
  [pmdata.dev](https://pmdata.dev/?utm_source=github&utm_medium=dataset&utm_campaign=btc5m-sample) · [Get an API key](https://pmdata.dev/app?utm_source=github&utm_medium=dataset&utm_campaign=btc5m-sample) ·
  [Docs](https://pmdata.dev/docs?utm_source=github&utm_medium=dataset&utm_campaign=btc5m-sample) · [Compare providers](https://pmdata.dev/compare?utm_source=github&utm_medium=dataset&utm_campaign=btc5m-sample)

| Free dataset | Where |
| --- | --- |
| BTC Up/Down 5m, 2026-08-08 to 2026-08-21: 4,032 markets, 457M order book events, 6.7M trades, 21.3M on-chain fills, Chainlink BTC/USD price and 60s TWAP (5.6 GB Parquet) | [Hugging Face](https://huggingface.co/datasets/mileswangs/polymarket-btc-updown-5m-orderbook-tick-data) · [Kaggle](https://www.kaggle.com/datasets/sumire2/polymarket-btc-updown-5m-order-book-tick-data) |

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
- Chainlink Data Streams and TWAP, collected directly from Chainlink. From 2026-08-14 on, the 60s
  TWAP reproduces 2,263 of 2,265 recorded outcomes.

## Quick start

```bash
pip install polars huggingface_hub
huggingface-cli download mileswangs/polymarket-btc-updown-5m-orderbook-tick-data --repo-type dataset --local-dir data
cd data && python ../examples/quickstart.py
```

[`examples/quickstart.py`](examples/quickstart.py) measures collection latency, loads one market's
order book events, and checks each market's outcome against the Chainlink TWAP. The same steps,
with charts, are in [`examples/quickstart.ipynb`](examples/quickstart.ipynb) and in a
[Kaggle notebook](https://www.kaggle.com/code/sumire2/polymarket-btc-up-down-5m-order-book-quick-start) that runs on the dataset directly.

For fill-level backtests with queue position and latency, use
[pm-hftbacktest](https://github.com/mileswangs/pm-hftbacktest). Across 547 BTC 5-minute markets,
its backtests [matched live trading in 95.32% of markets](https://pmdata.dev/research/polymarket-backtest-accuracy-95-32?utm_source=github&utm_medium=dataset&utm_campaign=btc5m-sample).

To read any other day, download it from the API instead of the sample files:

```python
import pandas as pd

url = "https://api.pmdata.dev/v1/polymarket/l2/2026/08/08/btc-updown-5m-1786147200.parquet"
df = pd.read_parquet(url, storage_options={"api_key": "<YOUR_API_KEY>", "User-Agent": "Mozilla/5.0"})
```

In the API's V1 Parquet files, L2 files of markets that resolved between 2026-08-07 and 2026-11-17, this sample's
dates included, mostly have no `market_resolved` event (Up/Down day ZIPs include it). To get the outcome of such a
market, use its final prices or Polymarket's Gamma API.

## License

Sample data: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), credit PMData. Code: MIT.
