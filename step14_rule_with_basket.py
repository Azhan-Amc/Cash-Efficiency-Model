"""
Cash Efficiency Model - Step 14: the 200-day rule parking in the sukuk + gold basket.

One variable changes from the paper: what the rule holds when parked.
Instead of one option, it holds the basket fixed in step 13
(results/step13_basket_weights.json), rebalanced to those weights at each
monthly check while parked. Everything else is the paper's main setup:
same signal, dates, costs, scenarios, out-of-sample convention, and Wahed's
5% purification (step 11).

What this is and is not:
- The weights were chosen on 2004-2019 data, before HLAL existed, by a rule
  fixed in SPEC.md section 7. They were not fitted to the 2020-2026 results.
- But the 2020-2026 results of SPSK and GLD on their own are already known
  (steps 3-12). So this is NOT a fresh out-of-sample test. The only clean
  test of the basket is forward, from the day the weights were locked.

Costs, same convention as backtest.py: every dollar bought or sold pays
0.10%. Moving from HLAL into the basket = sell 100% + buy 100% = 0.20%,
exactly like moving into a single ETF. Monthly rebalancing while parked
pays 0.10% on the small amount traded.

Self-check before reporting: the basket engine run with 100% SPSK, 100% GLD
or 100% cash must reproduce backtest.py's results exactly. If not, the
script stops.

Requires prices.csv, dividends_hlal.csv and results/step13_basket_weights.json.
Output: results/step14_rule_with_basket.md
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd

import step8_final
from backtest import CASH, EQUITY, build_positions, run_backtest
from metrics import format_value, summarize
from step2_buy_and_hold import COST_PER_TRADE, IN_SAMPLE_END, find_start_date, month_end_trading_days
from step6_tbill_comparison import BENCHMARK, HALAL_OPTIONS, TABLE_METRICS, comparison_table, gap_table
from step8_final import (OUT_OF_SAMPLE_START, PERIODS, SCENARIOS, load_full_prices, measure_period,
                         positions_from_signal_days, run_scenario)

PURIFICATION_RATE = 0.05   # Wahed's published rate, the paper's main setting (step 11)
WEIGHTS_FILE = Path("results") / "step13_basket_weights.json"
RESULTS_FILE = Path("results") / "step14_rule_with_basket.md"
BASKET = "BASKET"
BASKET_LABEL = "Basket (SPSK + GLD)"


# ---------- Basket engine ----------

def load_weights():
    data = json.loads(WEIGHTS_FILE.read_text())
    w = {k: float(v) for k, v in data["weights"].items()}
    if abs(sum(w.values()) - 1) > 1e-9:
        raise ValueError(f"Basket weights must add up to 1, got {w}")
    return w


def target_weights(label, basket):
    if label == EQUITY:
        return {EQUITY: 1.0}
    if label == CASH:
        return {CASH: 1.0}
    if label == BASKET:
        return dict(basket)
    return {label: 1.0}  # a single parking ETF


def rebalance_days(index):
    """Trading day after each month-end: the day the rule acts."""
    days = []
    for day in month_end_trading_days(index):
        i = index.get_loc(day) + 1
        if i < len(index):
            days.append(index[i])
    return set(days)


def run_weights_engine(prices, positions, basket, cost_per_trade):
    """Daily value of a portfolio that follows `positions`, holding weights per label.

    Timing (same as backtest.py): holdings at yesterday's close earn today's
    return; trades happen at today's close and pay cost_per_trade on every
    dollar bought or sold. While parked in the basket, weights are reset to
    target on each monthly rebalance day.
    """
    days = positions.index
    returns = prices.loc[days].pct_change().fillna(0.0)
    returns[CASH] = 0.0
    monthly = rebalance_days(prices.index)

    holdings = {}           # asset -> value, before today's trade
    value = 1.0
    previous_label = None
    out = pd.Series(np.nan, index=days)
    turnover_log = pd.Series(0.0, index=days)

    for t, day in enumerate(days):
        label = positions.iloc[t]
        if t > 0:
            holdings = {a: v * (1 + returns.at[day, a]) for a, v in holdings.items()}
            value = sum(holdings.values())

        must_trade = label != previous_label or (label == BASKET and day in monthly)
        if must_trade:
            target = {a: w * value for a, w in target_weights(label, basket).items()}
            assets = set(holdings) | set(target)
            traded = sum(abs(target.get(a, 0.0) - holdings.get(a, 0.0)) for a in assets if a != CASH)
            cost = cost_per_trade * traded
            # cost comes out of the new holdings in proportion to the target weights
            scale = (value - cost) / value
            holdings = {a: v * scale for a, v in target.items()}
            value = sum(holdings.values())
            turnover_log.iloc[t] = traded
        out.iloc[t] = value
        previous_label = label

    return out, turnover_log


def basket_positions(signal_hlal, first_signal_day, start_day, daily):
    """What the rule holds each day (HLAL or BASKET), built by the paper's own functions."""
    if daily:
        days = signal_hlal.loc[first_signal_day:].index
        return positions_from_signal_days(signal_hlal, days, start_day, BASKET)
    return build_positions(signal_hlal, first_signal_day, start_day, BASKET)


