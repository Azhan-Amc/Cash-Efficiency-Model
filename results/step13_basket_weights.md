# Step 13: Choosing the parking basket's weights (2004-2019, before HLAL)

Calibration window: 2004-11-18 to 2019-06-27. Signal: SPY vs its 200-day average, checked monthly, traded next close (same rule as the paper).
Share of days parked: 19.26%. Parked episodes: 8.

## The decision

| | Gold (GLD) | Sukuk proxy (PREMX) |
| --- | --- | --- |
| Volatility, parked weeks only | 23.58% | 13.69% |
| Inverse-volatility weight (unrounded) | 36.7% | 63.3% |
| **Locked weight (rounded to 5%)** | **35% GLD** | **65% SPSK** |

Correlation of gold and the sukuk proxy, parked weeks: 0.14 (all weeks: 0.15).

In step 14 the sukuk weight is held in SPSK and the gold weight in GLD. Rebalanced to these weights at each monthly check while parked.

## How reliable is the weight?

Bootstrap, 10,000 resamples of whole parked episodes: sukuk weight 5th percentile 62.1%, median 63.3%, 95th percentile 68.5%.
Share of resamples within 10 points of the locked 65%: 100.0%.

For context, the same rule on ALL weeks (parked or not) would give: gold 17.57% vol, sukuk proxy 8.41% vol, sukuk weight 67.6%. Not used.

## Each parked episode, 2004-2019 (locked weights)

| Parked from | Parked to | Trading days | Gold (GLD) | Sukuk proxy (PREMX) | Basket | 0% cash |
| --- | --- | --- | --- | --- | --- | --- |
| 2008-01-03 | 2009-06-01 | 355 | 12.81% | -4.38% | 2.17% | 0.00% |
| 2010-06-02 | 2010-10-01 | 86 | 7.51% | 10.79% | 9.76% | 0.00% |
| 2011-09-02 | 2012-01-03 | 84 | -12.34% | -1.91% | -5.50% | 0.00% |
| 2015-09-02 | 2015-11-02 | 43 | -0.56% | 2.21% | 1.24% | 0.00% |
| 2016-01-05 | 2016-04-01 | 61 | 13.65% | 5.22% | 8.24% | 0.00% |
| 2018-11-02 | 2018-12-03 | 21 | -0.19% | -0.41% | -0.33% | 0.00% |
| 2019-01-03 | 2019-03-01 | 40 | 0.45% | 5.97% | 4.02% | 0.00% |
| 2019-06-04 | 2019-06-27 | 18 | 6.18% | 2.86% | 4.02% | 0.00% |

25% of episodes lasted about one month or less, so monthly rebalancing rarely triggers more than once.

## Odds per episode

| Option | Episodes | Share of episodes with a loss | Average episode return | Median episode return | Worst episode | Best episode |
| --- | --- | --- | --- | --- | --- | --- |
| Gold (GLD) | 8 | 37.50% | 3.44% | 3.32% | -12.34% | 13.65% |
| Sukuk proxy (PREMX) | 8 | 37.50% | 2.54% | 2.54% | -4.38% | 10.79% |
| Basket | 8 | 25.00% | 2.95% | 3.09% | -5.50% | 9.76% |
| 0% cash | 8 | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |

## Proxy check (information only, does not affect the weights)

Weekly correlation PREMX vs SPSK, 2020-01-02 to 2026-09-30: 0.67. Annualized weekly volatility: PREMX 10.49%, SPSK 3.99%.

## Notes

- SPY and PREMX are measuring tools only. They are not halal instruments and are never held.
- PREMX holds conventional emerging-market bonds. Its duration and credit mix differ from SPSK's, so its volatility is an estimate of sukuk risk, not a copy of it.
- 0% cash is left out of the basket: at a 0% risk-free rate it changes the risk level, not the efficiency.
