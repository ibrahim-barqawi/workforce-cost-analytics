# ============================================================
#B) Cost Breakdown (VERY IMPORTANT)

#Break down total_cost by:

#Cost component:

#base_salary

#overtime_cost

#allowance_cost

#bonus_cost

#Department

#Project

#***Which cost component contributes the most, and why?***
# ============================================================

import os
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("/Users/ibrahimbarqawi/Desktop/Data Analysis _Course and projects /Codes/11-workforce-cost-analytics/data/processed/workforce_cost_cleaned.csv")

# Output folder
output_dir = "/Users/ibrahimbarqawi/Desktop/Data Analysis _Course and projects /Codes/11-workforce-cost-analytics/outputs/Cost Breakdown"
os.makedirs(output_dir, exist_ok=True)

# Cost components
break_down = ['base_salary', 'overtime_cost', 'allowance_cost', 'bonus_cost']

# ============================
# 1) Overall component totals
# ============================
component_totals = df[break_down].sum().sort_values(ascending=False)
component_pct = ((component_totals / component_totals.sum()) * 100).round(2)

summary_df = pd.DataFrame({
    'total_amount': component_totals,
    'contribution_pct': component_pct
}).reset_index().rename(columns={'index': 'cost_component'})

print(summary_df)

# Identify highest contributor
top_component = component_totals.idxmax()
top_value = component_totals.max()
top_pct = component_pct[top_component]

print(f"\nTop cost component: {top_component}")
print(f"Total value: {top_value:,.2f}")
print(f"Contribution %: {top_pct}%")

# ============================
# 2) Department breakdown
# ============================
dept_breakdown = df.groupby('department')[break_down].sum().round(2)
print("\nDepartment breakdown:")
print(dept_breakdown)

# ============================
# 3) Project breakdown
# ============================
project_breakdown = df.groupby('project')[break_down].sum().round(2)
print("\nProject breakdown:")
print(project_breakdown)

# ============================
# 4) Save outputs
# ============================
summary_df.to_csv(os.path.join(output_dir, "cost_component_summary.csv"), index=False)
dept_breakdown.to_csv(os.path.join(output_dir, "department_cost_breakdown.csv"))
project_breakdown.to_csv(os.path.join(output_dir, "project_cost_breakdown.csv"))

with pd.ExcelWriter(os.path.join(output_dir, "cost_breakdown_summary.xlsx"), engine="openpyxl") as writer:
    summary_df.to_excel(writer, sheet_name="ComponentSummary", index=False)
    dept_breakdown.to_excel(writer, sheet_name="DepartmentBreakdown")
    project_breakdown.to_excel(writer, sheet_name="ProjectBreakdown")

# ============================
# 5) Plot overall component contribution
# ============================
plt.figure(figsize=(10, 6))
component_totals.plot(kind='bar')
plt.title("Total Workforce Cost by Cost Component")
plt.ylabel("Total Cost")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ============================
# 6) Save styled HTML
# ============================
html_table = summary_df.style.highlight_max(subset=['total_amount', 'contribution_pct'], axis=0)
html_str = html_table.to_html()

html_path = os.path.join(output_dir, "cost_component_summary.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_str)
