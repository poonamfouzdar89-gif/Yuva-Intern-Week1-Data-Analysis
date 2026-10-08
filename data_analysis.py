import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("StudentsPerformance.csv")

print(df.head())

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns)

print("\nDataset Information:")
df.info()

print("\nStatistical Summary:")
print(df.describe())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nUnique Values in Categorical Columns:")

print("\nGender:")
print(df["gender"].value_counts())

print("\nRace/Ethnicity:")
print(df["race/ethnicity"].value_counts())

print("\nParental Education:")
print(df["parental level of education"].value_counts())

print("\nLunch:")
print(df["lunch"].value_counts())

print("\nTest Preparation Course:")
print(df["test preparation course"].value_counts())

print("\nAverage Scores by Test Preparation Course:")

score_comparison = df.groupby("test preparation course")[
    ["math score", "reading score", "writing score"]
].mean()

print(score_comparison)

print("\nAverage Scores by Parental Level of Education:")

parent_education_scores = df.groupby("parental level of education")[
    ["math score", "reading score", "writing score"]
].mean().round(2)

print(parent_education_scores)

print("\nAverage Scores by Lunch Type:")

lunch_scores = df.groupby("lunch")[
    ["math score", "reading score", "writing score"]
].mean().round(2)

print(lunch_scores)

print("\nAverage Scores by Gender:")

gender_scores = df.groupby("gender")[
    ["math score", "reading score", "writing score"]
].mean().round(2)

print(gender_scores)


# ==============================
# STUDENT PERFORMANCE DASHBOARD
# ==============================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Test Preparation Course
score_comparison.plot(kind="bar", ax=axes[0, 0])
axes[0, 0].set_title("Average Scores by Test Preparation Course")
axes[0, 0].set_xlabel("Test Preparation Course")
axes[0, 0].set_ylabel("Average Score")
axes[0, 0].tick_params(axis="x", rotation=0)
axes[0, 0].legend(title="Subjects")

# 2. Gender
gender_scores.plot(kind="bar", ax=axes[0, 1])
axes[0, 1].set_title("Average Scores by Gender")
axes[0, 1].set_xlabel("Gender")
axes[0, 1].set_ylabel("Average Score")
axes[0, 1].tick_params(axis="x", rotation=0)
axes[0, 1].legend(title="Subjects")

# 3. Parental Education
parent_education_scores.plot(kind="bar", ax=axes[1, 0])
axes[1, 0].set_title("Average Scores by Parental Education")
axes[1, 0].set_xlabel("Parental Education")
axes[1, 0].set_ylabel("Average Score")
axes[1, 0].tick_params(axis="x", rotation=45)
axes[1, 0].legend(title="Subjects")

# 4. Lunch Type
lunch_scores.plot(kind="bar", ax=axes[1, 1])
axes[1, 1].set_title("Average Scores by Lunch Type")
axes[1, 1].set_xlabel("Lunch Type")
axes[1, 1].set_ylabel("Average Score")
axes[1, 1].tick_params(axis="x", rotation=0)
axes[1, 1].legend(title="Subjects")

plt.suptitle("Student Performance EDA Dashboard", fontsize=16)
plt.tight_layout()
plt.show()