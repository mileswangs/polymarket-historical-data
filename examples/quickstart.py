"""Quick start for the Polymarket BTC Up/Down 5m dataset. Run from the dataset directory."""
import polars as pl

l2 = pl.scan_parquet("l2/*/*.parquet")
markets = pl.read_parquet("markets.parquet")

# 1. Collection latency: receive time minus Polymarket event time, on price changes.
latency_ms = (
    l2.filter(pl.col("event_type") == "price_change")
    .select(((pl.col("local_timestamp") - pl.col("timestamp")).dt.total_microseconds() / 1000).alias("ms"))
    .collect()
)
print(latency_ms.describe())

# 2. Rebuild one market's book at any moment: start from the last `book` snapshot,
#    then apply each `price_change` (pc_size = new total size at pc_price, 0 removes it).
slug = markets["market_slug"][144]
events = l2.filter(pl.col("market_slug") == slug).collect()

# 3. Reproduce the outcome from Chainlink 60s TWAP: Up wins if the TWAP at the end of the
#    window is at least the TWAP at the start. Use the last report at or before each time.
twap = (
    pl.read_parquet("chainlink_streams_twap60s/*/*.parquet")
    .select("observationsTimestamp", (pl.col("price").cast(pl.Float64) / 1e18).alias("twap"))
    .unique("observationsTimestamp", keep="last")
    .sort("observationsTimestamp")
)
m = markets.with_columns(
    pl.col("start_time").dt.replace_time_zone(None),
    pl.col("end_time").dt.replace_time_zone(None),
)
for col in ["start_time", "end_time"]:
    m = m.sort(col).join_asof(
        twap.rename({"observationsTimestamp": f"{col}_obs", "twap": f"{col}_twap"}),
        left_on=col, right_on=f"{col}_obs", strategy="backward",
    )
m = m.with_columns(
    pl.when(pl.col("end_time_twap") >= pl.col("start_time_twap")).then(pl.lit("yes")).otherwise(pl.lit("no")).alias("twap_outcome")
)
m = m.filter(pl.col("winning_outcome").is_not_null())
print(m.group_by(pl.col("start_time").dt.date()).agg((pl.col("twap_outcome") == pl.col("winning_outcome")).mean().alias("match")).sort("start_time"))
