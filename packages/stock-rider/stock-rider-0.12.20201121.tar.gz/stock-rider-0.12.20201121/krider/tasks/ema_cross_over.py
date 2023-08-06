import logging

import numpy as np
import pandas as pd
from pandas import DataFrame
from tqdm import tqdm

from krider.bot_config import config
from krider.notifications.console_notifier import console_notifier
from krider.stock_store import stock_store
from krider.ticker_data import ticker_data
from krider.utils.report_generator import report_generator
from krider.utils.timing_decorator import timeit

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)


class EmaCrossOverTask:
    @timeit
    def run_with(self, ema, price_filter, volume_filter, stocks=None):
        exchange_tickers: DataFrame = ticker_data.load_exchange_tickers_or_given_stocks(
            stocks
        )

        collective_post = []

        for ticker, ticker_df in tqdm(
            exchange_tickers.iterrows(), desc=f"Running ema {ema} cross-over"
        ):
            logging.debug("Running analysis on {}".format(ticker))
            selected_data = stock_store.data_for_ticker(ticker)
            if selected_data.empty:
                continue

            mean_volume = np.mean(selected_data.tail(n=10)["volume"])

            prev_session_data = selected_data[
                [
                    "datetime",
                    "exchange",
                    "close",
                    "volume",
                    self._close_ema(ema),
                    self._close_xd_ema(ema),
                ]
            ].iloc[-1]

            if self._indicator_found(
                ema, mean_volume, price_filter, volume_filter, prev_session_data
            ):
                body = self._output_body(ema, prev_session_data)
                report = report_generator.prepare_output(
                    ticker, prev_session_data, body
                )
                collective_post.append(report)

        logging.info(
            "Total {} stocks found with price near {} EMA ".format(
                len(collective_post), ema
            )
        )

        if collective_post:
            content = dict(
                title="[Daily] Closing near {} EMA".format(ema),
                flair_id=config("EMA_CROSSOVER"),
                body=report_generator.wrap_in_banner(collective_post),
            )
            console_notifier.send_notification(content)
        return "All done"

    def _output_body(self, ema, df: DataFrame):
        close = df["close"]
        close_200_sma = df[self._close_ema(ema)]
        return """Close ({:.2f}) closing near {} EMA ({:.2f})""".format(
            close, ema, close_200_sma
        )

    def _indicator_found(
        self, ema, mean_volume, price_filter, volume_filter, df: DataFrame
    ):
        return (
            df["volume"] > mean_volume
            and df[self._close_xd_ema(ema)]
            and df["close"] > price_filter
            and df["volume"] > volume_filter
        )

    def _close_ema(self, ema):
        return "close_{}_ema".format(ema)

    def _close_xd_ema(self, ema):
        return "close_xd_close_{}_ema".format(ema)


ema_cross_over_task = EmaCrossOverTask()
