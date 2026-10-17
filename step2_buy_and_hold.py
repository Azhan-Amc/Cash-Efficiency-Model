"""
Cash Efficiency Model - Step 2: buy-and-hold baseline (in-sample only).

Buys HLAL once and holds it. This is the reference every rule version
will be compared against.

To keep the comparison fair, the baseline starts on the same day the
rule versions will start: the trading day after the first month-end
where HLAL's 200-day average exists (SPEC.md, section 4). It pays the
same 0.10% cost for its one purchase.

Only in-sample data is used (up to December 31, 2023). The out-of-sample
period stays locked.

Requires prices.csv from load_data.py.
"""

from pathlib import Path

import pandas as pd

from metrics import format_value, summarize

PRICES_FILE = "prices.csv"
IN_SAMPLE_END = "2023-12-31"
SMA_DAYS = 200
COST_PER_TRADE = 0.0010
RESULTS_FILE = Path("results") / "step2_buy_and_hold.md"


def load_in_sample_prices():
    prices = pd.read_csv(PRICES_FILE, index_col=0, parse_dates=True)
    return prices.loc[:IN_SAMPLE_END]


def month_end_trading_days(index):
    periods = index.to_series().dt.to_period("M")
    is_last_day_of_month = periods != periods.shift(-1)
    return index[is_last_day_of_month.values]


def find_start_date(hlal):
    sma = hlal.rolling(SMA_DAYS).mean()
    valid_month_ends = [day for day in month_end_trading_days(hlal.index) if pd.notna(sma.loc[day])]
    first_signal_day = valid_month_ends[0]
    next_position = hlal.index.get_loc(first_signal_day) + 1
    return first_signal_day, hlal.index[next_position]


def write_results(first_signal_day, stats):
    RESULTS_FILE.parent.mkdir(exist_ok=True)
    lines = [
        "# Step 2: Buy-and-hold HLAL (in-sample)",
        "",
        f"First valid 200-day signal: {first_signal_day.date()}",
        "",
        "| Metric | Value |",
        "| --- | --- |",
    ]
    lines += [f"| {name} | {format_value(name, value)} |" for name, value in stats.items()]
    RESULTS_FILE.write_text("\n".join(lines) + "\n")


def main():
    prices = load_in_sample_prices()
    hlal = prices["HLAL"].dropna()

    first_signal_day, start_day = find_start_date(hlal)

    hlal_held = hlal.loc[start_day:]
    equity = (1 - COST_PER_TRADE) * hlal_held / hlal_held.iloc[0]

    tbill_returns = prices["BIL"].pct_change()
    stats = summarize(equity, tbill_returns)

    print(f"First valid 200-day signal: {first_signal_day.date()}")
    print(f"Buy-and-hold starts:        {start_day.date()}\n")
    for name, value in stats.items():
        print(f"{name:28} {format_value(name, value)}")

    write_results(first_signal_day, stats)
    print(f"\nSaved to {RESULTS_FILE}")


if __name__ == "__main__":
    main()