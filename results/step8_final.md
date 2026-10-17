# Step 8: Final run, out-of-sample and robustness checks

Out-of-sample: January 1, 2024 to September 30, 2026, run once. Measured from the close of the last in-sample day, continuing the rule's position. All versions purified (0.8% of HLAL dividends).

Return gap: negative means the halal option earned less than T-bills. Drawdown gap: negative means a deeper drawdown than T-bills.

## Main test (monthly signal, 0.10% costs)

### In-sample

| Metric | Buy-and-hold HLAL | Rule + 0% cash | Rule + GLD (gold) | Rule + SPSK (sukuk) | Rule + T-bills (BIL, benchmark) |
| --- | --- | --- | --- | --- | --- |
| CAGR | 20.34% | 12.88% | 15.61% | 14.31% | 13.18% |
| Volatility | 18.60% | 14.45% | 16.01% | 14.72% | 14.45% |
| Max drawdown | -23.18% | -21.60% | -22.86% | -21.43% | -20.88% |
| Sharpe (risk-free 0%) | 1.09 | 0.91 | 0.99 | 0.98 | 0.93 |
| Sharpe (risk-free T-bill) | 1.00 | 0.80 | 0.88 | 0.87 | 0.82 |
| Calmar | 0.88 | 0.60 | 0.68 | 0.67 | 0.63 |

Gap: each halal option minus the T-bill version

| Halal option | Return gap per year (CAGR) | Drawdown gap (max drawdown) |
| --- | --- | --- |
| 0% cash | -0.30% | -0.72% |
| GLD (gold) | +2.43% | -1.97% |
| SPSK (sukuk) | +1.12% | -0.55% |

### Out-of-sample

| Metric | Buy-and-hold HLAL | Rule + 0% cash | Rule + GLD (gold) | Rule + SPSK (sukuk) | Rule + T-bills (BIL, benchmark) |
| --- | --- | --- | --- | --- | --- |
| CAGR | 20.45% | 16.78% | 19.58% | 17.30% | 17.13% |
| Volatility | 16.73% | 13.72% | 15.61% | 13.79% | 13.71% |
| Max drawdown | -21.67% | -11.96% | -14.70% | -11.96% | -11.96% |
| Sharpe (risk-free 0%) | 1.20 | 1.21 | 1.23 | 1.23 | 1.23 |
| Sharpe (risk-free T-bill) | 0.95 | 0.89 | 0.96 | 0.92 | 0.92 |
| Calmar | 0.94 | 1.40 | 1.33 | 1.45 | 1.43 |

Gap: each halal option minus the T-bill version

| Halal option | Return gap per year (CAGR) | Drawdown gap (max drawdown) |
| --- | --- | --- |
| 0% cash | -0.35% | -0.00% |
| GLD (gold) | +2.44% | -2.74% |
| SPSK (sukuk) | +0.17% | -0.00% |

## Robustness: higher costs (monthly signal, 0.25% costs)

### In-sample

| Metric | Buy-and-hold HLAL | Rule + 0% cash | Rule + GLD (gold) | Rule + SPSK (sukuk) | Rule + T-bills (BIL, benchmark) |
| --- | --- | --- | --- | --- | --- |
| CAGR | 20.29% | 12.56% | 14.90% | 13.60% | 12.49% |
| Volatility | 18.60% | 14.46% | 16.00% | 14.72% | 14.47% |
| Max drawdown | -23.18% | -22.07% | -23.09% | -22.37% | -21.83% |
| Sharpe (risk-free 0%) | 1.09 | 0.89 | 0.95 | 0.95 | 0.89 |
| Sharpe (risk-free T-bill) | 1.00 | 0.78 | 0.85 | 0.83 | 0.78 |
| Calmar | 0.88 | 0.57 | 0.65 | 0.61 | 0.57 |

Gap: each halal option minus the T-bill version

| Halal option | Return gap per year (CAGR) | Drawdown gap (max drawdown) |
| --- | --- | --- |
| 0% cash | +0.07% | -0.24% |
| GLD (gold) | +2.41% | -1.26% |
| SPSK (sukuk) | +1.12% | -0.54% |

