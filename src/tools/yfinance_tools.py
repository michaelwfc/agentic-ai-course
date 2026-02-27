"""
- https://algotrading101.com/learn/yfinance-guide/
- https://ranaroussi.github.io/yfinance/index.html
- https://pypi.org/project/yfinance/

High granularity of data: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo



"""
import yfinance as yf


def get_stock_data(ticker="aapl"):
    """Get stock data from Yahoo Finance"""
    apple= yf.Ticker(ticker)

    # show actions (dividends, splits)
    apple.actions

    # show dividends
    apple.dividends

    # show splits
    apple.splits

    # + other methods etc.
    
    
    aapl_historical = aapl.history(start="2020-06-02", end="2020-06-07", interval="1m")
    aapl_historical

    return aapl_historical

