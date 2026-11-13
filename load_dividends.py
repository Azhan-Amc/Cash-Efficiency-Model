"""
Cash Efficiency Model - Purification data: HLAL dividends.

Downloads HLAL's dividend history and its unadjusted closing prices,
which are needed to turn each dividend into a percentage. prices.csv
only has dividend-adjusted prices, so this is a separate file.

Saves dividends_hlal.csv with, for each trading day:
- raw_close: unadjusted closing price
- dividend: dividend per share paid on that ex-dividend day (0 otherwise)

Requires: pip install yfinance pandas
"""

import yfinance as yf

from load_data import END, START

TICKER = "HLAL"
OUTPUT_FILE = "dividends_hlal.csv"


def download_dividends():
    history = yf.Ticker(TICKER).history(start=START, end=END, auto_adjust=False)
    history.index = history.index.tz_localize(None).normalize()
    data = history[["Close", "Dividends"]].rename(columns={"Close": "raw_close", "Dividends": "dividend"})
    data.index.name = "Date"
    return data


def main():
    data = download_dividends()
    data.to_csv(OUTPUT_FILE)

    paid = data[data["dividend"] > 0]
    print(f"Saved to {OUTPUT_FILE}")
    print(f"Trading days: {len(data)}, from {data.index[0].date()} to {data.index[-1].date()}")
    print(f"Dividends found: {len(paid)}\n")
    for day, row in paid.iterrows():
        print(f"  {day.date()}  ${row['dividend']:.4f} per share")


if __name__ == "__main__":
    main()