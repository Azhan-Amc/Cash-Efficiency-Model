# Step 10: Gold parking with GLDM instead of GLD

Only the gold ETF changes. Same rule, dates, costs, purification and out-of-sample convention as step 8.
The GLD columns should match step 8 exactly; if they don't, something is wrong.

Return gap: negative means the first option earned less. Drawdown gap: negative means a deeper drawdown.

## Main test (monthly signal, 0.10% costs)

### In-sample

| Metric | Buy-and-hold HLAL | Rule + GLD (paper) | Rule + GLDM (Corex holding) | Rule + T-bills (BIL, benchmark) |
| --- | --- | --- | --- | --- |
| CAGR | 20.34% | 15.61% | 15.64% | 13.18% |
| Volatility | 18.60% | 16.01% | 15.99% | 14.45% |
| Max drawdown | -23.18% | -22.86% | -22.78% | -20.88% |
| Sharpe (risk-free 0%) | 1.09 | 0.99 | 0.99 | 0.93 |
| Sharpe (risk-free T-bill) | 1.00 | 0.88 | 0.89 | 0.82 |
| Calmar | 0.88 | 0.68 | 0.69 | 0.63 |

| Comparison | Return gap per year (CAGR) | Drawdown gap (max drawdown) |
| --- | --- | --- |
| GLD minus T-bills | +2.43% | -1.97% |
| GLDM minus T-bills | +2.46% | -1.90% |
| GLDM minus GLD | +0.03% | +0.07% |

### Out-of-sample

| Metric | Buy-and-hold HLAL | Rule + GLD (paper) | Rule + GLDM (Corex holding) | Rule + T-bills (BIL, benchmark) |
| --- | --- | --- | --- | --- |
| CAGR | 20.45% | 19.58% | 19.58% | 17.13% |
| Volatility | 16.73% | 15.61% | 15.59% | 13.71% |
| Max drawdown | -21.67% | -14.70% | -14.48% | -11.96% |
| Sharpe (risk-free 0%) | 1.20 | 1.23 | 1.23 | 1.23 |
| Sharpe (risk-free T-bill) | 0.95 | 0.96 | 0.96 | 0.92 |
| Calmar | 0.94 | 1.33 | 1.35 | 1.43 |

| Comparison | Return gap per year (CAGR) | Drawdown gap (max drawdown) |
| --- | --- | --- |
| GLD minus T-bills | +2.44% | -2.74% |
| GLDM minus T-bills | +2.45% | -2.52% |
| GLDM minus GLD | +0.00% | +0.21% |

## Robustness: higher costs (monthly signal, 0.25% costs)

### In-sample

| Metric | Buy-and-hold HLAL | Rule + GLD (paper) | Rule + GLDM (Corex holding) | Rule + T-bills (BIL, benchmark) |
| --- | --- | --- | --- | --- |
| CAGR | 20.29% | 14.90% | 14.93% | 12.49% |
| Volatility | 18.60% | 16.00% | 15.98% | 14.47% |
| Max drawdown | -23.18% | -23.09% | -23.02% | -21.83% |
| Sharpe (risk-free 0%) | 1.09 | 0.95 | 0.96 | 0.89 |
| Sharpe (risk-free T-bill) | 1.00 | 0.85 | 0.85 | 0.78 |
| Calmar | 0.88 | 0.65 | 0.65 | 0.57 |

| Comparison | Return gap per year (CAGR) | Drawdown gap (max drawdown) |
| --- | --- | --- |
| GLD minus T-bills | +2.41% | -1.26% |
| GLDM minus T-bills | +2.44% | -1.18% |
| GLDM minus GLD | +0.03% | +0.07% |

### Out-of-sample

| Metric | Buy-and-hold HLAL | Rule + GLD (paper) | Rule + GLDM (Corex holding) | Rule + T-bills (BIL, benchmark) |
| --- | --- | --- | --- | --- |
| CAGR | 20.45% | 19.32% | 19.32% | 16.88% |
| Volatility | 16.73% | 15.61% | 15.58% | 13.71% |
| Max drawdown | -21.67% | -14.95% | -14.74% | -11.96% |
| Sharpe (risk-free 0%) | 1.20 | 1.22 | 1.22 | 1.21 |
| Sharpe (risk-free T-bill) | 0.95 | 0.94 | 0.94 | 0.90 |
| Calmar | 0.94 | 1.29 | 1.31 | 1.41 |

| Comparison | Return gap per year (CAGR) | Drawdown gap (max drawdown) |
| --- | --- | --- |
| GLD minus T-bills | +2.44% | -2.99% |
| GLDM minus T-bills | +2.44% | -2.78% |
| GLDM minus GLD | +0.00% | +0.21% |

## Robustness: daily signal (0.10% costs)

### In-sample

| Metric | Buy-and-hold HLAL | Rule + GLD (paper) | Rule + GLDM (Corex holding) | Rule + T-bills (BIL, benchmark) |
| --- | --- | --- | --- | --- |
| CAGR | 20.34% | 11.29% | 11.37% | 12.07% |
| Volatility | 18.60% | 15.83% | 15.81% | 14.06% |
| Max drawdown | -23.18% | -35.07% | -35.05% | -24.58% |
| Sharpe (risk-free 0%) | 1.09 | 0.76 | 0.76 | 0.88 |
| Sharpe (risk-free T-bill) | 1.00 | 0.65 | 0.66 | 0.77 |
| Calmar | 0.88 | 0.32 | 0.32 | 0.49 |

| Comparison | Return gap per year (CAGR) | Drawdown gap (max drawdown) |
| --- | --- | --- |
| GLD minus T-bills | -0.78% | -10.48% |
| GLDM minus T-bills | -0.70% | -10.46% |
| GLDM minus GLD | +0.08% | +0.02% |

### Out-of-sample

| Metric | Buy-and-hold HLAL | Rule + GLD (paper) | Rule + GLDM (Corex holding) | Rule + T-bills (BIL, benchmark) |
| --- | --- | --- | --- | --- |
| CAGR | 20.45% | 24.44% | 24.46% | 18.39% |
| Volatility | 16.73% | 15.09% | 15.07% | 13.17% |
| Max drawdown | -21.67% | -9.77% | -9.74% | -9.85% |
| Sharpe (risk-free 0%) | 1.20 | 1.54 | 1.54 | 1.36 |
| Sharpe (risk-free T-bill) | 0.95 | 1.25 | 1.25 | 1.03 |
| Calmar | 0.94 | 2.50 | 2.51 | 1.87 |

| Comparison | Return gap per year (CAGR) | Drawdown gap (max drawdown) |
| --- | --- | --- |
| GLD minus T-bills | +6.05% | +0.08% |
| GLDM minus T-bills | +6.06% | +0.11% |
| GLDM minus GLD | +0.02% | +0.03% |
