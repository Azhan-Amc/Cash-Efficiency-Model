# Cash Efficiency Model — Research Spec

Oct 16, 2026 · @Mohammad Azhan Chowdhry

## Status

All six sections are locked as of October 16, 2026. Prices have been loaded and checked for data quality only; no strategy results have been seen.

| Section | Status |
| --- | --- |
| 1. Research question | Locked |
| 2. Instruments | Locked |
| 3. The rule | Locked |
| 4. Dates | Locked |
| 5. What we measure | Locked |
| 6. Halal check per instrument | Locked |

## 1. Research question

How much return and risk do halal investors give up because they can't park cash in T-bills during market downturns, and which halal parking option (0% cash, gold, or sukuk) closes that gap best?

The goal is to measure the gap honestly. Any result is a valid finding, including "no option closes it" or "the gap is small". The rule is not tuned to produce a good return.

## 2. Instruments

The test uses real ETFs that investors can actually hold, with about 6 years of history. The short sample is a stated limitation.

| Role | Instrument | Data starts | Why |
| --- | --- | --- | --- |
| Equity | HLAL (Wahed FTSE USA Shariah ETF) | July 15, 2019 | Held in the Corex Halal Portfolio that Manzil clients own |
| Parking 1 | 0% cash | n/a | The halal baseline: parked money earns nothing |
| Parking 2 | SPSK (SP Funds Dow Jones Global Sukuk ETF) | December 30, 2019 | Held in the Corex Halal Portfolio |
| Parking 3 | GLD (SPDR Gold Shares) | November 18, 2004 | Certified under the AAOIFI Shari'ah Standard on Gold; used as an example until Manzil's own gold ticker is confirmed |
| Benchmark only | BIL (SPDR Bloomberg 1-3 Month T-Bill ETF) | May 2007 | Measures what conventional investors earn while parked. Not held. |

MNZL is excluded because it launched in November 2025, too recently to test.

## 3. The rule

Hold HLAL when its price is above its 200-day moving average; otherwise hold the parking option. All parameters are fixed in advance and are not tuned.

1. **Signal:** HLAL closing price compared with its 200-day simple moving average.
2. **Check frequency:** monthly, on the last trading day of each month.
3. **Execution:** trade at the close of the next trading day, so no trade uses information that wasn't available yet.
4. **Trading costs:** 0.10% per trade in the main test (a switch = sell + buy = 0.20%). Based on SPSK's published median spread of 0.06% and HLAL's typical regular-hours spread.

## 4. Dates

All dates were fixed on October 16, 2026, before any data was loaded or results observed.

| Period | Dates | Reason |
| --- | --- | --- |
| Start | First month-end with a valid 200-day signal (around May 2020) | Forced by the data: HLAL starts July 15, 2019 and needs 200 trading days. Calculated by the code, not chosen. |
| In-sample | Start to December 31, 2023 | Used to build and check the code. Contains one full cycle (2022 bear market, 2023 recovery). About 44 months. |
| Out-of-sample | January 1, 2024 to September 30, 2026 | Locked. Run once at the end, reported as is. Ends at the last complete month before this spec was written. About 33 months. |

The split is roughly 57/43, close to the common 60/40 convention, and cuts at a calendar year end rather than a market event.

## 5. What we measure

Every metric is calculated for each version: buy-and-hold HLAL, rule + 0% cash, rule + SPSK, rule + GLD, and rule + T-bills (benchmark only).

| Group | Metric | What it shows |
| --- | --- | --- |
| Performance | Annual return (CAGR) | Average yearly growth |
| Performance | Annualized volatility | How much it swings |
| Performance | Max drawdown | Worst fall from peak to low |
| Risk-adjusted | Sharpe ratio, risk-free = 0% (main) | Return per unit of risk, against what a halal investor actually earns risk-free |
| Risk-adjusted | Sharpe ratio, risk-free = T-bill rate (shown alongside) | The standard finance version, for comparison |
| Risk-adjusted | Calmar ratio (CAGR ÷ max drawdown) | Rewards avoiding big crashes |
| Behaviour | Number of switches | How often the rule moved in and out |
| Behaviour | % of time parked | How long money sat in the parking option |
| Behaviour | Total costs paid | Impact of trading costs |
| The gap (main result) | Return gap vs T-bill version, per year | What each halal option costs compared to T-bills |
| The gap (main result) | Drawdown gap vs T-bill version | Difference in crash protection |

## 6. Halal check per instrument

Every instrument must pass a halal check before it is included in any test. GLD is included as the gold example; Manzil's own gold ticker is to be confirmed later.

| Instrument | Evidence | Status |
| --- | --- | --- |
| HLAL | Tracks the FTSE Shariah USA Index, screened by Yasaar Limited and certified by fatwa; Wahed publishes a fund Shariah certificate, annual Shariah board reports (2021–2024) and quarterly purification amounts ([HalalWallet](https://www.halalwallet.us/providers/wahed-invest/wahed-ftse-usa-shariah-etf), [Wahed Shariah page](https://www.wahed.com/shariah)); held in the Corex Halal Portfolio | Passed |
| SPSK | Holds AAOIFI-screened, investment-grade sukuk; SP Funds states no purification is needed because sukuk income is not interest ([HalalWallet](https://www.halalwallet.us/providers/spfunds/sp-funds-dow-jones-global-sukuk-etf), [Zoya](https://zoya.finance/stocks/spsk)); held in the Corex Halal Portfolio. Note: the certifying scholars are not named on SP Funds' site | Passed, with that note |
| 0% cash | Non-interest account | Halal by definition |
| Gold | Candidate: GLD (SPDR Gold Shares), certified in 2017 by Amanie Advisors as compliant with the AAOIFI Shari'ah Standard on Gold ([The Asset](https://theasset.com/asset-management/32474/theasset.com)). Data from 2004. Manzil's own gold ticker is still unknown | Included as an example; confirm Manzil's own ticker later |
| T-bills | Never held; used only to measure the gap | No check needed |

**Purification.** HLAL's dividends are reduced by the purification amount. Main source: Wahed's published quarterly per-share purification amounts. Fallback if those can't be obtained: a third-party estimate of about 0.8% of dividends, clearly labeled as an estimate. If neither is usable, purification is left out of the numbers and stated as a limitation. Because HLAL's dividend yield is small (well under 1% a year), the expected effect on returns is tiny.

## Robustness checks and limitations

Each robustness check runs only after the main test is finished, with the same rules unchanged.

- **Longer history:** the same test on a halal index with a longer history.
- **Daily signal:** the same rule checked daily instead of monthly.
- **Higher costs:** 0.25% per trade instead of 0.10%.

Known limitations:

- About 6 years of data, with only a few real downturns.
- The test misses the 2020 Covid crash, because the 200-day signal only starts around May 2020.