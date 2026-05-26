# ============================================================
# HR ATTRITION PROJECT — FULL ANSWER SCRIPT
# Answers:
# Q1 Attrition rate
# Q2 Who leaves (segments)
# Q3 Why (differences & patterns)
# Q4 What matters most (stats + model)
# Q5 Actions (recommendations)
# ============================================================
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
df = pd.read_csv("data/raw/workforce_cost_raw.csv")

# ---------------------------
# 2) 4 mandatory checks
# ---------------------------

# (1) Missing values
missing = df.isnull().sum()
print("Missing values per column:\n", missing)

# Example handling (choose what fits your business logic)
# - Fill numeric nulls with 0 (common for overtime/allowance)
num_cols = df.select_dtypes(include="number").columns
df[num_cols] = df[num_cols].fillna(0)

# - Drop rows missing key identifiers (example)
key_cols = [c for c in ["employee_id", "date"] if c in df.columns]
if key_cols:
    df = df.dropna(subset=key_cols)

# (2) Duplicates
print("Duplicate rows:", df.duplicated().sum())
df = df.drop_duplicates()

# (3) Data types (examples: fix date + numeric columns if needed)
if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Convert currency-like text to numeric safely (example)
for col in ["salary", "overtime_cost", "allowance", "total_cost"]:
    if col in df.columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("AED", "", regex=False)
            .str.strip()
        )
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# (4) Business rule validation (examples)
# Remove impossible values (adjust to your rules)
for col in ["salary", "overtime_cost", "allowance", "total_cost"]:
    if col in df.columns:
        df = df[df[col] >= 0]

# Optional: Validate total_cost equals components (if columns exist)
required = {"salary", "overtime_cost", "allowance", "total_cost"}
if required.issubset(df.columns):
    df["calculated_total"] = df["salary"] + df["overtime_cost"] + df["allowance"]
    # Keep rows where difference is small (tolerance)
    tol = 1e-6
    bad = (df["total_cost"] - df["calculated_total"]).abs() > tol
    print("Rows failing total_cost rule:", bad.sum())
    # Option A: fix total_cost based on calculated_total
    df.loc[bad, "total_cost"] = df.loc[bad, "calculated_total"]
    # Option B (alternative): drop bad rows
    # df = df[~bad]

# ---------------------------
# 3) Save cleaned data to NEW CSV
# ---------------------------
output_path = "data/processed/workforce_cost_cleaned.csv"
df.to_csv(output_path, index=False)

print("Saved cleaned file to:", output_path)
print("Final rows:", len(df))




