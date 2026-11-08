"""
Step 12 - The parking options on their own.

Descriptive statistics for each parking asset held alone, with no trend rule.
Nothing here changes the main results; it describes the assets behind them.

  A. Standalone risk: CAGR, volatility, max drawdown, worst month
     (in-sample and out-of-sample, same dates as the paper)
  B. Correlation of daily returns with HLAL
  C. Return of each asset during every HLAL drawdown of 10% or more
     (peak close to trough close)
  D. Return of each asset during each of the 5 parked episodes of the main test

Prices: Yahoo Finance, dividend-adjusted closes (total return), as in the paper.
No purification is applied here (assets are shown on their own, not as versions).

Output: results/step12/  (one CSV per table + report.txt)
"""

import os

import numpy as np
import pandas as pd
import yfinance as yf

TICKERS = ["HLAL", "SPSK", "GLD", "GLDM", "BIL"]
DOWNLOAD_START = "2019-07-01"   # HLAL's first month, so drawdown peaks see its full history
DOWNLOAD_END = "2026-10-01"     # yfinance end date is exclusive -> last day is Sep 30, 2026
OUT_DIR = os.path.join("results", "step12")

# Same windows as the paper (Appendix): growth measured from these closes
PERIODS = {
    "In-sample": ("2020-05-01", "2023-12-29"),
    "Out-of-sample": ("2023-12-29", "2026-09-30"),
}

# Parked episodes of the main test: (exit close, re-entry close), from the Appendix
PARKED_EPISODES = [
    ("2020-05-01", "2020-06-01"),
    ("2022-05-02", "2022-12-01"),
    ("2023-01-03", "2023-02-01"),
    ("2023-11-01", "2023-12-01"),
    ("2025-04-01", "2025-07-01"),
]

DRAWDOWN_THRESHOLD = -0.10


def download_prices():
    data = yf.download(
        TICKERS,
        start=DOWNLOAD_START,
        end=DOWNLOAD_END,
        auto_adjust=True,
        progress=False,
    )
    prices = data["Close"][TICKERS]
    return prices


def window(series, start, end):
    """Prices from the start close to the end close, with missing days dropped."""
    return series.loc[start:end].dropna()


def standalone_stats(series, start, end):
    p = window(series, start, end)
    if len(p) < 2 or p.index[0] != pd.Timestamp(start):
        # asset has no price on the start date -> not comparable, leave blank
        return {"CAGR": np.nan, "Volatility": np.nan,
                "Max drawdown": np.nan, "Worst month": np.nan}

    days = (p.index[-1] - p.index[0]).days
    cagr = (p.iloc[-1] / p.iloc[0]) ** (365.25 / days) - 1

    daily = p.pct_change().dropna()
    vol = daily.std() * np.sqrt(252)

    max_dd = (p / p.cummax() - 1).min()

    month_end = p.groupby(p.index.to_period("M")).last()
    worst_month = month_end.pct_change().dropna().min()

    return {"CAGR": cagr, "Volatility": vol,
            "Max drawdown": max_dd, "Worst month": worst_month}


def table_a_standalone(prices):
    rows = []
    for period, (start, end) in PERIODS.items():
        for ticker in TICKERS:
            stats = standalone_stats(prices[ticker], start, end)
            rows.append({"Period": period, "Asset": ticker, **stats})
    return pd.DataFrame(rows)


def table_b_correlation(prices):
    rows = []
    for period, (start, end) in PERIODS.items():
        daily = prices.loc[start:end].pct_change().iloc[1:]
        row = {"Period": period}
        for ticker in TICKERS:
            if ticker == "HLAL":
                continue
            pair = daily[["HLAL", ticker]].dropna()
            row[ticker] = pair["HLAL"].corr(pair[ticker])
        rows.append(row)
    return pd.DataFrame(rows)


def find_drawdown_episodes(p, threshold):
    """Every underwater spell whose trough is at or below the threshold.

    Peak = last new high before the fall; trough = lowest close in the spell;
    recovery = first close back at the old high (None if not yet recovered).
    """
    p = p.dropna()
    dd = p / p.cummax() - 1

    episodes = []
    in_drawdown = False
    prev_date = dd.index[0]
    peak_date = trough_date = None
    trough_value = 0.0

    for date, value in dd.items():
        if not in_drawdown:
            if value < 0:
                in_drawdown = True
                peak_date = prev_date
                trough_date, trough_value = date, value
        else:
            if value < trough_value:
                trough_date, trough_value = date, value
            if value == 0:
                if trough_value <= threshold:
                    episodes.append((peak_date, trough_date, date, trough_value))
                in_drawdown = False
        prev_date = date

    if in_drawdown and trough_value <= threshold:
        episodes.append((peak_date, trough_date, None, trough_value))

    return episodes


