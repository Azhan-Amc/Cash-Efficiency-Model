"""
Cash Efficiency Model - Step 6: T-bill benchmark and the gap (in-sample only).

Runs the same 200-day rule parking in T-bills (BIL), which conventional
investors can use but halal investors cannot. BIL is a benchmark only:
it is never held in a halal portfolio.

Then measures the gap between each halal parking option (0% cash, GLD,
SPSK) and the T-bill version. This gap answers the research question
(SPEC.md, section 1).

All versions use the same rule (backtest.py) and the same metrics
(metrics.py), so the cash, gold and sukuk numbers are identical to
steps 3 to 5.

Only in-sample data is used (up to December 31, 2023).

Requires prices.csv from load_data.py.
"""

from pathlib import Path

from backtest import CASH, run_backtest
from metrics import format_value, summarize
from step2_buy_and_hold import COST_PER_TRADE, find_start_date, load_in_sample_prices

BENCHMARK = "BIL"
HALAL_OPTIONS = {"0% cash": CASH, "GLD (gold)": "GLD", "SPSK (sukuk)": "SPSK"}
TABLE_METRICS = ["CAGR", "Volatility", "Max drawdown", "Sharpe (risk-free 0%)", "Sharpe (risk-free T-bill)", "Calmar"]
RESULTS_FILE = Path("results") / "step6_tbill_comparison.md"


def run_all_versions(prices, hlal, first_signal_day, start_day):
    tbill_returns = prices[BENCHMARK].pct_change()
    results = {}

    hlal_held = hlal.loc[start_day:]
    buy_and_hold = (1 - COST_PER_TRADE) * hlal_held / hlal_held.iloc[0]
    results["Buy-and-hold HLAL"] = summarize(buy_and_hold, tbill_returns)

    versions = dict(HALAL_OPTIONS, **{"T-bills (BIL, benchmark)": BENCHMARK})
    for label, parking in versions.items():
        equity, _, _, _ = run_backtest(prices, hlal, first_signal_day, start_day, parking, COST_PER_TRADE)
        results[f"Rule + {label}"] = summarize(equity, tbill_returns)

    return results


def compute_gaps(results):
    benchmark = results["Rule + T-bills (BIL, benchmark)"]
    gaps = {}
    for label in HALAL_OPTIONS:
        version = results[f"Rule + {label}"]
        gaps[label] = {
            "Return gap per year (CAGR)": version["CAGR"] - benchmark["CAGR"],
            "Drawdown gap (max drawdown)": version["Max drawdown"] - benchmark["Max drawdown"],
        }
    return gaps


def comparison_table(results):
    names = list(results)
    lines = ["| Metric | " + " | ".join(names) + " |", "| --- |" + " --- |" * len(names)]
    for metric in TABLE_METRICS:
        values = [format_value(metric, results[name][metric]) for name in names]
        lines.append(f"| {metric} | " + " | ".join(values) + " |")
    return lines


def gap_table(gaps):
    lines = [
        "| Halal option | Return gap per year (CAGR) | Drawdown gap (max drawdown) |",
        "| --- | --- | --- |",
    ]
    for label, gap in gaps.items():
        lines.append(
            f"| {label} | {gap['Return gap per year (CAGR)']:+.2%} | {gap['Drawdown gap (max drawdown)']:+.2%} |"
        )
    return lines


def write_results(results, gaps):
    RESULTS_FILE.parent.mkdir(exist_ok=True)
    lines = ["# Step 6: T-bill benchmark and the gap (in-sample)", "", "## All versions", ""]
    lines += comparison_table(results)
    lines += [
        "",
        "## The gap: each halal option minus the T-bill version",
        "",
        "Return gap: negative means the halal option earned less than T-bills.",
        "Drawdown gap: negative means a deeper drawdown than T-bills; positive means better protection.",
        "",
    ]
    lines += gap_table(gaps)
    RESULTS_FILE.write_text("\n".join(lines) + "\n")


def main():
    prices = load_in_sample_prices()
    hlal = prices["HLAL"].dropna()
    first_signal_day, start_day = find_start_date(hlal)

    results = run_all_versions(prices, hlal, first_signal_day, start_day)
    gaps = compute_gaps(results)

    print("All versions:")
    for name, stats in results.items():
        summary = ", ".join(f"{metric} {format_value(metric, stats[metric])}" for metric in TABLE_METRICS[:3])
        print(f"  {name:33} {summary}")

    print("\nThe gap (halal option minus T-bill version):")
    for label, gap in gaps.items():
        print(
            f"  {label:14} return {gap['Return gap per year (CAGR)']:+.2%} per year, "
            f"drawdown {gap['Drawdown gap (max drawdown)']:+.2%}"
        )

    write_results(results, gaps)
    print(f"\nSaved to {RESULTS_FILE}")


if __name__ == "__main__":
    main()