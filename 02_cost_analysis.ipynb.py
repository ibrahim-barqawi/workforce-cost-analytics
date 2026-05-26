# ============================================================
#A) Overall Cost KPIs

#Total workforce cost (entire period)

#Average monthly workforce cost

#Average cost per employee

#Month-over-month cost growth (%)
# ============================================================
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import openpyxl

from scipy.stats import chi2_contingency, mannwhitneyu

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler  # ✅ HERE
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score, RocCurveDisplay
)
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier



# 1) Load raw data
df = pd.read_csv("/Users/ibrahimbarqawi/Desktop/Data Analysis _Course and projects /Codes/11-workforce-cost-analytics/data/processed/workforce_cost_cleaned.csv")
#============================
#A) Overall Cost KPIs
#============================
## 1) Total workforce cost over entire period (by year)
year_total = df.groupby('year')['total_cost'].sum().round(2)
print(year_total)

plt.figure(figsize=(8, 4))
year_total.plot(kind="bar")
plt.title("Total Workforce Cost by Year")
plt.ylabel("Total Cost")
plt.tight_layout()
plt.show()

# 2) Monthly total cost + average monthly workforce cost
monthly_total = df.groupby('year_month')['total_cost'].sum().round(2)
avg_monthly_cost = monthly_total.mean().round(2)

print(monthly_total)
print("Average monthly workforce cost:", avg_monthly_cost)

plt.figure(figsize=(10, 4))
monthly_total.plot(kind="line")
plt.title("Monthly Total Workforce Cost")
plt.ylabel("Total Cost")
plt.tight_layout()
plt.show()

# 3) Average cost per employee (avg monthly cost per employee)
avg_emp_cost = df.groupby('employee_id')['total_cost'].mean().round(2)
overall_avg_emp_cost = avg_emp_cost.mean().round(2)

print(avg_emp_cost.head(10))
print("Overall average cost per employee (monthly):", overall_avg_emp_cost)

plt.figure(figsize=(8, 4))
avg_emp_cost.sort_values(ascending=False).head(10).plot(kind="bar")
plt.title("Top 10 Employees by Average Monthly Cost")
plt.ylabel("Avg Monthly Cost")
plt.tight_layout()
plt.show()

# 4) Month-over-month cost growth (%)


monthly_cost = (
    df.groupby('year_month')['total_cost']
      .sum()
      .sort_index()
)

mom_growth = monthly_cost.pct_change().round(2)

print(mom_growth)

plt.figure(figsize=(10, 4))
mom_growth.plot(kind="line", marker="o")
plt.axhline(0, linestyle="--")
plt.title("Month-over-Month Workforce Cost Growth (%)")
plt.ylabel("Growth (%)")
plt.xlabel("Year-Month")
plt.tight_layout()
plt.show()

#============================
#Saving Data
#============================
print('Saving Data ....')
monthly_kpis = (
    pd.concat(
        [monthly_cost, mom_growth],
        axis=1
    )
    .reset_index().round(2)
)


monthly_kpis.columns = ["year_month", "total_cost", "mom_growth_pct"]

monthly_kpis.to_csv(
    '/Users/ibrahimbarqawi/Desktop/Data Analysis _Course and projects /Codes/11-workforce-cost-analytics/outputs/monthly_cost_summary.csv',
    index=False
)

print("monthly_cost_summary.csv saved")

path =  '/Users/ibrahimbarqawi/Desktop/Data Analysis _Course and projects /Codes/11-workforce-cost-analytics/outputs/monthly_cost_summary.xlsx'

#new_sheet = path.create_sheet("AvgEmpCost", index=1)
#avg_emp_cost.to_csv(path,sheet_name="AvgEmpCost", index=False)

with pd.ExcelWriter(path, engine='openpyxl', mode='a') as writer:
    # 3. Create the new sheet and save the data
    avg_emp_cost.to_excel(writer, sheet_name="AvgEmpCost", index=False)
