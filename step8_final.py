"""
Cash Efficiency Model - Step 8: final run, out-of-sample and robustness checks.

This is the one-time run of the locked out-of-sample period
(January 1, 2024 to September 30, 2026), done exactly as the spec says:

- The rule runs continuously from May 2020 to September 2026. The
  out-of-sample period is measured from the close of the last in-sample
  day (December 29, 2023), starting with whatever the rule held then.
  No restart, no new purchase (SPEC.md, section 4).
- All versions are purified (0.8% of HLAL's dividends), including the
  T-bill benchmark (SPEC.md, section 6).
- Robustness checks run on both periods and are all reported
  (SPEC.md, robustness checks):
    1. Main test: monthly signal, 0.10% per trade.
    2. Higher costs: monthly signal, 0.25% per trade.
    3. Daily signal: checked every trading day, 0.10% per trade.

The main test uses backtest.py exactly as in steps 3 to 7. The daily
signal needs a different set of signal days, so it is built here from
the same steps, and checked against backtest.py on monthly days.

Requires prices.csv (load_data.py) and dividends_hlal.csv (load_dividends.py).
"""

from pathlib import Path

import numpy as np
import pandas as pd

from backtest import CASH, EQUITY, count_trades, run_backtest
from metrics import format_value, summarize
from step2_buy_and_hold import COST_PER_TRADE, IN_SAMPLE_END, PRICES_FILE, SMA_DAYS, find_start_date
from step6_tbill_comparison import BENCHMARK, HALAL_OPTIONS, TABLE_METRICS, comparison_table, gap_table
from step7_purification import DIVIDENDS_FILE, PURIFICATION_RATE, gaps_against_benchmark

OUT_OF_SAMPLE_START = "2024-01-01"
OUT_OF_SAMPLE_END = "2026-09-30"
HIGH_COST_PER_TRADE = 0.0025
RESULTS_FILE = Path("results") / "step8_final.md"

SCENARIOS = {
    "Main test (monthly signal, 0.10% costs)": {"daily": False, "cost": COST_PER_TRADE},
    "Robustness: higher costs (monthly signal, 0.25% costs)": {"daily": False, "cost": HIGH_COST_PER_TRADE},
    "Robustness: daily signal (0.10% costs)": {"daily": True, "cost": COST_PER_TRADE},
}
PERIODS = ["In-sample", "Out-of-sample"]


# ---------- Data ----------

def load_full_prices():
    prices = pd.read_csv(PRICES_FILE, index_col=0, parse_dates=True)
    return prices.loc[:OUT_OF_SAMPLE_END]


def purify_full_period(prices, hlal):
    """Same purification as step 7, applied to the full period."""
    data = pd.read_csv(DIVIDENDS_FILE, index_col=0, parse_dates=True).loc[:OUT_OF_SAMPLE_END]
    dividend_yield = data["dividend"] / data["raw_close"].shift(1)
    drag = (PURIFICATION_RATE * dividend_yield).fillna(0.0)

    missing = drag[drag > 0].index.difference(hlal.index)
    if len(missing) > 0:
        raise ValueError(f"Dividend dates not found in prices.csv: {list(missing.date)}")

    drag = drag.reindex(hlal.index, fill_value=0.0)
    purified = prices.copy()
    purified.loc[hlal.index, "HLAL"] = hlal * (1 - drag).cumprod()
    return purified


# ---------- Daily-signal rule (same steps as backtest.py, every trading day) ----------

def positions_from_signal_days(hlal, signal_days, start_day, parking):
    sma = hlal.rolling(SMA_DAYS).mean()
    days = hlal.loc[start_day:].index
    positions = pd.Series(np.nan, index=days, dtype=object)

    for signal_day in signal_days:
        next_position = hlal.index.get_loc(signal_day) + 1
        if next_position >= len(hlal.index):
            continue
        execution_day = hlal.index[next_position]
        positions.loc[execution_day] = EQUITY if hlal.loc[signal_day] > sma.loc[signal_day] else parking

    return positions.ffill()


def equity_from_positions(prices, positions, cost_per_trade):
    days = positions.index
    daily_returns = prices.loc[days].pct_change()
    daily_returns[CASH] = 0.0

    held_yesterday = positions.shift(1)
    asset_returns = pd.Series(0.0, index=days)
    for asset in held_yesterday.dropna().unique():
        on_asset = held_yesterday == asset
        asset_returns[on_asset] = daily_returns.loc[on_asset, asset]

    previous = [None] + list(positions.iloc[:-1])
    trades = pd.Series([count_trades(old, new) for old, new in zip(previous, positions)], index=days)
    return ((1 + asset_returns) * (1 - cost_per_trade * trades)).cumprod()


# ---------- Running versions ----------

