"""
Cash Efficiency Model - Step 11: purification at Wahed's published rate.

Why this step: step 7 and step 8 purify 0.8% of each HLAL dividend. That
was an estimate from a third-party page, and the audit found the source
unstable. Wahed publishes its own figures for HLAL, on the fund page
(wahed.com/hlal, "Quarterly Purification on HLAL Dividends", file as of
June 30, 2026). For every dividend from 2019 to Q2 2026, the purification
amount is exactly 5% of the dividend per share.

One variable changes: the purification rate, 0.8% -> 5%. Everything else
is exactly step 8 (same rule, dates, costs, scenarios, out-of-sample
convention). Step 8's rate is swapped only inside this script while it
runs.

Results already seen in step 8, so this is a correction of an input,
not a new out-of-sample test.

Requires prices.csv and dividends_hlal.csv.
"""

from pathlib import Path

import step8_final
from step2_buy_and_hold import find_start_date
from step6_tbill_comparison import BENCHMARK, comparison_table, gap_table
from step7_purification import gaps_against_benchmark
from step8_final import PERIODS, SCENARIOS, load_full_prices, measure_period, run_scenario

OLD_RATE = 0.008   # third-party estimate used in steps 7 and 8
NEW_RATE = 0.05    # Wahed's published figure: 5% of every HLAL dividend
RESULTS_FILE = Path("results") / "step11_purification_wahed.md"


def run_all(rate):
    """Step 8's full set of results, with the purification rate set to `rate`."""
    step8_final.PURIFICATION_RATE = rate
    prices = load_full_prices()
    signal_hlal = prices["HLAL"].dropna()
    first_signal_day, start_day = find_start_date(signal_hlal)
    purified = step8_final.purify_full_period(prices, signal_hlal)
    tbill_returns = purified[BENCHMARK].pct_change()

    all_results, all_gaps = {}, {}
    for scenario, settings in SCENARIOS.items():
        equities = run_scenario(purified, signal_hlal, first_signal_day, start_day, settings["daily"], settings["cost"])
        all_results[scenario], all_gaps[scenario] = {}, {}
        for period in PERIODS:
            results = {name: measure_period(eq, tbill_returns, period) for name, eq in equities.items()}
            all_results[scenario][period] = results
            all_gaps[scenario][period] = gaps_against_benchmark(results)
    return all_results, all_gaps


def cagr_change_lines(old, new):
    lines = [
        f"| Version | CAGR at {OLD_RATE:.1%} | CAGR at {NEW_RATE:.0%} | Difference |",
        "| --- | --- | --- | --- |",
    ]
    for name in old:
        a, b = old[name]["CAGR"], new[name]["CAGR"]
        lines.append(f"| {name} | {a:.2%} | {b:.2%} | {b - a:+.3%} |")
    return lines


def write_results(old_results, new_results, new_gaps):
    RESULTS_FILE.parent.mkdir(exist_ok=True)
    lines = [
        "# Step 11: Purification at Wahed's published rate (5%)",
        "",
        f"Steps 7-8 used {OLD_RATE:.1%} of each HLAL dividend (third-party estimate). "
        f"Wahed's published HLAL purification is {NEW_RATE:.0%} of every dividend, 2019 to Q2 2026.",
        "Source: wahed.com/hlal, Quarterly Purification on HLAL Dividends (as of 30 June 2026).",
        "Everything else is identical to step 8.",
    ]
    for scenario in SCENARIOS:
        lines += ["", f"## {scenario}"]
        for period in PERIODS:
            lines += ["", f"### {period}", "", "CAGR before and after the change:", ""]
            lines += cagr_change_lines(old_results[scenario][period], new_results[scenario][period])
            lines += ["", f"All versions at {NEW_RATE:.0%} purification:", ""]
            lines += comparison_table(new_results[scenario][period])
            lines += ["", "Gap: each halal option minus the T-bill version", ""]
            lines += gap_table(new_gaps[scenario][period])
    RESULTS_FILE.write_text("\n".join(lines) + "\n")


def main():
    old_results, old_gaps = run_all(OLD_RATE)
    new_results, new_gaps = run_all(NEW_RATE)

    print(f"Purification {OLD_RATE:.1%} -> {NEW_RATE:.0%}: largest CAGR change in any version, scenario or period:")
    biggest = 0.0
    for scenario in SCENARIOS:
        for period in PERIODS:
            for name in old_results[scenario][period]:
                change = new_results[scenario][period][name]["CAGR"] - old_results[scenario][period][name]["CAGR"]
                biggest = min(biggest, change)
    print(f"  {biggest:+.3%} per year\n")

    print(f"THE GAP at {NEW_RATE:.0%} purification (was at {OLD_RATE:.1%}):")
    for scenario in SCENARIOS:
        print(f"\n  {scenario}")
        for period in PERIODS:
            for label, gap in new_gaps[scenario][period].items():
                was = old_gaps[scenario][period][label]["Return gap per year (CAGR)"]
                now = gap["Return gap per year (CAGR)"]
                print(f"    {period:14} {label:14} return {now:+.2%} per year (was {was:+.2%})")

    write_results(old_results, new_results, new_gaps)
    print(f"\nFull tables saved to {RESULTS_FILE}")


if __name__ == "__main__":
    main()
