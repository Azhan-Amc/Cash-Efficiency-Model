# Step 11: Purification at Wahed's published rate (5%)

Steps 7-8 used 0.8% of each HLAL dividend (third-party estimate). Wahed's published HLAL purification is 5% of every dividend, 2019 to Q2 2026.
Source: wahed.com/hlal, Quarterly Purification on HLAL Dividends (as of 30 June 2026).
Everything else is identical to step 8.

## Main test (monthly signal, 0.10% costs)

### In-sample

CAGR before and after the change:

| Version | CAGR at 0.8% | CAGR at 5% | Difference |
| --- | --- | --- | --- |
| Buy-and-hold HLAL | 20.34% | 20.29% | -0.048% |
| Rule + 0% cash | 12.88% | 12.84% | -0.038% |
| Rule + GLD (gold) | 15.61% | 15.57% | -0.039% |
| Rule + SPSK (sukuk) | 14.31% | 14.27% | -0.038% |
| Rule + T-bills (BIL, benchmark) | 13.18% | 13.14% | -0.038% |

All versions at 5% purification:

| Metric | Buy-and-hold HLAL | Rule + 0% cash | Rule + GLD (gold) | Rule + SPSK (sukuk) | Rule + T-bills (BIL, benchmark) |
| --- | --- | --- | --- | --- | --- |
| CAGR | 20.29% | 12.84% | 15.57% | 14.27% | 13.14% |
| Volatility | 18.60% | 14.45% | 16.01% | 14.72% | 14.45% |
| Max drawdown | -23.21% | -21.62% | -22.86% | -21.45% | -20.90% |
| Sharpe (risk-free 0%) | 1.09 | 0.91 | 0.99 | 0.98 | 0.93 |
| Sharpe (risk-free T-bill) | 1.00 | 0.79 | 0.88 | 0.87 | 0.81 |
| Calmar | 0.87 | 0.59 | 0.68 | 0.67 | 0.63 |

Gap: each halal option minus the T-bill version

| Halal option | Return gap per year (CAGR) | Drawdown gap (max drawdown) |
| --- | --- | --- |
| 0% cash | -0.30% | -0.72% |
| GLD (gold) | +2.43% | -1.96% |
| SPSK (sukuk) | +1.12% | -0.55% |

### Out-of-sample

CAGR before and after the change:

| Version | CAGR at 0.8% | CAGR at 5% | Difference |
| --- | --- | --- | --- |
| Buy-and-hold HLAL | 20.45% | 20.43% | -0.027% |
| Rule + 0% cash | 16.78% | 16.76% | -0.025% |
| Rule + GLD (gold) | 19.58% | 19.55% | -0.026% |
| Rule + SPSK (sukuk) | 17.30% | 17.28% | -0.025% |
| Rule + T-bills (BIL, benchmark) | 17.13% | 17.11% | -0.025% |

All versions at 5% purification:

| Metric | Buy-and-hold HLAL | Rule + 0% cash | Rule + GLD (gold) | Rule + SPSK (sukuk) | Rule + T-bills (BIL, benchmark) |
| --- | --- | --- | --- | --- | --- |
| CAGR | 20.43% | 16.76% | 19.55% | 17.28% | 17.11% |
| Volatility | 16.73% | 13.72% | 15.61% | 13.80% | 13.71% |
| Max drawdown | -21.68% | -11.97% | -14.71% | -11.97% | -11.97% |
| Sharpe (risk-free 0%) | 1.20 | 1.21 | 1.23 | 1.23 | 1.23 |
| Sharpe (risk-free T-bill) | 0.95 | 0.89 | 0.95 | 0.92 | 0.92 |
| Calmar | 0.94 | 1.40 | 1.33 | 1.44 | 1.43 |

Gap: each halal option minus the T-bill version

| Halal option | Return gap per year (CAGR) | Drawdown gap (max drawdown) |
| --- | --- | --- |
| 0% cash | -0.35% | -0.00% |
| GLD (gold) | +2.44% | -2.74% |
| SPSK (sukuk) | +0.17% | -0.00% |

## Robustness: higher costs (monthly signal, 0.25% costs)

### In-sample

CAGR before and after the change:

| Version | CAGR at 0.8% | CAGR at 5% | Difference |
| --- | --- | --- | --- |
| Buy-and-hold HLAL | 20.29% | 20.24% | -0.048% |
| Rule + 0% cash | 12.56% | 12.52% | -0.038% |
| Rule + GLD (gold) | 14.90% | 14.86% | -0.039% |
| Rule + SPSK (sukuk) | 13.60% | 13.57% | -0.038% |
| Rule + T-bills (BIL, benchmark) | 12.49% | 12.45% | -0.038% |

All versions at 5% purification:

| Metric | Buy-and-hold HLAL | Rule + 0% cash | Rule + GLD (gold) | Rule + SPSK (sukuk) | Rule + T-bills (BIL, benchmark) |
| --- | --- | --- | --- | --- | --- |
| CAGR | 20.24% | 12.52% | 14.86% | 13.57% | 12.45% |
| Volatility | 18.60% | 14.46% | 16.00% | 14.72% | 14.47% |
| Max drawdown | -23.21% | -22.09% | -23.10% | -22.39% | -21.85% |
| Sharpe (risk-free 0%) | 1.09 | 0.89 | 0.95 | 0.94 | 0.89 |
| Sharpe (risk-free T-bill) | 1.00 | 0.77 | 0.85 | 0.83 | 0.77 |
| Calmar | 0.87 | 0.57 | 0.64 | 0.61 | 0.57 |

Gap: each halal option minus the T-bill version

