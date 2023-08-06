import click

from krider.stock_store import stock_store
from krider.tasks.ema_cross_over import ema_cross_over_task
from krider.tasks.gainers_losers import gainers_losers_task
from krider.tasks.historical_data_downloader import historical_data_downloader
from krider.tasks.volume_analysis import volume_analysis_task
from krider.utils.log_helper import init_logger

init_logger()


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--period",
    help="Use periods to download data. Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max",
    default="1mo",
    required=False,
)
@click.option(
    "--interval",
    help="Data interval. 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo",
    required=True,
    default="60m",
)
@click.option(
    "--stocks",
    help="Download historical data and fill gaps for provided list of stocks. Eg. MSFT,TSLA,AAPL",
)
@click.option("--datadir", help="Directory to store database file", default=".")
def populate_data(interval, period, stocks, datadir):
    stock_store.init_database(datadir)
    result = historical_data_downloader.run_with(interval, period, stocks)
    click.echo(result, nl=False)


@cli.command()
@click.option(
    "--stocks", help="Run analysis on provided list of stocks. Eg. MSFT,TSLA,AAPL",
)
@click.option("--datadir", help="Directory to load database file", default=".")
def volume_analysis(stocks, datadir):
    stock_store.init_database(datadir)
    result = volume_analysis_task.run_with(stocks)
    click.echo(result, nl=False)


@cli.command()
@click.option(
    "--minvol", default=20000, help="Minimum Volume when checking for Gains/Losses",
)
@click.option(
    "--stocks", help="Run analysis on provided list of stocks. Eg. MSFT,TSLA,AAPL",
)
@click.option("--datadir", help="Directory to load database file", default=".")
def gainers_losers(stocks, minvol, datadir):
    stock_store.init_database(datadir)
    result = gainers_losers_task.run_with(minvol, stocks)
    click.echo(result, nl=False)


@cli.command()
@click.option(
    "--ema", default=200, help="EMA",
)
@click.option(
    "--stocks", help="Run analysis on provided list of stocks. Eg. MSFT,TSLA,AAPL",
)
@click.option(
    "--price-filter",
    default=10,
    help="Filter out any stocks with closing price less than this value",
)
@click.option(
    "--volume-filter",
    default=1000000,
    help="Filter out any stocks with closing volume less than this value",
)
@click.option("--datadir", help="Directory to load database file", default=".")
def ema_cross_over(stocks, price_filter, volume_filter, ema, datadir):
    stock_store.init_database(datadir)
    result = ema_cross_over_task.run_with(ema, price_filter, volume_filter, stocks)
    click.echo(result, nl=False)

