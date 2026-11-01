"""
Cash Efficiency Model - Step 10: gold parking with GLDM instead of GLD.

Why this step: the paper uses GLD as its gold ETF, but the Corex Halal
Portfolio (managed for Manzil) lists GLDM, SPDR Gold MiniShares, among
its possible holdings. GLDM holds the same physical gold as GLD but
charges a lower fee (0.10% a year vs 0.40%), so it should do slightly
better while the rule is parked in gold.

One variable changes: the gold ETF. Everything else is exactly step 8:
same rule, same dates, same costs, same purification, same
continue-don't-restart out-of-sample convention, same three scenarios.
No earlier file is modified.

The out-of-sample result for GLD was already seen in step 8, so this is
a robustness check on the instrument, not a new out-of-sample test.

Data: downloads GLDM into prices_gldm.csv the first time it runs
(prices.csv is not changed). Delete prices_gldm.csv to download again.

Requires prices.csv, dividends_hlal.csv, and: pip install yfinance pandas
"""

from pathlib import Path

import pandas as pd

from backtest import run_backtest
from load_data import END, START
from step2_buy_and_hold import find_start_date
from step6_tbill_comparison import BENCHMARK, comparison_table
from step8_final import (
    PERIODS,
    SCENARIOS,
    equity_from_positions,
    load_full_prices,
    measure_period,
    positions_from_signal_days,
    purify_full_period,
)

GLDM_FILE = "prices_gldm.csv"
GOLD_OPTIONS = {"GLD (paper)": "GLD", "GLDM (Corex holding)": "GLDM"}
BENCHMARK_LABEL = "T-bills (BIL, benchmark)"
RESULTS_FILE = Path("results") / "step10_gold_gldm.md"


# ---------- Data ----------

def load_gldm():
    path = Path(GLDM_FILE)
    if not path.exists():
        import yfinance as yf

        raw = yf.download("GLDM", start=START, end=END, auto_adjust=True, progress=False)
        series = raw["Close"]
        if isinstance(series, pd.DataFrame):
            series = series["GLDM"]
        series.rename("GLDM").to_frame().to_csv(path)
        print(f"Downloaded GLDM to {GLDM_FILE}")
    return pd.read_csv(path, index_col=0, parse_dates=True)["GLDM"]


def add_gldm(prices, gldm):
    """Put GLDM next to the other tickers and check it covers every day the rule can hold it."""
    combined = prices.copy()
    combined["GLDM"] = gldm.reindex(prices.index)
    return combined


def check_gldm(prices, start_day):
    window = prices.loc[start_day:]
    missing = window["GLDM"].isna().sum()
    if missing > 0:
        first_missing = window.index[window["GLDM"].isna()][0].date()
        raise ValueError(f"GLDM is missing {missing} days in the test period (first: {first_missing})")
    print(f"GLDM data: {window['GLDM'].first_valid_index().date()} to {window.index[-1].date()}, no missing days")


# ---------- Running versions ----------

def run_scenario(returns_prices, signal_hlal, first_signal_day, start_day, daily, cost):
    equities = {}
    hlal_held = returns_prices["HLAL"].loc[start_day:]
    equities["Buy-and-hold HLAL"] = (1 - cost) * hlal_held / hlal_held.iloc[0]

    versions = dict(GOLD_OPTIONS, **{BENCHMARK_LABEL: BENCHMARK})
    daily_signal_days = signal_hlal.loc[first_signal_day:].index
    for label, parking in versions.items():
        if daily:
            positions = positions_from_signal_days(signal_hlal, daily_signal_days, start_day, parking)
            equity = equity_from_positions(returns_prices, positions, cost)
        else:
            equity, _, _, _ = run_backtest(returns_prices, signal_hlal, first_signal_day, start_day, parking, cost)
        equities[f"Rule + {label}"] = equity
    return equities


def gold_gaps(results):
    benchmark = results[f"Rule + {BENCHMARK_LABEL}"]
    gld = results["Rule + GLD (paper)"]
    gldm = results["Rule + GLDM (Corex holding)"]
    return {
        "GLD minus T-bills": (gld["CAGR"] - benchmark["CAGR"], gld["Max drawdown"] - benchmark["Max drawdown"]),
        "GLDM minus T-bills": (gldm["CAGR"] - benchmark["CAGR"], gldm["Max drawdown"] - benchmark["Max drawdown"]),
        "GLDM minus GLD": (gldm["CAGR"] - gld["CAGR"], gldm["Max drawdown"] - gld["Max drawdown"]),
    }


def gap_lines(gaps):
    lines = ["| Comparison | Return gap per year (CAGR) | Drawdown gap (max drawdown) |", "| --- | --- | --- |"]
    lines += [f"| {name} | {ret:+.2%} | {dd:+.2%} |" for name, (ret, dd) in gaps.items()]
    return lines


# ---------- Output ----------

def write_results(all_results, all_gaps):
    RESULTS_FILE.parent.mkdir(exist_ok=True)
    lines = [
        "# Step 10: Gold parking with GLDM instead of GLD",
        "",
        "Only the gold ETF changes. Same rule, dates, costs, purification and out-of-sample convention as step 8.",
        "The GLD columns should match step 8 exactly; if they don't, something is wrong.",
        "",
        "Return gap: negative means the first option earned less. Drawdown gap: negative means a deeper drawdown.",
    ]
    for scenario in SCENARIOS:
        lines += ["", f"## {scenario}"]
        for period in PERIODS:
            lines += ["", f"### {period}", ""]
            lines += comparison_table(all_results[scenario][period])
            lines += [""]
            lines += gap_lines(all_gaps[scenario][period])
    RESULTS_FILE.write_text("\n".join(lines) + "\n")


def main():
    prices = load_full_prices()
    signal_hlal = prices["HLAL"].dropna()
    first_signal_day, start_day = find_start_date(signal_hlal)

    prices = add_gldm(prices, load_gldm())
    check_gldm(prices, start_day)

    purified = purify_full_period(prices, signal_hlal)
    tbill_returns = purified[BENCHMARK].pct_change()

    all_results, all_gaps = {}, {}
    for scenario, settings in SCENARIOS.items():
        equities = run_scenario(purified, signal_hlal, first_signal_day, start_day, settings["daily"], settings["cost"])
        all_results[scenario], all_gaps[scenario] = {}, {}
        for period in PERIODS:
            results = {name: measure_period(eq, tbill_returns, period) for name, eq in equities.items()}
            all_results[scenario][period] = results
            all_gaps[scenario][period] = gold_gaps(results)

    print("\nGLDM vs GLD, every scenario and period (CAGR difference per year):")
    for scenario in SCENARIOS:
        print(f"\n  {scenario}")
        for period in PERIODS:
            for name, (ret, dd) in all_gaps[scenario][period].items():
                print(f"    {period:14} {name:20} return {ret:+.2%}, drawdown {dd:+.2%}")

    write_results(all_results, all_gaps)
    print(f"\nFull tables saved to {RESULTS_FILE}")


if __name__ == "__main__":
    main()