def period_return(series, start, end):
    start, end = pd.Timestamp(start), pd.Timestamp(end)
    if start not in series.index or end not in series.index:
        return np.nan
    a, b = series.loc[start], series.loc[end]
    if pd.isna(a) or pd.isna(b):
        return np.nan
    return b / a - 1


def table_c_hlal_drawdowns(prices):
    episodes = find_drawdown_episodes(prices["HLAL"], DRAWDOWN_THRESHOLD)
    rows = []
    for peak, trough, recovery, depth in episodes:
        row = {
            "Peak": peak.date(),
            "Trough": trough.date(),
            "Recovered": recovery.date() if recovery is not None else "not yet",
        }
        for ticker in TICKERS:
            row[ticker] = period_return(prices[ticker], peak, trough)
        rows.append(row)
    return pd.DataFrame(rows)


def table_d_parked_episodes(prices):
    rows = []
    for exit_date, reentry_date in PARKED_EPISODES:
        trading_days = len(prices.loc[exit_date:reentry_date].dropna(subset=["HLAL"])) - 1
        row = {"Exit": exit_date, "Re-entry": reentry_date, "Trading days": trading_days}
        for ticker in TICKERS:
            row[ticker] = period_return(prices[ticker], exit_date, reentry_date)
        rows.append(row)
    return pd.DataFrame(rows)


def as_percent(df, columns):
    shown = df.copy()
    for col in columns:
        shown[col] = shown[col].map(lambda x: "n/a" if pd.isna(x) else f"{x:.2%}")
    return shown


def as_decimal(df, columns):
    shown = df.copy()
    for col in columns:
        shown[col] = shown[col].map(lambda x: "n/a" if pd.isna(x) else f"{x:.2f}")
    return shown


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    prices = download_prices()

    first_days = prices.apply(lambda s: s.first_valid_index().date())
    last_days = prices.apply(lambda s: s.last_valid_index().date())

    a = table_a_standalone(prices)
    b = table_b_correlation(prices)
    c = table_c_hlal_drawdowns(prices)
    d = table_d_parked_episodes(prices)

    a.to_csv(os.path.join(OUT_DIR, "A_standalone_risk.csv"), index=False)
    b.to_csv(os.path.join(OUT_DIR, "B_correlation_with_HLAL.csv"), index=False)
    c.to_csv(os.path.join(OUT_DIR, "C_returns_in_HLAL_drawdowns.csv"), index=False)
    d.to_csv(os.path.join(OUT_DIR, "D_returns_in_parked_episodes.csv"), index=False)

    others = [t for t in TICKERS if t != "HLAL"]
    lines = [
        "STEP 12 - THE PARKING OPTIONS ON THEIR OWN",
        "Adjusted closes from Yahoo Finance; no purification; no trend rule.",
        "",
        "Data range per ticker:",
        pd.DataFrame({"First day": first_days, "Last day": last_days}).to_string(),
        "",
        "A. Standalone risk (each asset bought and held alone)",
        as_percent(a, ["CAGR", "Volatility", "Max drawdown", "Worst month"]).to_string(index=False),
        "",
        "B. Correlation of daily returns with HLAL",
        as_decimal(b, others).to_string(index=False),
        "",
        f"C. Return during each HLAL drawdown of {abs(DRAWDOWN_THRESHOLD):.0%} or more (peak close to trough close)",
        as_percent(c, TICKERS).to_string(index=False) if len(c) else "No drawdown reached the threshold.",
        "",
        "D. Return during each parked episode of the main test (exit close to re-entry close)",
        as_percent(d, TICKERS).to_string(index=False),
        "",
    ]
    report = "\n".join(lines)

    with open(os.path.join(OUT_DIR, "report.txt"), "w", encoding="utf-8") as f:
        f.write(report)
    print(report)
    print(f"Saved to {OUT_DIR}/")


if __name__ == "__main__":
    main()