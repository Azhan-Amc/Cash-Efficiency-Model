# Step 14: The rule parking in the sukuk + gold basket

Basket locked in step 13 (2004-2019 data): **65% SPSK + 35% GLD**, rebalanced at each monthly check while parked.
Purification: 5% of HLAL dividends (Wahed). Same rule, dates, costs and scenarios as the paper.

Not a fresh out-of-sample test: SPSK's and GLD's 2020-2026 results were already known. The weights were not fitted to them. The clean test is forward from the lock date.

Self-check: the engine reproduces backtest.py exactly for 100% cash, SPSK and GLD (largest difference 2.0e-15).

Return gap: negative means the halal option earned less than T-bills. Drawdown gap: negative means a deeper drawdown than T-bills.

## Main test (monthly signal, 0.10% costs)

### In-sample

| Metric | Buy-and-hold HLAL | Rule + 0% cash | Rule + GLD (gold) | Rule + SPSK (sukuk) | Rule + Basket (SPSK + GLD) | Rule + T-bills (BIL, benchmark) |
| --- | --- | --- | --- | --- | --- | --- |
| CAGR | 20.29% | 12.84% | 15.57% | 14.27% | 14.76% | 13.14% |
| Volatility | 18.60% | 14.45% | 16.01% | 14.72% | 14.85% | 14.45% |
| Max drawdown | -23.21% | -21.62% | -22.86% | -21.45% | -20.81% | -20.90% |
| Sharpe (risk-free 0%) | 1.09 | 0.91 | 0.99 | 0.98 | 1.00 | 0.93 |
| Sharpe (risk-free T-bill) | 1.00 | 0.79 | 0.88 | 0.87 | 0.89 | 0.81 |
| Calmar | 0.87 | 0.59 | 0.68 | 0.67 | 0.71 | 0.63 |

Gap: each halal option minus the T-bill version

| Halal option | Return gap per year (CAGR) | Drawdown gap (max drawdown) |
| --- | --- | --- |
| 0% cash | -0.30% | -0.72% |
| GLD (gold) | +2.43% | -1.96% |
| SPSK (sukuk) | +1.12% | -0.55% |
| Basket (SPSK + GLD) | +1.62% | +0.10% |

Basket trading: 6 monthly rebalances costing 0.011% in total; all basket trading costs 2.125%.

### Out-of-sample

| Metric | Buy-and-hold HLAL | Rule + 0% cash | Rule + GLD (gold) | Rule + SPSK (sukuk) | Rule + Basket (SPSK + GLD) | Rule + T-bills (BIL, benchmark) |
| --- | --- | --- | --- | --- | --- | --- |
| CAGR | 20.43% | 16.76% | 19.55% | 17.28% | 18.08% | 17.11% |
| Volatility | 16.73% | 13.72% | 15.61% | 13.80% | 14.02% | 13.71% |
| Max drawdown | -21.68% | -11.97% | -14.71% | -11.97% | -12.55% | -11.97% |
| Sharpe (risk-free 0%) | 1.20 | 1.21 | 1.23 | 1.23 | 1.26 | 1.23 |
| Sharpe (risk-free T-bill) | 0.95 | 0.89 | 0.95 | 0.92 | 0.96 | 0.92 |
| Calmar | 0.94 | 1.40 | 1.33 | 1.44 | 1.44 | 1.43 |

Gap: each halal option minus the T-bill version

| Halal option | Return gap per year (CAGR) | Drawdown gap (max drawdown) |
| --- | --- | --- |
| 0% cash | -0.35% | -0.00% |
| GLD (gold) | +2.44% | -2.74% |
| SPSK (sukuk) | +0.17% | -0.00% |
| Basket (SPSK + GLD) | +0.98% | -0.58% |

Basket trading: 2 monthly rebalances costing 0.007% in total; all basket trading costs 0.740%.

## Robustness: higher costs (monthly signal, 0.25% costs)

### In-sample