| Halal option | Return gap per year (CAGR) | Drawdown gap (max drawdown) |
| --- | --- | --- |
| 0% cash | +0.07% | -0.24% |
| GLD (gold) | +2.41% | -1.25% |
| SPSK (sukuk) | +1.12% | -0.54% |

### Out-of-sample

CAGR before and after the change:

| Version | CAGR at 0.8% | CAGR at 5% | Difference |
| --- | --- | --- | --- |
| Buy-and-hold HLAL | 20.45% | 20.43% | -0.027% |
| Rule + 0% cash | 16.65% | 16.63% | -0.025% |
| Rule + GLD (gold) | 19.32% | 19.29% | -0.026% |
| Rule + SPSK (sukuk) | 17.05% | 17.02% | -0.025% |
| Rule + T-bills (BIL, benchmark) | 16.88% | 16.85% | -0.025% |

All versions at 5% purification:

| Metric | Buy-and-hold HLAL | Rule + 0% cash | Rule + GLD (gold) | Rule + SPSK (sukuk) | Rule + T-bills (BIL, benchmark) |
| --- | --- | --- | --- | --- | --- |
| CAGR | 20.43% | 16.63% | 19.29% | 17.02% | 16.85% |
| Volatility | 16.73% | 13.71% | 15.61% | 13.80% | 13.71% |
| Max drawdown | -21.68% | -11.97% | -14.97% | -11.97% | -11.97% |
| Sharpe (risk-free 0%) | 1.20 | 1.20 | 1.22 | 1.22 | 1.21 |
| Sharpe (risk-free T-bill) | 0.95 | 0.88 | 0.94 | 0.90 | 0.90 |
| Calmar | 0.94 | 1.39 | 1.29 | 1.42 | 1.41 |

Gap: each halal option minus the T-bill version

| Halal option | Return gap per year (CAGR) | Drawdown gap (max drawdown) |
| --- | --- | --- |
| 0% cash | -0.22% | -0.00% |
| GLD (gold) | +2.44% | -3.00% |
| SPSK (sukuk) | +0.17% | +0.00% |

## Robustness: daily signal (0.10% costs)

### In-sample

CAGR before and after the change:

| Version | CAGR at 0.8% | CAGR at 5% | Difference |
| --- | --- | --- | --- |
| Buy-and-hold HLAL | 20.34% | 20.29% | -0.048% |
| Rule + 0% cash | 12.32% | 12.29% | -0.034% |
| Rule + GLD (gold) | 11.29% | 11.26% | -0.033% |
| Rule + SPSK (sukuk) | 12.09% | 12.06% | -0.034% |
| Rule + T-bills (BIL, benchmark) | 12.07% | 12.04% | -0.034% |

All versions at 5% purification:

| Metric | Buy-and-hold HLAL | Rule + 0% cash | Rule + GLD (gold) | Rule + SPSK (sukuk) | Rule + T-bills (BIL, benchmark) |
| --- | --- | --- | --- | --- | --- |
| CAGR | 20.29% | 12.29% | 11.26% | 12.06% | 12.04% |
| Volatility | 18.60% | 14.04% | 15.83% | 14.29% | 14.06% |
| Max drawdown | -23.21% | -24.58% | -35.07% | -26.09% | -24.59% |
| Sharpe (risk-free 0%) | 1.09 | 0.90 | 0.76 | 0.87 | 0.88 |
| Sharpe (risk-free T-bill) | 1.00 | 0.78 | 0.65 | 0.75 | 0.76 |
| Calmar | 0.87 | 0.50 | 0.32 | 0.46 | 0.49 |

Gap: each halal option minus the T-bill version

| Halal option | Return gap per year (CAGR) | Drawdown gap (max drawdown) |
| --- | --- | --- |
| 0% cash | +0.25% | +0.01% |
| GLD (gold) | -0.78% | -10.48% |
| SPSK (sukuk) | +0.02% | -1.50% |

### Out-of-sample

CAGR before and after the change:

| Version | CAGR at 0.8% | CAGR at 5% | Difference |
| --- | --- | --- | --- |
| Buy-and-hold HLAL | 20.45% | 20.43% | -0.027% |
| Rule + 0% cash | 18.42% | 18.40% | -0.023% |
| Rule + GLD (gold) | 24.44% | 24.41% | -0.025% |
| Rule + SPSK (sukuk) | 18.91% | 18.89% | -0.023% |
| Rule + T-bills (BIL, benchmark) | 18.39% | 18.37% | -0.023% |

All versions at 5% purification:

| Metric | Buy-and-hold HLAL | Rule + 0% cash | Rule + GLD (gold) | Rule + SPSK (sukuk) | Rule + T-bills (BIL, benchmark) |
| --- | --- | --- | --- | --- | --- |
| CAGR | 20.43% | 18.40% | 24.41% | 18.89% | 18.37% |
| Volatility | 16.73% | 13.17% | 15.09% | 13.25% | 13.17% |
| Max drawdown | -21.68% | -9.71% | -9.77% | -9.69% | -9.85% |
| Sharpe (risk-free 0%) | 1.20 | 1.36 | 1.53 | 1.38 | 1.36 |
| Sharpe (risk-free T-bill) | 0.95 | 1.03 | 1.25 | 1.06 | 1.03 |
| Calmar | 0.94 | 1.90 | 2.50 | 1.95 | 1.86 |

Gap: each halal option minus the T-bill version

| Halal option | Return gap per year (CAGR) | Drawdown gap (max drawdown) |
| --- | --- | --- |
| 0% cash | +0.03% | +0.15% |
| GLD (gold) | +6.05% | +0.08% |
| SPSK (sukuk) | +0.52% | +0.17% |
