"""
Performance metrics for the Cash Efficiency Model.

Every step of the backtest uses these same functions, so all versions
(buy-and-hold, rule + cash, rule + sukuk, rule + gold, rule + T-bills)
are measured in exactly the same way. This file should not change
between steps.

Definitions (from SPEC.md, section 5):
- CAGR: annual growth rate, from the initial capital to the final value.
- Volatility: standard deviation of daily returns, annualized.
- Max drawdown: worst fall from a previous peak.
- Sharpe (0%): mean daily return / std of daily returns, annualized.
  Risk-free rate = 0%, what a halal investor actually earns risk-free.
- Sharpe (T-bill): same, using daily returns in excess of BIL.
  The standard finance version, shown for comparison only.
- Calmar: CAGR / |max drawdown|.
"""

import numpy as np
import pandas as pd

TRADING_DAYS_PER_YEAR = 252


def cagr(equity, initial_capital=1.0):
    days = (equity.index[-1] - equity.index[0]).days
    years = days / 365.25
    return (equity.iloc[-1] / initial_capital) ** (1 / years) - 1


def daily_returns(equity):
    return equity.pct_change().dropna()


def volatility(returns):
    return returns.std() * np.sqrt(TRADING_DAYS_PER_YEAR)


def max_drawdown(equity, initial_capital=1.0):
    peak = equity.cummax().clip(lower=initial_capital)
    drawdown = equity / peak - 1
    return drawdown.min()


def sharpe(returns, risk_free_returns=None):
    if risk_free_returns is None:
        excess = returns
    else:
        excess = returns - risk_free_returns.reindex(returns.index)
    return excess.mean() / excess.std() * np.sqrt(TRADING_DAYS_PER_YEAR)


def calmar(equity, initial_capital=1.0):
    return cagr(equity, initial_capital) / abs(max_drawdown(equity, initial_capital))


def summarize(equity, tbill_returns, initial_capital=1.0):
    returns = daily_returns(equity)
    return {
        "Start": equity.index[0].date(),
        "End": equity.index[-1].date(),
        "Final value (start = 1.00)": equity.iloc[-1] / initial_capital,
        "CAGR": cagr(equity, initial_capital),
        "Volatility": volatility(returns),
        "Max drawdown": max_drawdown(equity, initial_capital),
        "Sharpe (risk-free 0%)": sharpe(returns),
        "Sharpe (risk-free T-bill)": sharpe(returns, tbill_returns),
        "Calmar": calmar(equity, initial_capital),
    }


def format_value(name, value):
    if name in ("CAGR", "Volatility", "Max drawdown"):
        return f"{value:.2%}"
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)