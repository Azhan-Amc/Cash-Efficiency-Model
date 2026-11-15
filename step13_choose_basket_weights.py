"""
Cash Efficiency Model - Step 13: choose the parking basket's weights from older history.

Question: instead of parking in ONE halal option, should the rule park in a
fixed mix of sukuk and gold? And if so, in what proportions?

Why the weights are NOT chosen on the HLAL period (2019-2026):
every parking option's results on that period are already known (steps 3-12),
so any mix picked there would be fitted to results we have seen. The weights
are decided here, on 2004-2019 data that the paper never used, by one rule
fixed in advance (SPEC.md, section 7). Step 14 then applies them unchanged.

The decision rule (SPEC.md, section 7):
  1. Find the parked months with the same 200-day monthly rule, using SPY as
     the stand-in for a US Shariah equity index (HLAL did not exist yet).
  2. During parked weeks only, measure the volatility of gold (GLD) and of a
     sukuk stand-in (PREMX, an emerging-market dollar bond fund; SPSK did not
     exist yet). Weekly returns, because mutual-fund NAVs on foreign bonds are
     stale day to day.
  3. Weights = inverse volatility ("risk parity"): each asset contributes the
     same risk. Rounded to the nearest 5%. These are the locked weights.
  4. 0% cash is not in the basket. With a 0% risk-free rate, mixing in cash
     scales return and risk down together and leaves the Sharpe ratio
     unchanged, so it is a choice of risk level, not of efficiency.

Everything else printed here (bootstrap interval, per-episode odds of a loss,
proxy check) describes how reliable that choice is. None of it changes the
weights.

Stand-ins are used only to MEASURE; nothing here is held. SPY and PREMX are
not halal instruments and never enter a portfolio in this project.

Output: results/step13_basket_weights.md and results/step13_basket_weights.json
(the JSON is what step 14 reads).
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

from step2_buy_and_hold import SMA_DAYS, month_end_trading_days

PROXY_TICKERS = ["SPY", "GLD", "PREMX"]
DOWNLOAD_START = "2003-11-01"     # one year before GLD, so SPY's 200-day average is ready
CALIBRATION_START = "2004-11-18"  # GLD's first trading day
CALIBRATION_END = "2019-06-28"    # last month-end before HLAL launched (July 15, 2019)

# Proxy check only: weekly correlation of PREMX with the real sukuk ETF, 2020-2026.
# Printed for information; it does not feed into the weights.
CHECK_TICKERS = ["PREMX", "SPSK"]
CHECK_START = "2020-01-01"
CHECK_END = "2026-10-01"

GOLD, SUKUK_PROXY = "GLD", "PREMX"
ROUND_TO = 0.05
BOOTSTRAP_DRAWS = 10_000
SEED = 13

RESULTS_DIR = Path("results")
REPORT_FILE = RESULTS_DIR / "step13_basket_weights.md"
WEIGHTS_FILE = RESULTS_DIR / "step13_basket_weights.json"


# ---------- Data ----------

def download(tickers, start, end):
    raw = yf.download(tickers, start=start, end=end, auto_adjust=True, progress=False)
    return raw["Close"][tickers]


# ---------- Parked periods (same rule as backtest.py, on SPY) ----------

def parked_days(spy):
    """True on every day the rule would have been parked, False when in equities.

    Same timing as the main test: signal on the last trading day of the month,
    position taken at the next day's close, held until the next execution day.
    """
    sma = spy.rolling(SMA_DAYS).mean()
    held = pd.Series(np.nan, index=spy.index, dtype=object)
    for day in month_end_trading_days(spy.index):
        if pd.isna(sma.loc[day]):
            continue
        i = spy.index.get_loc(day) + 1
        if i < len(spy.index):
            held.iloc[i] = "EQUITY" if spy.loc[day] > sma.loc[day] else "PARKED"
    held = held.ffill()
    # a day "is parked" if the money sat in the parking basket from yesterday's close to today's
    return (held.shift(1) == "PARKED")


def parked_episodes(is_parked):
    """List of (first parked day, last parked day) spells."""
    episodes, start = [], None
    for day, flag in is_parked.items():
        if flag and start is None:
            start = day
        if not flag and start is not None:
            episodes.append((start, previous))
            start = None
        previous = day
    if start is not None:
        episodes.append((start, previous))
    return episodes


# ---------- Statistics ----------

def weekly_returns(prices, days):
    """Weekly (Friday-to-Friday) returns built only from the given days."""
    p = prices.loc[days]
    weekly = p.resample("W-FRI").last().dropna(how="all")
    return weekly.pct_change().dropna()


def episode_weekly_returns(prices, episodes):
    """Weekly returns inside each parked episode, kept separate per episode.

    Each episode starts from the close BEFORE its first parked day, so its first
    week is counted. Weeks never span two episodes.
    """
    out = []
    for first, last in episodes:
        i = prices.index.get_loc(first)
        start = prices.index[max(i - 1, 0)]
        p = prices.loc[start:last]
        # anchor at the close before parking began, then every Friday close (or last day)
        weekly = pd.concat([p.iloc[[0]], p.resample("W-FRI").last()])
        weekly = weekly[~weekly.index.duplicated(keep="last")].sort_index()
        r = weekly.pct_change().dropna()
        if len(r):
            out.append(r)
    return out


def inverse_vol_weights(weekly):
    vol = weekly.std() * np.sqrt(52)
    inv = 1 / vol
    return vol, inv / inv.sum()


def round_weights(w, step):
    sukuk = round(w[SUKUK_PROXY] / step) * step
    sukuk = min(max(sukuk, 0.0), 1.0)
    return {SUKUK_PROXY: round(sukuk, 4), GOLD: round(1 - sukuk, 4)}


def bootstrap_sukuk_weight(episode_returns, draws, seed):
    """Resample whole parked episodes with replacement; recompute the weight each time."""
    rng = np.random.default_rng(seed)
    n = len(episode_returns)
    weights = np.empty(draws)
    for k in range(draws):
        pick = rng.integers(0, n, n)
        pooled = pd.concat([episode_returns[j] for j in pick])
        if pooled[GOLD].std() == 0 or pooled[SUKUK_PROXY].std() == 0:
            weights[k] = np.nan
            continue
        _, w = inverse_vol_weights(pooled)
        weights[k] = w[SUKUK_PROXY]
    return weights[~np.isnan(weights)]


def episode_table(prices, episodes, w):
    """Return of gold, sukuk proxy and the basket over each parked episode.

    The basket is rebalanced to its weights at the start of every calendar
    month while parked (the rule's monthly check), same as step 14.
    """
    rows = []
    for first, last in episodes:
        i = prices.index.get_loc(first)
        start = prices.index[max(i - 1, 0)]
        p = prices.loc[start:last, [GOLD, SUKUK_PROXY]]
        daily = p.pct_change().iloc[1:]

        basket = 1.0
        for _, month in daily.groupby(daily.index.to_period("M")):
            growth = (1 + month).prod()
            basket *= w[GOLD] * growth[GOLD] + w[SUKUK_PROXY] * growth[SUKUK_PROXY]

        rows.append({
            "Parked from": first.date(),
            "Parked to": last.date(),
            "Trading days": len(daily),
            "Gold (GLD)": p[GOLD].iloc[-1] / p[GOLD].iloc[0] - 1,
            "Sukuk proxy (PREMX)": p[SUKUK_PROXY].iloc[-1] / p[SUKUK_PROXY].iloc[0] - 1,
            "Basket": basket - 1,
            "0% cash": 0.0,
        })
    return pd.DataFrame(rows)


def odds_table(episodes_df):
    cols = ["Gold (GLD)", "Sukuk proxy (PREMX)", "Basket", "0% cash"]
    rows = []
    for c in cols:
        x = episodes_df[c]
        rows.append({
            "Option": c,
            "Episodes": len(x),
            "Share of episodes with a loss": (x < 0).mean(),
            "Average episode return": x.mean(),
            "Median episode return": x.median(),
            "Worst episode": x.min(),
            "Best episode": x.max(),
        })
    return pd.DataFrame(rows)


# ---------- Output ----------

def pct(x, digits=2):
    return "n/a" if pd.isna(x) else f"{x:.{digits}%}"


def md_table(df, percent_cols=(), decimal_cols=()):
    shown = df.copy()
    for c in percent_cols:
        shown[c] = shown[c].map(pct)
    for c in decimal_cols:
        shown[c] = shown[c].map(lambda v: "n/a" if pd.isna(v) else f"{v:.2f}")
    header = "| " + " | ".join(shown.columns) + " |"
    sep = "| " + " | ".join("---" for _ in shown.columns) + " |"
    body = ["| " + " | ".join(str(v) for v in row) + " |" for row in shown.values]
    return [header, sep] + body


def main():
    RESULTS_DIR.mkdir(exist_ok=True)

    prices = download(PROXY_TICKERS, DOWNLOAD_START, CALIBRATION_END)
    prices = prices.loc[:CALIBRATION_END]
    spy = prices["SPY"].dropna()

    is_parked = parked_days(spy).loc[CALIBRATION_START:]
    assets = prices[[GOLD, SUKUK_PROXY]].loc[CALIBRATION_START:].dropna()
    is_parked = is_parked.reindex(assets.index, fill_value=False)
    episodes = parked_episodes(is_parked)

    # 1-3. The decision: inverse volatility on parked weeks
    ep_returns = episode_weekly_returns(assets, episodes)
    pooled = pd.concat(ep_returns)
    vol_parked, w_raw = inverse_vol_weights(pooled)
    corr_parked = pooled[GOLD].corr(pooled[SUKUK_PROXY])
    locked = round_weights(w_raw, ROUND_TO)

    # Context: same numbers over all weeks (not used for the decision)
    all_weekly = weekly_returns(assets, assets.index)
    vol_all, w_all = inverse_vol_weights(all_weekly)
    corr_all = all_weekly[GOLD].corr(all_weekly[SUKUK_PROXY])

    # Reliability: bootstrap over episodes
    boot = bootstrap_sukuk_weight(ep_returns, BOOTSTRAP_DRAWS, SEED)
    lo, mid, hi = np.percentile(boot, [5, 50, 95])
    share_near_locked = np.mean(np.abs(boot - locked[SUKUK_PROXY]) <= 0.10)

    # Per-episode outcomes with the locked weights
    ep_df = episode_table(assets, episodes, locked)
    odds = odds_table(ep_df)
    months = ep_df["Trading days"] / 21
    single_month_share = (months <= 1.5).mean()

    # Proxy check (information only): PREMX vs SPSK, 2020-2026
    try:
        check = download(CHECK_TICKERS, CHECK_START, CHECK_END).dropna()
        cw = check.resample("W-FRI").last().pct_change().dropna()
        proxy_corr = cw["PREMX"].corr(cw["SPSK"])
        proxy_vol = cw.std() * np.sqrt(52)
        proxy_line = (f"Weekly correlation PREMX vs SPSK, {check.index[0].date()} to {check.index[-1].date()}: "
                      f"{proxy_corr:.2f}. Annualized weekly volatility: PREMX {pct(proxy_vol['PREMX'])}, "
                      f"SPSK {pct(proxy_vol['SPSK'])}.")
    except Exception as error:  # the check is optional; never block the decision on it
        proxy_corr, proxy_line = np.nan, f"Proxy check skipped ({error})."

    parked_share = is_parked.mean()

    # ---------- Save the locked weights for step 14 ----------
    WEIGHTS_FILE.write_text(json.dumps({
        "decided_on": "step13_choose_basket_weights.py",
        "calibration_window": [CALIBRATION_START, CALIBRATION_END],
        "rule": "inverse volatility of weekly returns during parked weeks, rounded to 5%",
        "weights": {"SPSK": locked[SUKUK_PROXY], "GLD": locked[GOLD]},
        "unrounded_sukuk_weight": round(float(w_raw[SUKUK_PROXY]), 4),
    }, indent=2) + "\n")

    # ---------- Report ----------
    lines = [
        "# Step 13: Choosing the parking basket's weights (2004-2019, before HLAL)",
        "",
        f"Calibration window: {assets.index[0].date()} to {assets.index[-1].date()}. "
        "Signal: SPY vs its 200-day average, checked monthly, traded next close (same rule as the paper).",
        f"Share of days parked: {pct(parked_share)}. Parked episodes: {len(episodes)}.",
        "",
        "## The decision",
        "",
        "| | Gold (GLD) | Sukuk proxy (PREMX) |",
        "| --- | --- | --- |",
        f"| Volatility, parked weeks only | {pct(vol_parked[GOLD])} | {pct(vol_parked[SUKUK_PROXY])} |",
        f"| Inverse-volatility weight (unrounded) | {pct(w_raw[GOLD], 1)} | {pct(w_raw[SUKUK_PROXY], 1)} |",
        f"| **Locked weight (rounded to 5%)** | **{locked[GOLD]:.0%} GLD** | **{locked[SUKUK_PROXY]:.0%} SPSK** |",
        "",
        f"Correlation of gold and the sukuk proxy, parked weeks: {corr_parked:.2f} (all weeks: {corr_all:.2f}).",
        "",
        "In step 14 the sukuk weight is held in SPSK and the gold weight in GLD. "
        "Rebalanced to these weights at each monthly check while parked.",
        "",
        "## How reliable is the weight?",
        "",
        f"Bootstrap, {BOOTSTRAP_DRAWS:,} resamples of whole parked episodes: sukuk weight "
        f"5th percentile {pct(lo, 1)}, median {pct(mid, 1)}, 95th percentile {pct(hi, 1)}.",
        f"Share of resamples within 10 points of the locked {locked[SUKUK_PROXY]:.0%}: {pct(share_near_locked, 1)}.",
        "",
        "For context, the same rule on ALL weeks (parked or not) would give: "
        f"gold {pct(vol_all[GOLD])} vol, sukuk proxy {pct(vol_all[SUKUK_PROXY])} vol, "
        f"sukuk weight {pct(w_all[SUKUK_PROXY], 1)}. Not used.",
        "",
        "## Each parked episode, 2004-2019 (locked weights)",
        "",
    ]
    lines += md_table(ep_df, percent_cols=["Gold (GLD)", "Sukuk proxy (PREMX)", "Basket", "0% cash"])
    lines += [
        "",
        f"{pct(single_month_share, 0)} of episodes lasted about one month or less, so monthly rebalancing "
        "rarely triggers more than once.",
        "",
        "## Odds per episode",
        "",
    ]
    lines += md_table(odds, percent_cols=["Share of episodes with a loss", "Average episode return",
                                          "Median episode return", "Worst episode", "Best episode"])
    lines += [
        "",
        "## Proxy check (information only, does not affect the weights)",
        "",
        proxy_line,
        "",
        "## Notes",
        "",
        "- SPY and PREMX are measuring tools only. They are not halal instruments and are never held.",
        "- PREMX holds conventional emerging-market bonds. Its duration and credit mix differ from SPSK's, "
        "so its volatility is an estimate of sukuk risk, not a copy of it.",
        "- 0% cash is left out of the basket: at a 0% risk-free rate it changes the risk level, not the efficiency.",
    ]
    REPORT_FILE.write_text("\n".join(lines) + "\n")

    print("\n".join(lines))
    print(f"\nLocked weights saved to {WEIGHTS_FILE}")


if __name__ == "__main__":
    main()
