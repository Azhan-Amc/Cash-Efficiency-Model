"""
Cash Efficiency Model - Step 7: purification (in-sample only).

Reruns every version with HLAL's dividends reduced by the purification
amount (SPEC.md, section 6).

Purification estimate: 0.8% of each dividend is donated, from a
third-party screening estimate of HLAL's impermissible income. It is an
estimate, not Wahed's published figure.

How it is applied:
- On each ex-dividend day, HLAL's return is reduced by
  0.8% x (dividend / previous unadjusted close).
- Only while HLAL is held, since the backtest only earns HLAL's
  returns on days it holds HLAL.
- The 200-day signal still uses the market price of HLAL, unchanged.
- Every version is purified, including the T-bill benchmark, so the gap
  still measures only the parking choice.

Only in-sample data is used (up to December 31, 2023).

Requires prices.csv (load_data.py) and dividends_hlal.csv (load_dividends.py).
"""

from pathlib import Path

import pandas as pd

from backtest import run_backtest
from metrics import format_value, summarize
from step2_buy_and_hold import COST_PER_TRADE, IN_SAMPLE_END, find_start_date, load_in_sample_prices
from step6_tbill_comparison import BENCHMARK, HALAL_OPTIONS, TABLE_METRICS, comparison_table, gap_table

PURIFICATION_RATE = 0.008
DIVIDENDS_FILE = "dividends_hlal.csv"
RESULTS_FILE = Path("results") / "step7_purification.md"


def purification_drag(hlal_index):
    """Daily fraction of HLAL's value donated (non-zero only on ex-dividend days)."""
    data = pd.read_csv(DIVIDENDS_FILE, index_col=0, parse_dates=True).loc[:IN_SAMPLE_END]
    dividend_yield = data["dividend"] / data["raw_close"].shift(1)
    drag = (PURIFICATION_RATE * dividend_yield).fillna(0.0)

    paid_days = drag[drag > 0].index
    missing = paid_days.difference(hlal_index)
    if len(missing) > 0:
        raise ValueError(f"Dividend dates not found in prices.csv: {list(missing.date)}")

    return drag.reindex(hlal_index, fill_value=0.0), len(paid_days)


def purified_prices(prices, hlal):
    drag, dividend_count = purification_drag(hlal.index)
    purified = prices.copy()
    purified.loc[hlal.index, "HLAL"] = hlal * (1 - drag).cumprod()
    return purified, drag, dividend_count


def run_versions(returns_prices, signal_hlal, first_signal_day, start_day):
    tbill_returns = returns_prices[BENCHMARK].pct_change()
    results = {}

    hlal_held = returns_prices["HLAL"].loc[start_day:]
    buy_and_hold = (1 - COST_PER_TRADE) * hlal_held / hlal_held.iloc[0]
    results["Buy-and-hold HLAL"] = summarize(buy_and_hold, tbill_returns)

    versions = dict(HALAL_OPTIONS, **{"T-bills (BIL, benchmark)": BENCHMARK})
    for label, parking in versions.items():
        equity, _, _, _ = run_backtest(returns_prices, signal_hlal, first_signal_day, start_day, parking, COST_PER_TRADE)
        results[f"Rule + {label}"] = summarize(equity, tbill_returns)

    return results


def gaps_against_benchmark(results):
    benchmark = results["Rule + T-bills (BIL, benchmark)"]
    return {
        label: {
            "Return gap per year (CAGR)": results[f"Rule + {label}"]["CAGR"] - benchmark["CAGR"],
            "Drawdown gap (max drawdown)": results[f"Rule + {label}"]["Max drawdown"] - benchmark["Max drawdown"],
        }
        for label in HALAL_OPTIONS
    }


def write_results(before, after, gaps, dividend_count, total_drag):
    RESULTS_FILE.parent.mkdir(exist_ok=True)
    lines = [
        "# Step 7: Purification (in-sample)",
        "",
        f"Purification rate: {PURIFICATION_RATE:.1%} of each HLAL dividend (estimate, not Wahed's published figure).",
        f"HLAL dividends from July 2019 to December 2023: {dividend_count}. Total purification while always holding HLAL: {total_drag:.4%} of value.",
        "",
        "## CAGR before and after purification",
        "",
        "| Version | Before | After | Difference |",
        "| --- | --- | --- | --- |",
    ]
    for name in before:
        b, a = before[name]["CAGR"], after[name]["CAGR"]
        lines.append(f"| {name} | {b:.2%} | {a:.2%} | {a - b:+.4%} |")
    lines += ["", "## All versions, after purification", ""]
    lines += comparison_table(after)
    lines += ["", "## The gap after purification: each halal option minus the T-bill version", ""]
    lines += gap_table(gaps)
    RESULTS_FILE.write_text("\n".join(lines) + "\n")


def main():
    prices = load_in_sample_prices()
    hlal = prices["HLAL"].dropna()
    first_signal_day, start_day = find_start_date(hlal)

    purified, drag, dividend_count = purified_prices(prices, hlal)
    total_drag = 1 - (1 - drag.loc[start_day:]).prod()

    before = run_versions(prices, hlal, first_signal_day, start_day)
    after = run_versions(purified, hlal, first_signal_day, start_day)
    gaps = gaps_against_benchmark(after)

    print(f"HLAL dividends from July 2019 to December 2023: {dividend_count}")
    print(f"Total purification while always holding HLAL: {total_drag:.4%}\n")
    print("CAGR before -> after purification:")
    for name in before:
        b, a = before[name]["CAGR"], after[name]["CAGR"]
        print(f"  {name:33} {b:.2%} -> {a:.2%}  ({a - b:+.4%})")

    print("\nThe gap after purification (halal option minus T-bill version):")
    for label, gap in gaps.items():
        print(
            f"  {label:14} return {gap['Return gap per year (CAGR)']:+.2%} per year, "
            f"drawdown {gap['Drawdown gap (max drawdown)']:+.2%}"
        )

    write_results(before, after, gaps, dividend_count, total_drag)
    print(f"\nSaved to {RESULTS_FILE}")


if __name__ == "__main__":
    main()