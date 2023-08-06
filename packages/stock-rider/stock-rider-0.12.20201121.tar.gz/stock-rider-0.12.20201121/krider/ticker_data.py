from pathlib import Path

import pandas as pd
from pandas import DataFrame


class TickerData:
    def __init__(self):
        self.exchanges = [
            ("nasdaq", "nasdaq-listed.csv"),
            ("amex", "amex-listed.csv"),
            ("nyse", "nyse-listed.csv"),
        ]

    def load_exchange_tickers_or_given_stocks(self, stocks) -> DataFrame:
        exchange_securities = [s for s in self._extract_data(self.exchanges)]
        exchange_tickers = pd.concat(exchange_securities)

        if stocks:
            selected_stocks = stocks.split(",")
            exchange_tickers = exchange_tickers[
                exchange_tickers.index.isin(selected_stocks)
            ]

        return exchange_tickers

    def _extract_data(self, exchanges):
        for exchange, data_file in exchanges:
            df = self._load_from("data/{}".format(data_file))
            df["exchange"] = exchange
            yield df

    def _load_from(self, listing_path):
        securities_file = Path.cwd().joinpath(listing_path)
        return pd.read_csv(securities_file, index_col=["Symbol"])


ticker_data = TickerData()
