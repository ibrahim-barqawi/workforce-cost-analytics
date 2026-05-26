# ============================================================
#D) Allowance Analysis

#Allowance cost as % of total cost
#Allowance distribution by job level
#% of rows flagged as high_allowance_flag
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import openpyxl
import os 



# 1) Load raw data and creating the output file 
df = pd.read_csv("/Users/ibrahimbarqawi/Desktop/Data Analysis _Course and projects /Codes/11-workforce-cost-analytics/data/processed/workforce_cost_cleaned.csv")
path ='/Users/ibrahimbarqawi/Desktop/Data Analysis _Course and projects /Codes/11-workforce-cost-analytics/outputs/D) Allowance Analysis'
os.makedirs(path, exist_ok=True)
#============================
##D) Allowance Analysis
#============================
#===========================================
#1-Allowance cost as % of total cost
#===========================================
Allowance_Cost_Percentage = ((df['allowance_cost'].sum()/df['total_cost'].sum())*100).round(2)

allowance_pct = pd.DataFrame({'Allowance Percentage ': Allowance_Cost_Percentage},index = [0])

print(f'The percentage of allowance cost from the total cost is {Allowance_Cost_Percentage}%')

#===========================================
#2-#Allowance distribution by job level
#===========================================
Allowance_distribution = df.groupby('job_level')['allowance_cost'].mean().round(2)

print(Allowance_distribution)


plt.figure(figsize=(10, 6))
Allowance_distribution.plot(kind='bar')
plt.title("Allowance Distribution By job level")
plt.ylabel("allowance cost average")
plt.xticks(rotation=45)
plt.tight_layout()

pic_path = path +'/Allowance_distribution_by_job_level.png'
plt.savefig(pic_path, dpi=300, bbox_inches='tight')

plt.show()

#===========================================
#3-% of rows flagged as high_allowance_flag
#===========================================
allowance_percentage = (df['allowance_cost']/df['total_cost'] *100).round(2)

df['high_allowance_flag'] = allowance_percentage.apply(lambda x: 'High' if x >= 20 else 'Normal')

pct = (df['high_allowance_flag'].value_counts().get('High', 0)/len(df['high_allowance_flag'])*100).round(2)
allowance_pct = pd.DataFrame({'high_allowance_flag ': pct},index = [0])
print(pct)
print(df['high_allowance_flag'].value_counts().get('High', 0))
print(len(df['high_allowance_flag'])*100)


#============================
#Saving Data
#============================
print('Saving Data ....')

excel_path = path +'/Allowance_Analysis_report.xlsx'

with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    allowance_pct.to_excel(writer, sheet_name="Avgcostpertotal", index=False)
    Allowance_distribution.reset_index().to_excel(writer,sheet_name = "Allowance Vs Job level" , index = False)
    allowance_pct.to_excel(writer, sheet_name = 'high allowance flag data', index = False)

print("File successfuly saved")
