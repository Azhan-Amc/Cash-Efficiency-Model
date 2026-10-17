"""
Cash Efficiency Model - Step 3: 200-day rule with 0% cash (in-sample only).

Holds HLAL when it is above its 200-day average at month-end; otherwise
holds cash earning 0%. The rule is in backtest.py; this file only picks
the parking option and saves the results.

Only in-sample data is used (up to December 31, 2023).

Requires prices.csv from load_data.py.
"""

from pathlib import Path

from backtest import CASH, behaviour_stats, format_behaviour, run_backtest
from metrics import format_value, summarize
from step2_buy_and_hold import COST_PER_TRADE, find_start_date, load_in_sample_prices

PARKING = CASH
RESULTS_FILE = Path("results") / "step3_rule_cash.md"


def write_results(stats, behaviour, switches):
    RESULTS_FILE.parent.mkdir(exist_ok=True)
    lines = [
        "# Step 3: 200-day rule with 0% cash (in-sample)",
        "",
        "| Metric | Value |",
        "| --- | --- |",
    ]
    lines += [f"| {name} | {format_value(name, value)} |" for name, value in stats.items()]
    lines += [f"| {name} | {format_behaviour(name, value)} |" for name, value in behaviour.items()]
    lines += ["", "## Switch log", "", "| Trade date | Now holding |", "| --- | --- |"]
    lines += [f"| {day.date()} | {asset} |" for day, asset in switches.items()]
    RESULTS_FILE.write_text("\n".join(lines) + "\n")


def main():
    prices = load_in_sample_prices()
    hlal = prices["HLAL"].dropna()
    first_signal_day, start_day = find_start_date(hlal)

    equity, positions, trades, switches = run_backtest(
        prices, hlal, first_signal_day, start_day, PARKING, COST_PER_TRADE
    )

    stats = summarize(equity, prices["BIL"].pct_change())
    behaviour = behaviour_stats(positions, trades, COST_PER_TRADE)

    for name, value in stats.items():
        print(f"{name:32} {format_value(name, value)}")
    for name, value in behaviour.items():
        print(f"{name:32} {format_behaviour(name, value)}")

    print("\nSwitch log:")
    for day, asset in switches.items():
        print(f"  {day.date()}  now holding {asset}")

    write_results(stats, behaviour, switches)
    print(f"\nSaved to {RESULTS_FILE}")


if __name__ == "__main__":
    main() 