# ============================================================
#C) Overtime Analysis

#Calculate:

#Overtime cost as % of total cost

#Avg overtime hours per employee

#Departments with highest overtime cost %

#Use your flag:

#% of rows with ot_inefficiency_flag = True

#📌 Insight example (you’ll write your own):

#Operations shows high overtime dependency, indicating workload imbalance rather than headcount shortage.
# ============================================================
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import openpyxl

from scipy.stats import chi2_contingency, mannwhitneyu




# 1) Load raw data
df = pd.read_csv("/Users/ibrahimbarqawi/Desktop/Data Analysis _Course and projects /Codes/11-workforce-cost-analytics/data/processed/workforce_cost_cleaned.csv")
#============================
#Overtime Analysis
#============================

#***************************************
#Overtime cost as % of total cost
#***************************************
OT_pc = ((df['overtime_cost'].sum()/df['total_cost'].sum())*100).round(2)

print(f'Over Time cost percentage from the total is : {OT_pc}%' )

heads = {'Overtime Percentage' : OT_pc }

OT_perct = pd.DataFrame(heads, index = [0])

#***************************************
#Avg overtime hours per employee
#***************************************

avg_ot = df.groupby('employee_id')['overtime_hours'].mean().round(2)
overall_avg_ot = avg_ot.mean().round(2)

average_overtime = avg_ot.reset_index()
average_overtime.columns = ['employee_id', 'avg_overtime_hours']


N = 10
top_employees_ot = avg_ot.nlargest(N).reset_index()
top_employees_ot.columns = ['employee_id', 'avg_overtime_hours']
print(top_employees_ot)


plt.figure(figsize=(10, 6))
top_employees_ot.plot(kind='bar')
plt.title("Top employees with OT")
plt.ylabel("Hours")
plt.xticks(rotation=45)
plt.tight_layout()


path ='/Users/ibrahimbarqawi/Desktop/Data Analysis _Course and projects /Codes/11-workforce-cost-analytics/outputs/Overtime Analysis/top_employees_ot.png'
plt.savefig(path, dpi=300, bbox_inches='tight')
plt.show()

#******************************************
#Departments with highest overtime cost %
#******************************************

cost_dept = df.groupby('department')['total_cost'].sum()

ot_dept = df.groupby('department')['overtime_cost'].sum()

Avgdpt_OT = ((ot_dept / cost_dept)*100).round(2).sort_values(ascending=False).reset_index()
Avgdpt_OT.columns = ['department', 'overtime_cost_pct']



plt.figure(figsize=(10, 6))
Avgdpt_OT.plot(kind='bar')
plt.title("Overtime Cost % by Department")
plt.ylabel("Overtime cost %")
plt.xticks(rotation=45)
plt.tight_layout()



path ='/Users/ibrahimbarqawi/Desktop/Data Analysis _Course and projects /Codes/11-workforce-cost-analytics/outputs/Overtime Analysis/Overtime cost per Department.png'
plt.savefig(path, dpi=300, bbox_inches='tight')

plt.show()

#============================
#% of rows with ot_inefficiency_flag = True
#============================
df['ot_inefficiency_flag'] = (
    (df['overtime_hours'] > 20) &
    ((df['overtime_cost'] / df['total_cost']) > 0.2)
)

flag_pct = round(df['ot_inefficiency_flag'].mean() * 100, 2)

print(f"% of rows with ot_inefficiency_flag = True: {flag_pct}%")
#============================
#Saving Data
#============================
print('Saving Data ....')

summary = pd.DataFrame({
    'Metric':['OT % Total Cost','Avg OT Hours','Inefficiency Flag %'],
    'Value':[OT_pc, overall_avg_ot, flag_pct]
})

file_name = 'Overtime Analysis.xlsx'
path = '/Users/ibrahimbarqawi/Desktop/Data Analysis _Course and projects /Codes/11-workforce-cost-analytics/outputs/Overtime Analysis/Overtime Analysis.xlsx'
with pd.ExcelWriter(path, engine='openpyxl') as writer:
    OT_perct.to_excel(writer, sheet_name='Overtime percentage', index=False)
    average_overtime.to_excel(writer, sheet_name='Overtime hours', index=False)
    Avgdpt_OT.to_excel(writer, sheet_name='Departments with highest OT', index=False)
    summary.to_excel(writer,sheet_name = "Summary" , index = False)

print(f"Successfully created '{file_name}' with three sheets.")