### Out-of-sample

| Metric | Buy-and-hold HLAL | Rule + 0% cash | Rule + GLD (gold) | Rule + SPSK (sukuk) | Rule + T-bills (BIL, benchmark) |
| --- | --- | --- | --- | --- | --- |
| CAGR | 20.45% | 16.65% | 19.32% | 17.05% | 16.88% |
| Volatility | 16.73% | 13.71% | 15.61% | 13.80% | 13.71% |
| Max drawdown | -21.67% | -11.96% | -14.95% | -11.96% | -11.96% |
| Sharpe (risk-free 0%) | 1.20 | 1.20 | 1.22 | 1.22 | 1.21 |
| Sharpe (risk-free T-bill) | 0.95 | 0.89 | 0.94 | 0.91 | 0.90 |
| Calmar | 0.94 | 1.39 | 1.29 | 1.43 | 1.41 |

Gap: each halal option minus the T-bill version

| Halal option | Return gap per year (CAGR) | Drawdown gap (max drawdown) |
| --- | --- | --- |
| 0% cash | -0.22% | +0.00% |
| GLD (gold) | +2.44% | -2.99% |
| SPSK (sukuk) | +0.17% | -0.00% |

## Robustness: daily signal (0.10% costs)

### In-sample

| Metric | Buy-and-hold HLAL | Rule + 0% cash | Rule + GLD (gold) | Rule + SPSK (sukuk) | Rule + T-bills (BIL, benchmark) |
| --- | --- | --- | --- | --- | --- |
| CAGR | 20.34% | 12.32% | 11.29% | 12.09% | 12.07% |
| Volatility | 18.60% | 14.04% | 15.83% | 14.29% | 14.06% |
| Max drawdown | -23.18% | -24.57% | -35.07% | -26.09% | -24.58% |
| Sharpe (risk-free 0%) | 1.09 | 0.90 | 0.76 | 0.87 | 0.88 |
| Sharpe (risk-free T-bill) | 1.00 | 0.78 | 0.65 | 0.76 | 0.77 |
| Calmar | 0.88 | 0.50 | 0.32 | 0.46 | 0.49 |

Gap: each halal option minus the T-bill version

| Halal option | Return gap per year (CAGR) | Drawdown gap (max drawdown) |
| --- | --- | --- |
| 0% cash | +0.25% | +0.01% |
| GLD (gold) | -0.78% | -10.48% |
| SPSK (sukuk) | +0.02% | -1.50% |

### Out-of-sample

| Metric | Buy-and-hold HLAL | Rule + 0% cash | Rule + GLD (gold) | Rule + SPSK (sukuk) | Rule + T-bills (BIL, benchmark) |
| --- | --- | --- | --- | --- | --- |
| CAGR | 20.45% | 18.42% | 24.44% | 18.91% | 18.39% |
| Volatility | 16.73% | 13.17% | 15.09% | 13.25% | 13.17% |
| Max drawdown | -21.67% | -9.70% | -9.77% | -9.68% | -9.85% |
| Sharpe (risk-free 0%) | 1.20 | 1.36 | 1.54 | 1.38 | 1.36 |
| Sharpe (risk-free T-bill) | 0.95 | 1.03 | 1.25 | 1.06 | 1.03 |
| Calmar | 0.94 | 1.90 | 2.50 | 1.95 | 1.87 |

Gap: each halal option minus the T-bill version

| Halal option | Return gap per year (CAGR) | Drawdown gap (max drawdown) |
| --- | --- | --- |
| 0% cash | +0.03% | +0.15% |
| GLD (gold) | +6.05% | +0.08% |
| SPSK (sukuk) | +0.52% | +0.17% |

## Out-of-sample switch log (main test)

Held at the start of 2024: HLAL. Share of out-of-sample days parked: 9.00%.

| Trade date | Now holding |
| --- | --- |
| 2025-04-01 | parking option |
| 2025-07-01 | HLAL |
