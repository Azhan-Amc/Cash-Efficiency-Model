# Cash Efficiency Model

**How much do halal investors give up because they can't park cash in T-bills during market downturns, and which halal parking option (0% cash, gold or sukuk) closes that gap best?**

## Main finding

Using a simple monthly 200-day trend rule on a Shariah-compliant equity ETF (HLAL), the cost of not having T-bills was small: **about 0.5% a year before trading costs and about 0.3% after** when parking in 0% cash, in both the in-sample and the out-of-sample period.

- **Sukuk (SPSK)** was the most reliable halal replacement in this sample. It matched or beat T-bills on return in every test (6 of 6), with at most 1.5 points of extra drawdown. These tests cover only a few parked episodes, so this is a measurement, not a statistically established result.
- **Gold (GLD)** earned about 2.4% a year more than T-bills with the main rule, but with deeper drawdowns, and its result flipped negative when the signal was checked daily. Gold's result depends heavily on timing.
- **Trading costs barely mattered**, because the rule switches rarely (7 switches in 3.7 years in-sample, 2 in 2.75 years out-of-sample).
- **Purification** at Wahed's published rate (5% of HLAL's dividends) lowered returns by at most 0.05% a year and left every return gap unchanged.
- **Gold fund:** replacing GLD with GLDM, the gold ETF listed in the Corex Halal Portfolio, changed the gold gap by at most 0.08% a year.

The cost of 0% cash is roughly **the T-bill return earned while parked, minus the extra cost of trading a T-bill fund** (two trades per switch instead of one). Out-of-sample, T-bills paid more but the rule was parked only 9% of the time; in-sample, rates were lower but it was parked 23% of the time. Both land near 0.5% a year before costs and 0.3% after. At 0.25% per trade, cash comes out slightly ahead in-sample (+0.07% a year).

## The gap: each halal option minus the T-bill version

Main test: monthly signal, 0.10% per trade, purified.

The tables below are step 8's output, purified at the earlier 0.8% estimate. At Wahed's published 5% rate (step 11), every return gap is the same to two decimals and no figure moves by more than 0.05 points.

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
- GLD is used as the gold example (certified under the AAOIFI Shari'ah Standard on Gold). The Corex Halal Portfolio lists SPDR Gold MiniShares (GLDM) instead; step 10 reruns every test with GLDM, and the gold gap changes by at most 0.08% a year.
- Purification uses Wahed's published figures: 5% of every HLAL dividend from 2019 to Q2 2026. This appears to be a flat rate equal to the AAOIFI ceiling, not a ratio measured each year. Steps 7 and 8 used an earlier third-party estimate (0.8%), which was replaced after the out-of-sample run (step 11).
- The signal uses dividend-adjusted HLAL prices; the spec says "closing price" without specifying.
- Gold can fall sharply too: GLD fell 10.3% in one day on January 30, 2026.
- The benchmark is US T-bills in US dollars. For an investor in Canadian dollars, the forgone rate is the Canadian T-bill rate, which was lower than the US rate for much of 2025, so their cost was likely somewhat lower. Currency effects are not modelled.

## Research discipline

- The rule, dates, costs and metrics in [SPEC.md](SPEC.md) were fixed on October 16, 2026, before any data was loaded. Three choices were fixed after the in-sample results but before the out-of-sample run: the purification rate, measuring the out-of-sample period continuously, and running both robustness checks on both periods.
- SPEC.md was first committed after the in-sample results, so the commit history does not prove the order above. The study was not preregistered.
- In-sample: first valid signal (May 2020) to December 31, 2023. Out-of-sample: January 1, 2024 to September 30, 2026, run once.
- The final script was tested on synthetic data before the out-of-sample run. It was committed to this repository after the run, so the commit history does not by itself prove that ordering.
- No rule was changed after seeing results. One input was corrected after the out-of-sample run: the purification rate, from the 0.8% estimate to Wahed's published 5% (step 11).
- Every number from steps 2 to 8 (at 0.8% purification) was reproduced exactly by a second, separately written implementation (`audit/independent_check.py`). It was written by the same author with AI assistance, so it is an internal cross-check, not a third-party replication.
- Every instrument held passed a halal check (SPEC.md, section 6). T-bills are used only as a benchmark and never held.

## Use of AI

The author chose the research question, made all methodological decisions and ran the analysis. Code and text were drafted with the assistance of an AI model (Claude, Anthropic) and reviewed by the author. Every figure from steps 2 to 8 was reproduced by a second, separately written implementation (`audit/independent_check.py`).

## How to run

```
pip install yfinance pandas numpy matplotlib
python load_data.py
python load_dividends.py
python step2_buy_and_hold.py
python step3_rule_cash.py
python step4_rule_gold.py
python step5_rule_sukuk.py
python step6_tbill_comparison.py
python step7_purification.py
python step8_final.py
python step9_chart.py
python step10_gold_gldm.py
python step11_purification_wahed.py
python 12_parking_options_on_their_own.py
```

To cross-check the results with the separate implementation, run `python audit/independent_check.py .` from the repository root.

Price data is downloaded from Yahoo Finance and not included in this repository. Results for each step are saved in `results/`.

## Files

| Step | File | What it does |
| --- | --- | --- |
| 1 | `load_data.py` | Downloads dividend-adjusted prices and checks data quality |
| — | `load_dividends.py` | Downloads HLAL dividends for purification |
| — | `metrics.py` | All performance metrics, shared by every step |
| — | `backtest.py` | The 200-day rule, shared by the step scripts |
| 2 | `step2_buy_and_hold.py` | Buy-and-hold baseline, in-sample |
| 3 | `step3_rule_cash.py` | Rule parking in 0% cash, in-sample |
| 4 | `step4_rule_gold.py` | Rule parking in GLD, in-sample |
| 5 | `step5_rule_sukuk.py` | Rule parking in SPSK, in-sample |
| 6 | `step6_tbill_comparison.py` | T-bill benchmark and the gap, in-sample |
| 7 | `step7_purification.py` | Purification applied to every version, in-sample |
| 8 | `step8_final.py` | Out-of-sample run and all robustness checks |
| 9 | `step9_chart.py` | Figure 1 of the paper: growth of $1 and drawdowns |
| 10 | `step10_gold_gldm.py` | Same as step 8, parking in GLDM instead of GLD |
| 11 | `step11_purification_wahed.py` | Same as step 8, purified at Wahed's published 5% |
| 12 | `12_parking_options_on_their_own.py` | Each parking asset on its own: risk, correlation with HLAL, returns in drawdowns (saved in `results/step12/`) |
| — | `audit/independent_check.py` | Separate re-implementation that reproduces steps 2 to 8 |

## Next

- Run the same test on the Russell IdealRatings Manzil Halal USA Broad Market Index (MNZL's index) for a longer history, if index data can be obtained. It will be added to the spec before running.
