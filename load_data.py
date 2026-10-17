"""
Cash Efficiency Model - Step 1: load and check the data.

Downloads daily prices for the four instruments in the spec and checks
that the data is clean. No strategy, no results yet.

Prices are adjusted for dividends (auto_adjust=True), so they measure
total return, not just price change.

Requires: pip install yfinance pandas
"""

import pandas as pd
import yfinance as yf

TICKERS = ["HLAL", "SPSK", "GLD", "BIL"]
START = "2019-07-01"  # a little before HLAL's first trading day (July 15, 2019)
END = "2026-10-01"    # yfinance excludes the end date, so data stops at Sep 30, 2026
OUTPUT_FILE = "prices.csv"


def download_prices():
    raw = yf.download(TICKERS, start=START, end=END, auto_adjust=True, progress=False)
    prices = raw["Close"][TICKERS]
    return prices


def check_prices(prices):
    print(f"Total rows: {len(prices)}\n")

    print("First and last date per ticker:")
    for ticker in TICKERS:
        series = prices[ticker].dropna()
        print(f"  {ticker}: {series.index[0].date()} to {series.index[-1].date()} ({len(series)} days)")

    print("\nMissing values after each ticker's first date (should be 0):")
    for ticker in TICKERS:
        series = prices[ticker]
        first_date = series.first_valid_index()
        missing = series.loc[first_date:].isna().sum()
        print(f"  {ticker}: {missing}")

    print("\nLargest one-day move per ticker (to spot bad data):")
    for ticker in TICKERS:
        daily_change = prices[ticker].dropna().pct_change().abs()
        worst_day = daily_change.idxmax()
        print(f"  {ticker}: {daily_change.max():.2%} on {worst_day.date()}")


def main():
    prices = download_prices()
    prices.to_csv(OUTPUT_FILE)
    print(f"Saved to {OUTPUT_FILE}\n")
    check_prices(prices)


if __name__ == "__main__":
    main()