| Metric | Buy-and-hold HLAL | Rule + 0% cash | Rule + GLD (gold) | Rule + SPSK (sukuk) | Rule + Basket (SPSK + GLD) | Rule + T-bills (BIL, benchmark) |
| --- | --- | --- | --- | --- | --- | --- |
| CAGR | 20.24% | 12.52% | 14.86% | 13.57% | 14.05% | 12.45% |
| Volatility | 18.60% | 14.46% | 16.00% | 14.72% | 14.84% | 14.47% |
| Max drawdown | -23.21% | -22.09% | -23.10% | -22.39% | -21.76% | -21.85% |
| Sharpe (risk-free 0%) | 1.09 | 0.89 | 0.95 | 0.94 | 0.97 | 0.89 |
| Sharpe (risk-free T-bill) | 1.00 | 0.77 | 0.85 | 0.83 | 0.85 | 0.77 |
| Calmar | 0.87 | 0.57 | 0.64 | 0.61 | 0.65 | 0.57 |

Gap: each halal option minus the T-bill version

| Halal option | Return gap per year (CAGR) | Drawdown gap (max drawdown) |
| --- | --- | --- |
| 0% cash | +0.07% | -0.24% |
| GLD (gold) | +2.41% | -1.25% |
| SPSK (sukuk) | +1.12% | -0.54% |
| Basket (SPSK + GLD) | +1.60% | +0.09% |

Basket trading: 6 monthly rebalances costing 0.027% in total; all basket trading costs 5.256%.

### Out-of-sample

| Metric | Buy-and-hold HLAL | Rule + 0% cash | Rule + GLD (gold) | Rule + SPSK (sukuk) | Rule + Basket (SPSK + GLD) | Rule + T-bills (BIL, benchmark) |
| --- | --- | --- | --- | --- | --- | --- |
| CAGR | 20.43% | 16.63% | 19.29% | 17.02% | 17.82% | 16.85% |
| Volatility | 16.73% | 13.71% | 15.61% | 13.80% | 14.02% | 13.71% |
| Max drawdown | -21.68% | -11.97% | -14.97% | -11.97% | -12.81% | -11.97% |
| Sharpe (risk-free 0%) | 1.20 | 1.20 | 1.22 | 1.22 | 1.25 | 1.21 |
| Sharpe (risk-free T-bill) | 0.95 | 0.88 | 0.94 | 0.90 | 0.94 | 0.90 |
| Calmar | 0.94 | 1.39 | 1.29 | 1.42 | 1.39 | 1.41 |

Gap: each halal option minus the T-bill version

| Halal option | Return gap per year (CAGR) | Drawdown gap (max drawdown) |
| --- | --- | --- |
| 0% cash | -0.22% | -0.00% |
| GLD (gold) | +2.44% | -3.00% |
| SPSK (sukuk) | +0.17% | -0.00% |
| Basket (SPSK + GLD) | +0.97% | -0.84% |

Basket trading: 2 monthly rebalances costing 0.016% in total; all basket trading costs 1.805%.

## Robustness: daily signal (0.10% costs)

### In-sample

| Metric | Buy-and-hold HLAL | Rule + 0% cash | Rule + GLD (gold) | Rule + SPSK (sukuk) | Rule + Basket (SPSK + GLD) | Rule + T-bills (BIL, benchmark) |
| --- | --- | --- | --- | --- | --- | --- |
| CAGR | 20.29% | 12.29% | 11.26% | 12.06% | 11.83% | 12.04% |
| Volatility | 18.60% | 14.04% | 15.83% | 14.29% | 14.48% | 14.06% |
| Max drawdown | -23.21% | -24.58% | -35.07% | -26.09% | -28.85% | -24.59% |
| Sharpe (risk-free 0%) | 1.09 | 0.90 | 0.76 | 0.87 | 0.85 | 0.88 |
| Sharpe (risk-free T-bill) | 1.00 | 0.78 | 0.65 | 0.75 | 0.73 | 0.76 |
| Calmar | 0.87 | 0.50 | 0.32 | 0.46 | 0.41 | 0.49 |

Gap: each halal option minus the T-bill version

