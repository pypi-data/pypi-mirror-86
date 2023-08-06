## Stocks Rider

Find anomalies in Stock market.

![](docs/stockridertips-banner.png)

A live version of this is running as a bot on [StockRiderTips](https://www.reddit.com/r/StockRiderTips) sub-reddit.

![](docs/stockridertips-post.png)

### Installation

```bash
pip install stock-rider
```

Then copy `env.cfg.sample` to `env.cfg` and populate values.

### Using Stocks Rider

*Populate data*

```bash
stock-rider populate-data --period 6mo --interval 1d
```

*Run analysis*

```bash
# High Volume analysis
stock-rider volume-analysis

# Gains/Losses
stock-rider gainers-losers
```

### Publishing

Increment version in setup.py
Publish with `make package`

### License

[MIT](https://choosealicense.com/licenses/mit/)
