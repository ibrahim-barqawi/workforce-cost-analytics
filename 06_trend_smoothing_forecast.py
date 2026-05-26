# ============================================================
# E) Basic Forecasting / Trend Smoothing
# Moving Average & Exponential Smoothing
# ============================================================
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# 1) Load raw data
df = pd.read_csv("/Users/ibrahimbarqawi/Desktop/Data Analysis _Course and projects /Codes/11-workforce-cost-analytics/data/processed/workforce_cost_cleaned.csv")


# Monthly total workforce cost
monthly_cost = df.groupby('year_month')['total_cost'].sum().reset_index()

# Convert year_month to datetime
monthly_cost['year_month'] = pd.to_datetime(monthly_cost['year_month'])

# Sort by month
monthly_cost = monthly_cost.sort_values('year_month')

# 3-month moving average
monthly_cost['moving_avg_3m'] = monthly_cost['total_cost'].rolling(window=3).mean()

# Exponential smoothing
monthly_cost['exp_smoothing'] = monthly_cost['total_cost'].ewm(alpha=0.3, adjust=False).mean()

print(monthly_cost)

# Plot combined trend
plt.figure(figsize=(10, 5))

plt.plot(monthly_cost['year_month'], monthly_cost['total_cost'], marker='o', label='Actual Cost')
plt.plot(monthly_cost['year_month'], monthly_cost['moving_avg_3m'], marker='o', label='3-Month Moving Average')
plt.plot(monthly_cost['year_month'], monthly_cost['exp_smoothing'], marker='o', label='Exponential Smoothing')

plt.title('Monthly Workforce Cost Trend Analysis')
plt.xlabel('Month')
plt.ylabel('Total Workforce Cost')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

PLOT_DIR= '/Users/ibrahimbarqawi/Desktop/Data Analysis _Course and projects /Codes/11-workforce-cost-analytics/outputs'
plt.savefig(os.path.join(PLOT_DIR, "monthly_cost_trend_analysis.png"), dpi=300)
plt.show()

# Save output
OUTPUT_DIR ='/Users/ibrahimbarqawi/Desktop/Data Analysis _Course and projects /Codes/11-workforce-cost-analytics/outputs'
monthly_cost.to_excel(
    os.path.join(OUTPUT_DIR, "monthly_cost_forecasting_analysis.xlsx"),
    index=False
)



