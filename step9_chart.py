"""
Cash Efficiency Model - Step 9: chart for the paper.

Draws the main test (monthly signal, 0.10% costs, purified) over the full
period, May 2020 to September 2026:
- top panel: growth of 1 dollar for all five versions
- bottom panel: drawdown from the previous peak
- grey bands: months the rule was parked
- dashed line: start of the out-of-sample period

Uses the functions from step 8 unchanged, so the curves are exactly the
ones behind the paper's tables. Nothing is recalculated differently.

Saves results/figure1_growth_and_drawdown.png (for the paper) and .svg.

Requires prices.csv and dividends_hlal.csv, and matplotlib:
    pip install matplotlib
"""

from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

from backtest import CASH, EQUITY, run_backtest
from step2_buy_and_hold import COST_PER_TRADE, find_start_date
from step8_final import OUT_OF_SAMPLE_START, load_full_prices, purify_full_period, run_scenario

OUTPUT_PNG = Path("results") / "figure1_growth_and_drawdown.png"
OUTPUT_SVG = Path("results") / "figure1_growth_and_drawdown.svg"

SURFACE = "#fcfcfb"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
GRID = "#e4e3df"
PARKED_BAND = "#ecebe7"

# Series: halal options take the first three categorical slots (validated
# all-pairs); the two reference lines are neutral, so colour marks the options
# the paper compares. Identity is also carried by direct labels and line style.
SERIES = {
    "Buy-and-hold HLAL": {"label": "Buy-and-hold", "color": "#a3a29c", "style": "-"},
    "Rule + T-bills (BIL, benchmark)": {"label": "Rule + T-bills (benchmark)", "color": TEXT_PRIMARY, "style": "--"},
    "Rule + 0% cash": {"label": "Rule + 0% cash", "color": "#2a78d6", "style": "-"},
    "Rule + GLD (gold)": {"label": "Rule + gold", "color": "#eb6834", "style": "-"},
    "Rule + SPSK (sukuk)": {"label": "Rule + sukuk", "color": "#1baf7a", "style": "-"},
}


def parked_periods(prices, hlal, first_signal_day, start_day):
    """(start, end) date pairs when the main-test rule was out of HLAL."""
    _, positions, _, _ = run_backtest(prices, hlal, first_signal_day, start_day, CASH, COST_PER_TRADE)
    parked = positions != EQUITY
    periods, start = [], None
    for day, is_parked in parked.items():
        if is_parked and start is None:
            start = day
        elif not is_parked and start is not None:
            periods.append((start, day))
            start = None
    if start is not None:
        periods.append((start, parked.index[-1]))
    return periods


def drawdown(equity):
    return equity / equity.cummax().clip(lower=1.0) - 1


def place_end_labels(ax, values, min_gap):
    """Spread end-of-line labels vertically so they never overlap."""
    order = sorted(values.items(), key=lambda item: item[1])
    placed = []
    for name, value in order:
        y = value if not placed else max(value, placed[-1][1] + min_gap)
        placed.append((name, y))
    return dict(placed)


def style_axis(ax):
    ax.set_facecolor(SURFACE)
    ax.grid(axis="y", color=GRID, linewidth=0.6)
    ax.grid(axis="x", visible=False)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY, labelsize=8, length=0)


def main():
    prices = load_full_prices()
    hlal = prices["HLAL"].dropna()
    first_signal_day, start_day = find_start_date(hlal)
    purified = purify_full_period(prices, hlal)

    equities = run_scenario(purified, hlal, first_signal_day, start_day, daily=False, cost=COST_PER_TRADE)
    periods = parked_periods(purified, hlal, first_signal_day, start_day)
    split_day = pd.Timestamp(OUT_OF_SAMPLE_START)

    fig, (top, bottom) = plt.subplots(
        2, 1, figsize=(7.5, 6.2), sharex=True, gridspec_kw={"height_ratios": [2.2, 1]}, facecolor=SURFACE
    )
    fig.subplots_adjust(left=0.08, right=0.74, top=0.9, bottom=0.08, hspace=0.12)

    for ax in (top, bottom):
        style_axis(ax)
        for start, end in periods:
            ax.axvspan(start, end, color=PARKED_BAND, linewidth=0, zorder=0)
        ax.axvline(split_day, color=TEXT_SECONDARY, linewidth=0.8, linestyle=(0, (2, 2)), zorder=1)

    # Draw neutral reference lines first so the halal options sit on top.
    for name, spec in SERIES.items():
        equity = equities[name]
        top.plot(equity.index, equity.values, color=spec["color"], linestyle=spec["style"],
                 linewidth=1.5, label=spec["label"], zorder=3, solid_capstyle="round")
        bottom.plot(equity.index, drawdown(equity).values * 100, color=spec["color"],
                    linestyle=spec["style"], linewidth=1.2, zorder=3)

    ends = {name: equities[name].iloc[-1] for name in SERIES}
    y_low, y_high = top.get_ylim()
    label_y = place_end_labels(top, ends, min_gap=0.055 * (y_high - y_low))
    last_day = equities["Buy-and-hold HLAL"].index[-1]
    label_x = last_day + pd.Timedelta(days=25)
    for name, spec in SERIES.items():
        top.annotate(
            f"{spec['label']}  {ends[name]:.2f}",
            xy=(last_day, ends[name]), xytext=(label_x, label_y[name]), textcoords="data",
            va="center", fontsize=8, color=TEXT_PRIMARY, annotation_clip=False,
            arrowprops={"arrowstyle": "-", "color": spec["color"], "linewidth": 0.8, "shrinkA": 0, "shrinkB": 2},
        )

    top.set_ylabel("Growth of $1", fontsize=8, color=TEXT_SECONDARY)
    bottom.set_ylabel("Drawdown (%)", fontsize=8, color=TEXT_SECONDARY)
    top.text(split_day, top.get_ylim()[1], "  Out-of-sample →", fontsize=8,
             color=TEXT_SECONDARY, va="top", ha="left")
    top.text(split_day, top.get_ylim()[1], "← In-sample  ", fontsize=8,
             color=TEXT_SECONDARY, va="top", ha="right")

    bottom.xaxis.set_major_locator(mdates.YearLocator())
    bottom.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    top.legend(loc="upper left", fontsize=8, frameon=False, labelcolor=TEXT_PRIMARY, handlelength=2.2)

    fig.suptitle("Figure 1. Growth of $1 and drawdown, monthly 200-day rule, May 2020 to September 2026",
                 x=0.08, ha="left", fontsize=9.5, color=TEXT_PRIMARY)
    fig.text(0.08, 0.925, "Grey bands: months the rule was parked. After 0.10% trading costs and purification.",
             fontsize=8, color=TEXT_SECONDARY)

    OUTPUT_PNG.parent.mkdir(exist_ok=True)
    fig.savefig(OUTPUT_PNG, dpi=300, facecolor=SURFACE)
    fig.savefig(OUTPUT_SVG, facecolor=SURFACE)
    print(f"Saved {OUTPUT_PNG} and {OUTPUT_SVG}")
    print("Parked periods:")
    for start, end in periods:
        print(f"  {start.date()} to {end.date()}")


if __name__ == "__main__":
    main()