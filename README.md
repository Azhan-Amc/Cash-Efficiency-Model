# Cash Efficiency Model

How much return and risk do halal investors give up because they can't park cash in T-bills during market downturns, and which halal parking option (0% cash, gold, or sukuk) closes that gap best?

This project tests a simple risk-off rule on a Shariah-compliant equity ETF:

- **Hold HLAL** (Wahed FTSE USA Shariah ETF) when its price is above its 200-day moving average.
- **Otherwise park** in one of three halal options: 0% cash, SPSK (sukuk) or GLD (gold).
- **Compare** each halal version with the same rule using T-bills (BIL), which halal investors can't hold, to measure the gap.

The full research design (instruments, rule, dates, metrics and halal checks) is in [SPEC.md](SPEC.md). It was written and committed before any strategy results were produced.

## Research discipline

- All rules and dates were fixed on October 16, 2026, before running any backtest.
- In-sample period: first valid signal (around May 2020) to December 31, 2023.
- Out-of-sample period: January 1, 2024 to September 30, 2026. Locked and run once, at the end.
- Every instrument held passes a halal check before inclusion (see SPEC.md, section 6).

## How to run

```
pip install yfinance pandas
python load_data.py
```

`load_data.py` downloads daily prices (adjusted for dividends) and checks the data for missing days and unusual moves. It saves them to `prices.csv`, which is not included in this repository; run the script to recreate it.

## Progress

| Step | File | Status |
| --- | --- | --- |
| 1. Load and check data | `load_data.py` | Done |
| 2. Buy-and-hold baseline | | Next |
| 3. 200-day rule with 0% cash | | |
| 4. Parking in gold | | |
| 5. Parking in sukuk | | |
| 6. Comparison with T-bill version | | |