# ---------- Self-check against backtest.py ----------

def self_check(purified, signal_hlal, first_signal_day, start_day):
    worst = 0.0
    for parking in [CASH, "SPSK", "GLD"]:
        for cost in [COST_PER_TRADE, 0.0025]:
            reference, positions, _, _ = run_backtest(purified, signal_hlal, first_signal_day, start_day, parking, cost)
            # tell the engine that `parking` is a 100% basket of that one asset
            relabelled = positions.replace({parking: BASKET})
            mine, _ = run_weights_engine(purified, relabelled, {parking: 1.0}, cost)
            diff = (mine / reference - 1).abs().max()
            worst = max(worst, diff)
            if diff > 1e-10:
                raise AssertionError(f"Engine does not reproduce backtest.py for {parking} at {cost:.2%}: {diff:.2e}")
    return worst


# ---------- The basket on its own (same tables as step 12) ----------

def standalone_basket(prices, basket):
    """Basket bought and held alone, rebalanced on the first trading day of each month."""
    assets = list(basket)
    p = prices[assets].dropna()
    daily = p.pct_change().fillna(0.0)
    value, out = 1.0, []
    holdings = {a: basket[a] for a in assets}
    months = daily.index.to_period("M")
    for i, day in enumerate(daily.index):
        if i > 0:
            holdings = {a: v * (1 + daily.at[day, a]) for a, v in holdings.items()}
            value = sum(holdings.values())
            if months[i] != months[i - 1]:
                holdings = {a: basket[a] * value for a in assets}
        out.append(value)
    return pd.Series(out, index=daily.index, name="Basket")


def basket_risk_profile(prices, basket):
    import importlib
    step12 = importlib.import_module("12_parking_options_on_their_own")

    series = prices[["HLAL", "SPSK", "GLD", "BIL"]].copy()
    series["Basket"] = standalone_basket(prices, basket)
    columns = ["HLAL", "SPSK", "GLD", "Basket", "BIL"]

    a_rows, b_rows = [], []
    for period, (start, end) in step12.PERIODS.items():
        for col in columns:
            a_rows.append({"Period": period, "Asset": col, **step12.standalone_stats(series[col], start, end)})
        daily = series.loc[start:end].pct_change().iloc[1:]
        b_rows.append({"Period": period, **{c: daily["HLAL"].corr(daily[c]) for c in columns if c != "HLAL"}})

    c_rows = []
    for peak, trough, recovery, _ in step12.find_drawdown_episodes(series["HLAL"], step12.DRAWDOWN_THRESHOLD):
        row = {"Peak": peak.date(), "Trough": trough.date()}
        row.update({c: step12.period_return(series[c], peak, trough) for c in columns})
        c_rows.append(row)

    return pd.DataFrame(a_rows), pd.DataFrame(b_rows), pd.DataFrame(c_rows)


def plain_table(df, percent_cols=(), decimal_cols=()):
    shown = df.copy()
    for c in percent_cols:
        shown[c] = shown[c].map(lambda v: "n/a" if pd.isna(v) else f"{v:.2%}")
    for c in decimal_cols:
        shown[c] = shown[c].map(lambda v: "n/a" if pd.isna(v) else f"{v:.2f}")
    lines = ["| " + " | ".join(shown.columns) + " |", "| " + " | ".join("---" for _ in shown.columns) + " |"]
    lines += ["| " + " | ".join(str(v) for v in row) + " |" for row in shown.values]
    return lines


# ---------- Running ----------

def gaps_vs_tbills(results, labels):
    bench = results["Rule + T-bills (BIL, benchmark)"]
    return {
        label: {
            "Return gap per year (CAGR)": results[f"Rule + {label}"]["CAGR"] - bench["CAGR"],
            "Drawdown gap (max drawdown)": results[f"Rule + {label}"]["Max drawdown"] - bench["Max drawdown"],
        }
        for label in labels
    }


def parked_cost_stats(turnover, positions, cost):
    oos_start = positions.loc[:IN_SAMPLE_END].index[-1]
    stats = {}
    for period, part in [("In-sample", turnover.loc[:IN_SAMPLE_END]), ("Out-of-sample", turnover.loc[oos_start:].iloc[1:])]:
        pos = positions.loc[part.index]
        rebalance_only = part[(pos == BASKET) & (pos.shift(1) == BASKET)]
        stats[period] = {
            "rebalances": int((rebalance_only > 0).sum()),
            "rebalance cost": rebalance_only.sum() * cost,
            "all trading cost": part.sum() * cost,
        }
    return stats


