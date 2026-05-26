# Workforce Cost Analytics & Forecasting Baseline

## Project Overview
This project analyzes monthly workforce cost trends using Python, pandas, and visualization techniques. The objective is to identify cost patterns, detect seasonal spikes, and support decision-making for workforce cost planning.

## Business Problem
Workforce cost can fluctuate due to bonuses, overtime, allowances, new joiners, and other cost drivers. Management needs a clear view of actual monthly cost, short-term trends, and normalized cost baselines to support budgeting, cash flow planning, and variance investigation.

## Dataset
The repository includes an aggregated monthly cost dataset. The analysis focuses on monthly total cost, bonus cost, overtime cost, allowance cost, employee count, moving average trend, exponential smoothing trend, and variance against the smoothed baseline.

## Tools Used
- Python
- pandas
- matplotlib
- Jupyter Notebook
- CSV outputs

## Analysis Performed
- Monthly workforce cost trend analysis
- 3-month moving average trend
- Exponential smoothing trend
- Bonus-driven year-end spike analysis
- Actual cost vs. normalized baseline comparison
- Variance analysis against the smoothed baseline

## Key Insights
- Significant year-end cost spikes were observed in both 2023 and 2024.
- The spikes were mainly driven by annual bonus payments.
- The 3-month moving average increased during these periods, reflecting short-term cost pressure.
- The exponential smoothing trend increased more gradually and did not follow the actual cost spikes at the same magnitude.
- The year-end spikes should be treated as seasonal or temporary costs unless they continue in future periods.

## Business Recommendation
Actual monthly cost should be used for cash flow planning and variance investigation. The exponential smoothing trend should be used as a normalized baseline for future cost planning. Annual bonus payments should be planned separately as seasonal cost items rather than treated as part of the normal monthly workforce cost baseline.

## Project Structure
```text
workforce-cost-analytics/
├── data/
│   └── monthly_cost_summary.csv
├── notebooks/
│   └── workforce_cost_analysis.ipynb
├── outputs/
│   └── monthly_cost_summary.csv
├── reports/
│   └── final_report.md
├── README.md
├── requirements.txt
└── LICENSE
```

## Main Output
The main output is a trend analysis comparing:
- Actual Monthly Workforce Cost
- 3-Month Moving Average Trend
- Normalized Cost Trend using Exponential Smoothing

## Conclusion
This project demonstrates the ability to prepare workforce cost data, perform trend analysis, apply moving average and exponential smoothing methods, visualize cost patterns, and translate analytical outputs into business recommendations for management decision-making.