| Halal option | Return gap per year (CAGR) | Drawdown gap (max drawdown) |
| --- | --- | --- |
| 0% cash | +0.25% | +0.01% |
| GLD (gold) | -0.78% | -10.48% |
| SPSK (sukuk) | +0.02% | -1.50% |
| Basket (SPSK + GLD) | -0.21% | -4.26% |

Basket trading: 9 monthly rebalances costing 0.013% in total; all basket trading costs 6.062%.

### Out-of-sample

| Metric | Buy-and-hold HLAL | Rule + 0% cash | Rule + GLD (gold) | Rule + SPSK (sukuk) | Rule + Basket (SPSK + GLD) | Rule + T-bills (BIL, benchmark) |
| --- | --- | --- | --- | --- | --- | --- |
| CAGR | 20.43% | 18.40% | 24.41% | 18.89% | 20.83% | 18.37% |
| Volatility | 16.73% | 13.17% | 15.09% | 13.25% | 13.50% | 13.17% |
| Max drawdown | -21.68% | -9.71% | -9.77% | -9.69% | -9.69% | -9.85% |
| Sharpe (risk-free 0%) | 1.20 | 1.36 | 1.53 | 1.38 | 1.48 | 1.36 |
| Sharpe (risk-free T-bill) | 0.95 | 1.03 | 1.25 | 1.06 | 1.16 | 1.03 |
| Calmar | 0.94 | 1.90 | 2.50 | 1.95 | 2.15 | 1.86 |

Gap: each halal option minus the T-bill version

| Halal option | Return gap per year (CAGR) | Drawdown gap (max drawdown) |
| --- | --- | --- |
| 0% cash | +0.03% | +0.15% |
| GLD (gold) | +6.05% | +0.08% |
| SPSK (sukuk) | +0.52% | +0.17% |
| Basket (SPSK + GLD) | +2.46% | +0.17% |

Basket trading: 2 monthly rebalances costing 0.008% in total; all basket trading costs 3.626%.

## The basket on its own (no trend rule), next to each option

A. Standalone risk

| Period | Asset | CAGR | Volatility | Max drawdown | Worst month |
| --- | --- | --- | --- | --- | --- |
| In-sample | HLAL | 20.38% | 18.60% | -23.18% | -8.86% |
| In-sample | SPSK | 0.02% | 5.16% | -12.83% | -4.17% |
| In-sample | GLD | 5.02% | 14.71% | -22.00% | -7.15% |
| In-sample | Basket | 1.95% | 6.79% | -14.81% | -3.71% |
| In-sample | BIL | 1.68% | 0.25% | -0.16% | -0.02% |
| Out-of-sample | HLAL | 20.46% | 16.73% | -21.67% | -6.20% |
| Out-of-sample | SPSK | 2.40% | 5.28% | -3.37% | -2.62% |
| Out-of-sample | GLD | 28.43% | 22.11% | -26.40% | -11.68% |
| Out-of-sample | Basket | 11.26% | 9.04% | -10.33% | -5.17% |
| Out-of-sample | BIL | 4.36% | 0.22% | -0.01% | 0.27% |

B. Correlation of daily returns with HLAL

| Period | SPSK | GLD | Basket | BIL |
| --- | --- | --- | --- | --- |
| In-sample | 0.27 | 0.16 | 0.25 | -0.00 |
| Out-of-sample | 0.22 | 0.21 | 0.26 | -0.06 |

C. Return during each HLAL drawdown of 10% or more (peak close to trough close)

| Peak | Trough | HLAL | SPSK | GLD | Basket | BIL |
| --- | --- | --- | --- | --- | --- | --- |
| 2020-02-19 | 2020-03-23 | -33.57% | -4.88% | -3.62% | -4.43% | 0.26% |
| 2022-01-03 | 2022-10-12 | -23.18% | -10.18% | -7.33% | -9.07% | 0.61% |
| 2024-12-17 | 2025-04-08 | -21.67% | 0.71% | 12.81% | 4.90% | 1.29% |
| 2026-01-28 | 2026-03-30 | -10.20% | -1.30% | -16.17% | -6.82% | 0.60% |
