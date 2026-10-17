"""
The 200-day rule backtest, shared by steps 3 to 6.

Only the parking option changes between steps (0% cash, GLD, SPSK, BIL),
so the rule itself lives here once and is never rewritten.

The rule (SPEC.md, section 3):
- On the last trading day of each month, compare HLAL's close with its
  200-day simple moving average.
- Above the average: hold HLAL. Otherwise: hold the parking option.
- Trades happen at the close of the next trading day.
- Each buy or sell costs 0.10%. A switch from HLAL to a parking ETF is a
  sell plus a buy (0.20%). Moving to or from 0% cash is one trade (0.10%).

Timing: the asset held at the close of day t-1 earns the return of day t.
"""

import numpy as np
import pandas as pd

from step2_buy_and_hold import SMA_DAYS, month_end_trading_days

CASH = "CASH"
EQUITY = "HLAL"


def monthly_signals(hlal, first_signal_day):
    """Target asset decided on each month-end, from the first valid signal on."""
    sma = hlal.rolling(SMA_DAYS).mean()
    signal_days = [day for day in month_end_trading_days(hlal.index) if day >= first_signal_day]
    return {day: hlal.loc[day] > sma.loc[day] for day in signal_days}


def build_positions(hlal, first_signal_day, start_day, parking):
    """Asset held at the close of each day, from start_day to the last in-sample day."""
    days = hlal.loc[start_day:].index
    positions = pd.Series(np.nan, index=days, dtype=object)

    for signal_day, above_average in monthly_signals(hlal, first_signal_day).items():
        next_position = hlal.index.get_loc(signal_day) + 1
        if next_position >= len(hlal.index):
            continue  # execution day falls outside the in-sample period
        execution_day = hlal.index[next_position]
        positions.loc[execution_day] = EQUITY if above_average else parking

    return positions.ffill()


def count_trades(old_asset, new_asset):
    """Number of buy/sell legs needed to move from one holding to another."""
    if old_asset == new_asset:
        return 0
    sells = 0 if old_asset in (None, CASH) else 1
    buys = 0 if new_asset == CASH else 1
    return sells + buys


def run_backtest(prices, hlal, first_signal_day, start_day, parking, cost_per_trade):
    positions = build_positions(hlal, first_signal_day, start_day, parking)
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
    cost_factor = 1 - cost_per_trade * trades

    equity = ((1 + asset_returns) * cost_factor).cumprod()

    switches = positions[positions != positions.shift(1)]
    return equity, positions, trades, switches


def behaviour_stats(positions, trades, cost_per_trade):
    return {
        "Number of switches": len(positions[positions != positions.shift(1)]) - 1,
        "% of time parked": (positions != EQUITY).mean(),
        "Number of trades (buys + sells)": int(trades.sum()),
        "Total costs (sum of charges)": trades.sum() * cost_per_trade,
    }


def format_behaviour(name, value):
    if name in ("% of time parked", "Total costs (sum of charges)"):
        return f"{value:.2%}"
    return str(value)