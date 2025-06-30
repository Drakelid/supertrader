"""Helpers for fetching market data from Binance."""

import pandas as pd
from binance import Client

class HistoricalData:
    """Fetch historical candlestick data."""

    def __init__(self, api_key: str, api_secret: str) -> None:
        self.client = Client(api_key, api_secret)

    def get_historical_klines(self, symbol: str, interval: str, start: str, end: str) -> pd.DataFrame:
        """Return a DataFrame of historical klines."""

        klines = self.client.get_historical_klines(symbol, interval, start, end)
        df = pd.DataFrame(klines, columns=[
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base", "taker_buy_quote", "ignore"
        ])
        df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
        df.set_index("open_time", inplace=True)
        return df.astype(float)
