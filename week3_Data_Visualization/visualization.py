
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load dataset
df = pd.read_csv("StudentsPerformance.csv")

# 2. Create output folder
os.makedirs("outputs", exist_ok=True)

# 3. Prepare subject score columns
subjects = ["math score", "reading score", "writing score"]
average_scores = df[subjects].mean()

sns.set_theme(style="whitegrid")

# Chart 1: Average scores bar chart
plt.figure(figsize=(8, 5))
sns.barplot(x=average_scores.index, y=average_scores.values)
plt.title("Average Scores by Subject")
plt.xlabel("Subject")
plt.ylabel("Average Score")
plt.ylim(0, 100)
plt.tight_layout()
plt.savefig("outputs/1_average_scores.png", dpi=300)
plt.close()

# Chart 2: Score distribution
plt.figure(figsize=(9, 5))
for subject in subjects:
    sns.kdeplot(data=df, x=subject, label=subject, fill=False)
plt.title("Distribution of Student Scores")
plt.xlabel("Score")
plt.ylabel("Density")
plt.legend()
plt.tight_layout()
plt.savefig("outputs/2_score_distribution.png", dpi=300)
plt.close()

# Chart 3: Maths vs Reading scatter plot
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="math score", y="reading score", alpha=0.6)
plt.title("Math Score vs Reading Score")
plt.xlabel("Math Score")
plt.ylabel("Reading Score")
plt.tight_layout()
plt.savefig("outputs/3_math_vs_reading.png", dpi=300)
plt.close()

# Chart 4: Subject score correlation heatmap
plt.figure(figsize=(7, 5))
correlation = df[subjects].corr()
sns.heatmap(correlation, annot=True, cmap="coolwarm",
            vmin=-1, vmax=1, fmt=".2f")
plt.title("Correlation Between Subject Scores")
plt.tight_layout()
plt.savefig("outputs/4_score_correlation.png", dpi=300)
plt.close()

# 4. Save numerical summary
summary = df[subjects].agg(["mean", "median", "min", "max"]).round(2)
summary.to_csv("outputs/score_summary.csv")

# 5. Print key findings
print("Dataset shape:", df.shape)
print("\nAverage scores:")
print(average_scores.round(2))

print("\nCorrelation matrix:")
print(correlation.round(2))

print("\nAll charts and summary saved in the outputs folder.")

# Chart 5: Student score trends
plt.figure(figsize=(10, 5))

plt.plot(df.index + 1, df["math score"], label="Math", alpha=0.7)
plt.plot(df.index + 1, df["reading score"], label="Reading", alpha=0.7)
plt.plot(df.index + 1, df["writing score"], label="Writing", alpha=0.7)

plt.title("Student Scores Across Dataset Records")
plt.xlabel("Student Record Number")
plt.ylabel("Score")
plt.legend()
plt.tight_layout()

plt.savefig("outputs/5_student_score_trends.png", dpi=300)
plt.close()

print("Line chart saved successfully!")