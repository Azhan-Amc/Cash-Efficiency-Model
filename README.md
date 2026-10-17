# Cash Efficiency Model

**How much do halal investors give up because they can't park cash in T-bills during market downturns, and which halal parking option (0% cash, gold or sukuk) closes that gap best?**

## Main finding

Using a simple 200-day trend rule on a Shariah-compliant equity ETF (HLAL), the cost of not having T-bills was small: **about 0.3% a year** when parking in 0% cash, in both the in-sample and the out-of-sample period.

- **Sukuk (SPSK)** was the most reliable halal replacement. It matched or beat T-bills on return in every test (6 of 6), with at most 1.5 points of extra drawdown.
- **Gold (GLD)** earned about 2.4% a year more than T-bills with the main rule, but with deeper drawdowns, and its result flipped negative when the signal was checked daily. Gold's result depends heavily on timing.
- **Trading costs barely mattered**, because the rule switches rarely (7 switches in 3.7 years in-sample, 2 in 2.75 years out-of-sample).
- **Purification** (0.8% of HLAL's dividends) changed returns by less than 0.01% a year.

The cost of 0% cash is roughly **the T-bill rate × the share of time parked**. Out-of-sample, T-bills paid more but the rule was parked only 9% of the time; in-sample, rates were lower but it was parked 23% of the time. Both land near 0.3% a year.

## The gap: each halal option minus the T-bill version

Main test: monthly signal, 0.10% per trade, purified.

| Halal option | In-sample return gap | Out-of-sample return gap | In-sample drawdown gap | Out-of-sample drawdown gap |
| --- | --- | --- | --- | --- |
| 0% cash | −0.30% / yr | −0.35% / yr | −0.72% | −0.00% |
| GLD (gold) | +2.43% / yr | +2.44% / yr | −1.97% | −2.74% |
| SPSK (sukuk) | +1.12% / yr | +0.17% / yr | −0.55% | −0.00% |

Negative return gap: earned less than T-bills. Negative drawdown gap: deeper drawdown than T-bills.

## Robustness checks (return gap per year)

All checks were decided before the out-of-sample run and are all reported.

| Halal option | Main test, IS / OOS | Costs 0.25%, IS / OOS | Daily signal, IS / OOS |
| --- | --- | --- | --- |
| 0% cash | −0.30% / −0.35% | +0.07% / −0.22% | +0.25% / +0.03% |
| GLD (gold) | +2.43% / +2.44% | +2.41% / +2.44% | **−0.78%** / +6.05% |
| SPSK (sukuk) | +1.12% / +0.17% | +1.12% / +0.17% | +0.02% / +0.52% |

## The rule against buy-and-hold

| | In-sample CAGR | In-sample max drawdown | Out-of-sample CAGR | Out-of-sample max drawdown |
| --- | --- | --- | --- | --- |
| Buy-and-hold HLAL | 20.35% | −23.18% | 20.45% | −21.67% |
| Rule + 0% cash | 12.89% | −21.60% | 16.78% | −11.96% |
| Rule + SPSK | 14.31% | −21.43% | 17.30% | −11.96% |
| Rule + GLD | 15.62% | −22.86% | 19.58% | −14.70% |

The rule never beat buy-and-hold on return. Its protection depended on the type of decline: in the 2022 bear market it exited late and barely reduced the drawdown; in 2025 it exited on April 1, just before the tariff sell-off, and cut the drawdown almost in half. That is one event and the timing was partly lucky, so it is not evidence that the rule reliably protects.

## Limitations

- Short history: HLAL and SPSK start in 2019, so the test covers about 6 years and only a few real downturns.
- The test misses the 2020 Covid crash, because the 200-day signal only starts around May 2020.
- Out-of-sample, the rule was parked only about 3 months, so the out-of-sample gap rests on very little parked time.
- GLD is used as a gold example (certified under the AAOIFI Shari'ah Standard on Gold); Manzil's own gold ETF is not public.
- Purification uses a third-party estimate (0.8% of dividends), not Wahed's published figures.
- Gold can fall sharply too: GLD fell 10.3% in one day on January 30, 2026.

## Research discipline

- The full design ([SPEC.md](SPEC.md)) was written on October 16, 2026, before any strategy result was produced.
- In-sample: first valid signal (May 2020) to December 31, 2023. Out-of-sample: January 1, 2024 to September 30, 2026, run once.
- The final script was tested on synthetic data before the out-of-sample run. It was committed to this repository after the run, so the commit history does not by itself prove that ordering.
- No rule was changed after seeing results.
- Every instrument held passed a halal check (SPEC.md, section 6). T-bills are used only as a benchmark and never held.

## How to run

```
pip install yfinance pandas
python load_data.py
python load_dividends.py
python step2_buy_and_hold.py
python step3_rule_cash.py
python step4_rule_gold.py
python step5_rule_sukuk.py
python step6_tbill_comparison.py
python step7_purification.py
python step8_final.py
```

Price data is downloaded from Yahoo Finance and not included in this repository. Results for each step are saved in `results/`.

## Files

| Step | File | What it does |
| --- | --- | --- |
| 1 | `load_data.py` | Downloads dividend-adjusted prices and checks data quality |
| — | `load_dividends.py` | Downloads HLAL dividends for purification |
| — | `metrics.py` | All performance metrics, shared by every step |
| — | `backtest.py` | The 200-day rule, shared by steps 3 to 8 |
| 2 | `step2_buy_and_hold.py` | Buy-and-hold baseline, in-sample |
| 3 | `step3_rule_cash.py` | Rule parking in 0% cash, in-sample |
| 4 | `step4_rule_gold.py` | Rule parking in GLD, in-sample |
| 5 | `step5_rule_sukuk.py` | Rule parking in SPSK, in-sample |
| 6 | `step6_tbill_comparison.py` | T-bill benchmark and the gap, in-sample |
| 7 | `step7_purification.py` | Purification applied to every version, in-sample |
| 8 | `step8_final.py` | Out-of-sample run and all robustness checks |

## Next

- Run the same test on the Russell IdealRatings Manzil Halal USA Broad Market Index (MNZL's index) for a longer history, if index data can be obtained. It will be added to the spec before running.