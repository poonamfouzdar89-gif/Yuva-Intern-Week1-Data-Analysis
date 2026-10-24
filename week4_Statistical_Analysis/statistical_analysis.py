
import pandas as pd
from scipy import stats
from pathlib import Path

# Folder paths
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "StudentsPerformance.csv"
OUTPUT_FILE = BASE_DIR / "statistical_results.csv"

# Load dataset
df = pd.read_csv(DATA_FILE)

print("Dataset shape:", df.shape)
print("\nMissing values:", df.isnull().sum().sum())

results = []

def save_result(test_name, hypothesis, statistic, p_value, details=""):
    alpha = 0.05
    conclusion = (
        "Reject the null hypothesis (statistically significant)"
        if p_value < alpha
        else "Fail to reject the null hypothesis (not statistically significant)"
    )
    results.append({
        "Test": test_name,
        "Null Hypothesis": hypothesis,
        "Statistic": statistic,
        "P-value": p_value,
        "Conclusion at 5%": conclusion,
        "Details": details
    })
    print(f"\n{test_name}")
    print(f"Statistic: {statistic:.4f}")
    print(f"P-value: {p_value:.6g}")
    print(conclusion)

# 1. Independent t-test:
# Math scores of students who completed test preparation vs none
completed = df.loc[
    df["test preparation course"] == "completed", "math score"
].dropna()
none = df.loc[
    df["test preparation course"] == "none", "math score"
].dropna()

t_stat, t_p = stats.ttest_ind(completed, none, equal_var=False)
mean_diff = completed.mean() - none.mean()

# Welch confidence interval for difference in means
se = ((completed.var(ddof=1) / len(completed)) +
      (none.var(ddof=1) / len(none))) ** 0.5

df_welch = (
    (completed.var(ddof=1) / len(completed) +
     none.var(ddof=1) / len(none)) ** 2
    /
    (
        (completed.var(ddof=1) / len(completed)) ** 2 / (len(completed) - 1)
        +
        (none.var(ddof=1) / len(none)) ** 2 / (len(none) - 1)
    )
)

critical_t = stats.t.ppf(0.975, df_welch)
ci_low = mean_diff - critical_t * se
ci_high = mean_diff + critical_t * se

save_result(
    "Welch independent t-test",
    "Mean math scores are equal for completed and non-completed test preparation groups",
    t_stat,
    t_p,
    f"Completed mean={completed.mean():.2f}; "
    f"None mean={none.mean():.2f}; difference={mean_diff:.2f}; "
    f"95% CI for difference=({ci_low:.2f}, {ci_high:.2f})"
)

# 2. One-way ANOVA:
# Math scores across parental education groups
groups = [
    group["math score"].dropna().to_numpy()
    for _, group in df.groupby("parental level of education")
]
f_stat, anova_p = stats.f_oneway(*groups)

save_result(
    "One-way ANOVA",
    "Mean math scores are equal across all parental education groups",
    f_stat,
    anova_p,
    "Compares mean math scores across parental education categories"
)

# 3. Pearson correlation:
# Reading and writing scores
r, corr_p = stats.pearsonr(df["reading score"], df["writing score"])

save_result(
    "Pearson correlation",
    "There is no linear correlation between reading and writing scores",
    r,
    corr_p,
    f"Pearson r={r:.4f}"
)

# Save all test results
pd.DataFrame(results).to_csv(OUTPUT_FILE, index=False)

print("\nResults saved to:", OUTPUT_FILE)
print("\nMean scores by test preparation:")
print(df.groupby("test preparation course")[
    ["math score", "reading score", "writing score"]
].mean().round(2))