def main():
    basket = load_weights()
    labels_text = " + ".join(f"{w:.0%} {a}" for a, w in basket.items())

    step8_final.PURIFICATION_RATE = PURIFICATION_RATE
    prices = load_full_prices()
    signal_hlal = prices["HLAL"].dropna()
    first_signal_day, start_day = find_start_date(signal_hlal)
    purified = step8_final.purify_full_period(prices, signal_hlal)
    tbill_returns = purified[BENCHMARK].pct_change()

    worst = self_check(purified, signal_hlal, first_signal_day, start_day)
    print(f"Self-check passed: engine reproduces backtest.py (largest difference {worst:.1e}).\n")

    labels = list(HALAL_OPTIONS) + [BASKET_LABEL]
    all_results, all_gaps, cost_notes = {}, {}, {}
    for scenario, settings in SCENARIOS.items():
        equities = run_scenario(purified, signal_hlal, first_signal_day, start_day, settings["daily"], settings["cost"])
        positions = basket_positions(signal_hlal, first_signal_day, start_day, settings["daily"])
        basket_equity, turnover = run_weights_engine(purified, positions, basket, settings["cost"])

        ordered = {}
        for name, eq in equities.items():
            if name == "Rule + T-bills (BIL, benchmark)":
                ordered[f"Rule + {BASKET_LABEL}"] = basket_equity
            ordered[name] = eq

        all_results[scenario], all_gaps[scenario] = {}, {}
        for period in PERIODS:
            results = {name: measure_period(eq, tbill_returns, period) for name, eq in ordered.items()}
            all_results[scenario][period] = results
            all_gaps[scenario][period] = gaps_vs_tbills(results, labels)
        cost_notes[scenario] = parked_cost_stats(turnover, positions, settings["cost"])

    # ---------- Print ----------
    main_scenario = list(SCENARIOS)[0]
    print(f"Basket (locked in step 13): {labels_text}. Purification {PURIFICATION_RATE:.0%}.\n")
    for period in PERIODS:
        print(f"MAIN TEST, {period.upper()}:")
        for name, stats in all_results[main_scenario][period].items():
            summary = ", ".join(f"{m} {format_value(m, stats[m])}" for m in TABLE_METRICS)
            print(f"  {name:35} {summary}")
        print()

    print("THE GAP (halal option minus T-bill version), every scenario and period:")
    for scenario in SCENARIOS:
        print(f"\n  {scenario}")
        for period in PERIODS:
            for label, gap in all_gaps[scenario][period].items():
                print(f"    {period:14} {label:20} return {gap['Return gap per year (CAGR)']:+.2%} per year, "
                      f"drawdown {gap['Drawdown gap (max drawdown)']:+.2%}")

    # ---------- Save ----------
    RESULTS_FILE.parent.mkdir(exist_ok=True)
    lines = [
        "# Step 14: The rule parking in the sukuk + gold basket",
        "",
        f"Basket locked in step 13 (2004-2019 data): **{labels_text}**, rebalanced at each monthly check while parked.",
        f"Purification: {PURIFICATION_RATE:.0%} of HLAL dividends (Wahed). Same rule, dates, costs and scenarios as the paper.",
        "",
        "Not a fresh out-of-sample test: SPSK's and GLD's 2020-2026 results were already known. "
        "The weights were not fitted to them. The clean test is forward from the lock date.",
        "",
        f"Self-check: the engine reproduces backtest.py exactly for 100% cash, SPSK and GLD (largest difference {worst:.1e}).",
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
            c = cost_notes[scenario][period]
            lines += ["", f"Basket trading: {c['rebalances']} monthly rebalances costing {c['rebalance cost']:.3%} in total; "
                          f"all basket trading costs {c['all trading cost']:.3%}."]
    # The basket on its own, next to each option (unpurified prices, as in step 12)
    a, b, c = basket_risk_profile(prices, basket)
    profile = [
        "", "## The basket on its own (no trend rule), next to each option", "",
        "A. Standalone risk", "",
        *plain_table(a, percent_cols=["CAGR", "Volatility", "Max drawdown", "Worst month"]),
        "", "B. Correlation of daily returns with HLAL", "",
        *plain_table(b, decimal_cols=[col for col in b.columns if col != "Period"]),
        "", "C. Return during each HLAL drawdown of 10% or more (peak close to trough close)", "",
        *plain_table(c, percent_cols=[col for col in c.columns if col not in ("Peak", "Trough")]),
    ]
    lines += profile
    print("\n".join(profile))

    RESULTS_FILE.write_text("\n".join(lines) + "\n")
    print(f"\nFull tables saved to {RESULTS_FILE}")


if __name__ == "__main__":
    main()