def run_scenario(returns_prices, signal_hlal, first_signal_day, start_day, daily, cost):
    equities = {}

    hlal_held = returns_prices["HLAL"].loc[start_day:]
    equities["Buy-and-hold HLAL"] = (1 - cost) * hlal_held / hlal_held.iloc[0]

    daily_signal_days = signal_hlal.loc[first_signal_day:].index
    versions = dict(HALAL_OPTIONS, **{"T-bills (BIL, benchmark)": BENCHMARK})
    for label, parking in versions.items():
        if daily:
            positions = positions_from_signal_days(signal_hlal, daily_signal_days, start_day, parking)
            equity = equity_from_positions(returns_prices, positions, cost)
        else:
            equity, _, _, _ = run_backtest(returns_prices, signal_hlal, first_signal_day, start_day, parking, cost)
        equities[f"Rule + {label}"] = equity

    return equities


def measure_period(equity, tbill_returns, period):
    if period == "In-sample":
        return summarize(equity.loc[:IN_SAMPLE_END], tbill_returns)
    last_in_sample_day = equity.loc[:IN_SAMPLE_END].index[-1]
    segment = equity.loc[last_in_sample_day:]
    return summarize(segment, tbill_returns, initial_capital=segment.iloc[0])


def out_of_sample_switches(signal_hlal, first_signal_day, start_day, returns_prices):
    _, positions, _, _ = run_backtest(returns_prices, signal_hlal, first_signal_day, start_day, CASH, COST_PER_TRADE)
    held_at_start = positions.loc[:IN_SAMPLE_END].iloc[-1]
    oos = positions.loc[OUT_OF_SAMPLE_START:]
    switches = oos[oos != oos.shift(1).fillna(held_at_start)]
    parked_share = (oos != EQUITY).mean()
    return held_at_start, switches, parked_share


# ---------- Output ----------

def describe(asset):
    return "HLAL" if asset == EQUITY else "parking option"


def write_results(all_results, all_gaps, held_at_start, switches, parked_share):
    RESULTS_FILE.parent.mkdir(exist_ok=True)
    lines = [
        "# Step 8: Final run, out-of-sample and robustness checks",
        "",
        "Out-of-sample: January 1, 2024 to September 30, 2026, run once. Measured from the close of the last "
        "in-sample day, continuing the rule's position. All versions purified (0.8% of HLAL dividends).",
        "",
        "Return gap: negative means the halal option earned less than T-bills. "
        "Drawdown gap: negative means a deeper drawdown than T-bills.",
    ]
    for scenario in SCENARIOS:
        lines += ["", f"## {scenario}"]
        for period in PERIODS:
            lines += ["", f"### {period}", ""]
            lines += comparison_table(all_results[scenario][period])
            lines += ["", "Gap: each halal option minus the T-bill version", ""]
            lines += gap_table(all_gaps[scenario][period])

    lines += [
        "",
        "## Out-of-sample switch log (main test)",
        "",
        f"Held at the start of 2024: {describe(held_at_start)}. Share of out-of-sample days parked: {parked_share:.2%}.",
        "",
        "| Trade date | Now holding |",
        "| --- | --- |",
    ]
    lines += [f"| {day.date()} | {describe(asset)} |" for day, asset in switches.items()]
    RESULTS_FILE.write_text("\n".join(lines) + "\n")


def main():
    prices = load_full_prices()
    signal_hlal = prices["HLAL"].dropna()
    first_signal_day, start_day = find_start_date(signal_hlal)
    purified = purify_full_period(prices, signal_hlal)
    tbill_returns = purified[BENCHMARK].pct_change()

    all_results, all_gaps = {}, {}
    for scenario, settings in SCENARIOS.items():
        equities = run_scenario(purified, signal_hlal, first_signal_day, start_day, settings["daily"], settings["cost"])
        all_results[scenario], all_gaps[scenario] = {}, {}
        for period in PERIODS:
            results = {name: measure_period(eq, tbill_returns, period) for name, eq in equities.items()}
            all_results[scenario][period] = results
            all_gaps[scenario][period] = gaps_against_benchmark(results)

    held_at_start, switches, parked_share = out_of_sample_switches(signal_hlal, first_signal_day, start_day, purified)

    main_scenario = list(SCENARIOS)[0]
    print("MAIN TEST, OUT-OF-SAMPLE (Jan 2024 - Sep 2026):")
    for name, stats in all_results[main_scenario]["Out-of-sample"].items():
        summary = ", ".join(f"{m} {format_value(m, stats[m])}" for m in TABLE_METRICS[:3])
        print(f"  {name:33} {summary}")

    print("\nTHE GAP (halal option minus T-bill version), every scenario and period:")
    for scenario in SCENARIOS:
        print(f"\n  {scenario}")
        for period in PERIODS:
            for label, gap in all_gaps[scenario][period].items():
                print(
                    f"    {period:14} {label:14} return {gap['Return gap per year (CAGR)']:+.2%} per year, "
                    f"drawdown {gap['Drawdown gap (max drawdown)']:+.2%}"
                )

    print(f"\nOut-of-sample: held {describe(held_at_start)} at the start of 2024, parked {parked_share:.2%} of days")
    for day, asset in switches.items():
        print(f"  {day.date()}  now holding {describe(asset)}")

    write_results(all_results, all_gaps, held_at_start, switches, parked_share)
    print(f"\nFull tables saved to {RESULTS_FILE}")


if __name__ == "__main__":
    main()