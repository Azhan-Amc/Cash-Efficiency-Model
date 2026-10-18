"""
Independent audit of the Cash Efficiency Model results.

Written separately from the repository code: it does NOT import backtest.py,
metrics.py or any step file. It re-implements the rule as a plain day-by-day
loop straight from SPEC.md, so agreement with the published numbers is a real
cross-check rather than the same code run twice.

Inputs: prices.csv and dividends_hlal.csv (as produced by the repo's loaders).
Usage:  python audit/independent_check.py .   (run from the repository root)
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

IN_SAMPLE_END = pd.Timestamp("2023-12-31")
OOS_END = pd.Timestamp("2026-09-30")
SMA_DAYS = 200
PURIFICATION_RATE = 0.008
PARKINGS = ["CASH", "GLD", "SPSK", "BIL"]


def load(folder):
    prices = pd.read_csv(folder / "prices.csv", index_col=0, parse_dates=True).loc[:OOS_END]
    divs = pd.read_csv(folder / "dividends_hlal.csv", index_col=0, parse_dates=True).loc[:OOS_END]
    return prices, divs


def month_ends(index):
    s = pd.Series(index, index=index)
    return list(s.groupby([index.year, index.month]).max())


def purified_hlal_returns(prices, divs):
    """Daily HLAL total return minus purification on ex-dividend days."""
    hlal = prices["HLAL"].dropna()
    ret = hlal.pct_change()
    div_yield = (divs["dividend"] / divs["raw_close"].shift(1)).reindex(hlal.index).fillna(0.0)
    drag = PURIFICATION_RATE * div_yield
    # value after purification: (1 + r) * (1 - drag)
    return (1 + ret) * (1 - drag) - 1, drag


def simulate(prices, hlal_ret, signal_days, start_day, parking, cost):
    """Plain loop. Returns equity series, list of (trade day, new holding), legs paid."""
    hlal = prices["HLAL"].dropna()
    sma = hlal.rolling(SMA_DAYS).mean()
    days = list(hlal.loc[start_day:].index)
    pos_in_index = {d: i for i, d in enumerate(hlal.index)}
    targets = {}
    for d in signal_days:
        i = pos_in_index[d]
        if i + 1 < len(hlal.index):
            targets[hlal.index[i + 1]] = "HLAL" if hlal[d] > sma[d] else parking

    rets = {"HLAL": hlal_ret}
    for a in ["GLD", "SPSK", "BIL"]:
        rets[a] = prices[a].pct_change()

    held, value, legs_total = None, 1.0, 0
    out, trades = [], []
    for k, d in enumerate(days):
        if k > 0 and held != "CASH":
            value *= 1 + rets[held][d]
        new = targets.get(d, held)
        if new != held:
            legs = (0 if held in (None, "CASH") else 1) + (0 if new == "CASH" else 1)
            value *= 1 - cost * legs
            legs_total += legs
            trades.append((d, new))
            held = new
        out.append(value)
    return pd.Series(out, index=days), trades, legs_total


def buy_and_hold(hlal_ret, start_day, cost):
    r = hlal_ret.loc[start_day:].copy()
    r.iloc[0] = 0.0
    return (1 - cost) * (1 + r).cumprod()


def metrics(eq, rf_returns, base):
    r = eq.pct_change().dropna()
    years = (eq.index[-1] - eq.index[0]).days / 365.25
    cagr = (eq.iloc[-1] / base) ** (1 / years) - 1
    peak = eq.cummax().clip(lower=base)
    mdd = (eq / peak - 1).min()
    ex = r - rf_returns.reindex(r.index)
    return {
        "start": eq.index[0].date(), "end": eq.index[-1].date(), "years": years,
        "start value": base, "end value": eq.iloc[-1],
        "CAGR": cagr, "vol": r.std() * np.sqrt(252), "MDD": mdd,
        "Sharpe0": r.mean() / r.std() * np.sqrt(252),
        "SharpeT": ex.mean() / ex.std() * np.sqrt(252),
        "Calmar": cagr / abs(mdd),
    }


def split(eq):
    ins = eq.loc[:IN_SAMPLE_END]
    oos = eq.loc[ins.index[-1]:]
    return ins, oos


def main(folder):
    prices, divs = load(folder)
    hlal = prices["HLAL"].dropna()
    hlal_ret, drag = purified_hlal_returns(prices, divs)
    sma = hlal.rolling(SMA_DAYS).mean()
    me = month_ends(hlal.index)
    first_signal = [d for d in me if not np.isnan(sma[d])][0]
    start_day = hlal.index[hlal.index.get_loc(first_signal) + 1]
    bil_ret = prices["BIL"].pct_change()
    print(f"first signal {first_signal.date()}, start {start_day.date()}")

    rows = []
    for cost in (0.001, 0.0025):
        for label, sig in (("monthly", [d for d in me if d >= first_signal]),
                           ("daily", list(hlal.loc[first_signal:].index))):
            if label == "daily" and cost != 0.001:
                continue
            eqs = {"Buy-and-hold": buy_and_hold(hlal_ret, start_day, cost)}
            logs = {}
            for p in PARKINGS:
                eq, trades, legs = simulate(prices, hlal_ret, sig, start_day, p, cost)
                eqs[p] = eq
                logs[p] = (trades, legs)
            for name, eq in eqs.items():
                ins, oos = split(eq)
                for period, seg, base in (("IS", ins, 1.0), ("OOS", oos, oos.iloc[0])):
                    m = metrics(seg, bil_ret, base)
                    m.update(scenario=f"{label} {cost:.2%}", version=name, period=period)
                    if name in PARKINGS:
                        trades, legs = logs[name]
                        held = pd.Series(np.nan, index=eq.index, dtype=object)
                        for d, a in trades:
                            held[d] = a
                        held = held.ffill()
                        hs = held.loc[seg.index]
                        m["parked share"] = (hs != "HLAL").mean()
                        m["switches"] = sum(1 for d, _ in trades if seg.index[0] < d <= seg.index[-1]) if period == "OOS" else sum(1 for d, _ in trades if d <= seg.index[-1]) - 1
                        # T-bill return earned on parked days (what 0% cash forgoes)
                        parked_days = hs.shift(1).reindex(seg.index) != "HLAL"
                        parked_days.iloc[0] = False
                        m["BIL return on parked days"] = (1 + bil_ret.loc[seg.index][parked_days]).prod() - 1
                    rows.append(m)
            if label == "monthly" and cost == 0.001:
                main_logs = logs
    df = pd.DataFrame(rows)
    pd.set_option("display.width", 250, "display.max_columns", 30, "display.max_rows", 200)
    cols = ["scenario", "period", "version", "start", "end", "years", "start value", "end value",
            "CAGR", "vol", "MDD", "Sharpe0", "SharpeT", "Calmar", "parked share", "switches", "BIL return on parked days"]
    print(df[cols].round(4).to_string(index=False))

    print("\nGaps vs BIL (CAGR, MDD):")
    for (sc, per), g in df.groupby(["scenario", "period"], sort=False):
        b = g[g.version == "BIL"].iloc[0]
        for p in ("CASH", "GLD", "SPSK"):
            r = g[g.version == p].iloc[0]
            print(f"  {sc:14} {per:4} {p:5} return {r.CAGR - b.CAGR:+.2%}  drawdown {r.MDD - b.MDD:+.2%}")

    print("\nMain-test trade log (cash version):")
    for d, a in main_logs["CASH"][0]:
        print(f"  {d.date()} -> {a}")
    print("Legs paid, main test:", {p: main_logs[p][1] for p in PARKINGS})

    total_drag = 1 - (1 - drag.loc[start_day:IN_SAMPLE_END]).prod()
    total_drag_oos = 1 - (1 - drag.loc[IN_SAMPLE_END:]).prod()
    print(f"\nPurification removed (if always in HLAL): in-sample {total_drag:.4%}, out-of-sample {total_drag_oos:.4%}")
    print(f"Dividend days used: {(drag > 0).sum()}")

    # Gross-of-cost gap for cash vs BIL, main monthly signal
    for cost in (0.0,):
        sig = [d for d in me if d >= first_signal]
        c, _, _ = simulate(prices, hlal_ret, sig, start_day, "CASH", cost)
        b, _, _ = simulate(prices, hlal_ret, sig, start_day, "BIL", cost)
        for per, (cs, bs) in (("IS", (split(c)[0], split(b)[0])), ("OOS", (split(c)[1], split(b)[1]))):
            mc = metrics(cs, bil_ret, 1.0 if per == "IS" else cs.iloc[0])
            mb = metrics(bs, bil_ret, 1.0 if per == "IS" else bs.iloc[0])
            print(f"Zero-cost cash minus BIL CAGR, {per}: {mc['CAGR'] - mb['CAGR']:+.2%}")


if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1 else "."))
