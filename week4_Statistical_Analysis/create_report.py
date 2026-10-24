
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

BASE = Path(__file__).resolve().parent
DATA = BASE / "StudentsPerformance.csv"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

REPORT = BASE / "Week4_Statistical_Analysis_Report.docx"

# ---------- Load and validate data ----------
df = pd.read_csv(DATA)
required = [
    "math score", "reading score", "writing score",
    "test preparation course", "parental level of education"
]
missing_columns = [c for c in required if c not in df.columns]
if missing_columns:
    raise ValueError(f"Dataset columns missing: {missing_columns}")

for col in ["math score", "reading score", "writing score"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

n_rows, n_cols = df.shape
missing_total = int(df[required].isna().sum().sum())

# ---------- Test 1: Welch independent t-test ----------
completed = df.loc[
    df["test preparation course"] == "completed", "math score"
].dropna()
not_completed = df.loc[
    df["test preparation course"] == "none", "math score"
].dropna()

t_stat, t_p = stats.ttest_ind(
    completed, not_completed, equal_var=False
)
mean_completed = completed.mean()
mean_none = not_completed.mean()
mean_diff = mean_completed - mean_none

var1, var2 = completed.var(ddof=1), not_completed.var(ddof=1)
n1, n2 = len(completed), len(not_completed)
se_diff = np.sqrt(var1 / n1 + var2 / n2)

df_welch = (var1 / n1 + var2 / n2) ** 2 / (
    (var1 / n1) ** 2 / (n1 - 1) +
    (var2 / n2) ** 2 / (n2 - 1)
)
critical = stats.t.ppf(0.975, df_welch)
t_ci = (mean_diff - critical * se_diff,
        mean_diff + critical * se_diff)

# Cohen's d using pooled standard deviation
pooled_sd = np.sqrt(
    ((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2)
)
cohens_d = mean_diff / pooled_sd

# ---------- Test 2: One-way ANOVA ----------
education_groups = [
    group["math score"].dropna().to_numpy()
    for _, group in df.groupby("parental level of education")
]
f_stat, f_p = stats.f_oneway(*education_groups)

# ANOVA effect size: eta squared
valid_education = df.dropna(
    subset=["parental level of education", "math score"]
)
grand_mean = valid_education["math score"].mean()
ss_total = ((valid_education["math score"] - grand_mean) ** 2).sum()
ss_between = sum(
    len(g) * (g.mean() - grand_mean) ** 2
    for _, g in valid_education.groupby("parental level of education")[
        "math score"
    ]
)
eta_squared = ss_between / ss_total if ss_total else np.nan

# Tukey HSD: which groups differ?
tukey = pairwise_tukeyhsd(
    endog=valid_education["math score"],
    groups=valid_education["parental level of education"],
    alpha=0.05
)
tukey_df = pd.DataFrame(
    data=tukey._results_table.data[1:],
    columns=tukey._results_table.data[0]
)
tukey_df.to_csv(OUT / "anova_tukey_posthoc.csv", index=False)

# ---------- Test 3: Pearson correlation ----------
paired = df[["reading score", "writing score"]].dropna()
r, corr_p = stats.pearsonr(
    paired["reading score"], paired["writing score"]
)
n_corr = len(paired)

# Fisher z confidence interval for Pearson r
if n_corr > 3 and abs(r) < 1:
    z = np.arctanh(r)
    z_se = 1 / np.sqrt(n_corr - 3)
    corr_ci = (
        np.tanh(z - 1.96 * z_se),
        np.tanh(z + 1.96 * z_se)
    )
else:
    corr_ci = (np.nan, np.nan)

# ---------- Save numeric results ----------
results = pd.DataFrame([
    {
        "Test": "Welch independent t-test",
        "Statistic": t_stat,
        "P-value": t_p,
        "Effect size": cohens_d,
        "Effect measure": "Cohen's d",
        "95% CI lower": t_ci[0],
        "95% CI upper": t_ci[1],
        "Conclusion": (
            "Significant difference in group means"
            if t_p < 0.05 else "Insufficient evidence of a mean difference"
        )
    },
    {
        "Test": "One-way ANOVA",
        "Statistic": f_stat,
        "P-value": f_p,
        "Effect size": eta_squared,
        "Effect measure": "Eta squared",
        "95% CI lower": np.nan,
        "95% CI upper": np.nan,
        "Conclusion": (
            "At least one group mean differs"
            if f_p < 0.05 else "Insufficient evidence of group mean differences"
        )
    },
    {
        "Test": "Pearson correlation",
        "Statistic": r,
        "P-value": corr_p,
        "Effect size": r,
        "Effect measure": "Pearson r",
        "95% CI lower": corr_ci[0],
        "95% CI upper": corr_ci[1],
        "Conclusion": (
            "Significant linear association"
            if corr_p < 0.05 else "Insufficient evidence of linear association"
        )
    }
])
results.to_csv(BASE / "statistical_results.csv", index=False)

# ---------- Visualizations ----------
sns.set_theme(style="whitegrid")

plt.figure(figsize=(8, 5))
sns.barplot(
    data=df, x="test preparation course", y="math score",
    errorbar=("ci", 95)
)
plt.title("Mean Mathematics Score by Test Preparation")
plt.xlabel("Test preparation course")
plt.ylabel("Mathematics score")
plt.tight_layout()
plt.savefig(OUT / "1_test_prep_math_scores.png", dpi=200)
plt.close()

plt.figure(figsize=(10, 6))
sns.boxplot(
    data=valid_education,
    x="parental level of education", y="math score"
)
plt.xticks(rotation=25, ha="right")
plt.title("Mathematics Scores by Parental Education")
plt.tight_layout()
plt.savefig(OUT / "2_education_math_boxplot.png", dpi=200)
plt.close()

plt.figure(figsize=(7, 6))
sns.regplot(
    data=paired, x="reading score", y="writing score",
    scatter_kws={"alpha": 0.5}, line_kws={"color": "red"}
)
plt.title(f"Reading vs Writing Scores (r = {r:.3f})")
plt.tight_layout()
plt.savefig(OUT / "3_reading_writing_correlation.png", dpi=200)
plt.close()

# ---------- Word report ----------
doc = Document()
section = doc.sections[0]
section.top_margin = Inches(0.7)
section.bottom_margin = Inches(0.7)
section.left_margin = Inches(0.8)
section.right_margin = Inches(0.8)

for style_name in ["Normal", "Heading 1", "Heading 2"]:
    doc.styles[style_name].font.name = "Arial"
doc.styles["Normal"].font.size = Pt(10)

title = doc.add_heading(
    "Statistical Analysis and Hypothesis Testing", 0
)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p = doc.add_paragraph("Week 4 Internship Project Report")
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
doc.add_paragraph(
    "Dataset: Students Performance | Tools: Python, Pandas, SciPy, "
    "Statsmodels, Matplotlib, Seaborn"
)
doc.add_page_break()

doc.add_heading("1. Executive Summary", level=1)
doc.add_paragraph(
    f"This project analyzes {n_rows} records and {n_cols} columns from the "
    "Students Performance dataset. Three inferential methods were applied: "
    "Welch's independent t-test, one-way ANOVA, and Pearson correlation. "
    "A 5% significance level was used. The analysis examines mathematics "
    "score differences by test-preparation status and parental education, "
    "and the relationship between reading and writing scores."
)
doc.add_paragraph(
    f"The dataset contains {missing_total} missing values across the fields "
    "required for these analyses. Statistical significance indicates that "
    "the observed result is unlikely under the corresponding null hypothesis; "
    "it does not establish causation."
)

doc.add_heading("2. Objectives", level=1)
for item in [
    "Formulate null and alternative hypotheses for each statistical test.",
    "Compare mathematics scores by test-preparation status.",
    "Test for differences among parental education groups.",
    "Measure the linear association between reading and writing scores.",
    "Report p-values, confidence intervals, effect sizes and limitations."
]:
    doc.add_paragraph(item, style="List Bullet")

doc.add_heading("3. Dataset and Preparation", level=1)
doc.add_paragraph(
    "The dataset includes student background variables, test-preparation "
    "status and mathematics, reading and writing scores. The score columns "
    "were converted to numeric values for analysis. Each test uses complete "
    "observations for the variables relevant to that test."
)
doc.add_paragraph(
    f"Dataset dimensions: {n_rows} rows and {n_cols} columns. "
    f"Missing values in analysis fields: {missing_total}."
)

doc.add_heading("4. Statistical Methodology", level=1)
doc.add_paragraph(
    "The significance threshold was alpha = 0.05. When p < 0.05, the null "
    "hypothesis was rejected. Otherwise, the analysis would fail to reject "
    "the null hypothesis. P-values are interpreted together with effect sizes "
    "and confidence intervals rather than as measures of practical importance."
)
doc.add_heading("4.1 Welch Independent t-test", level=2)
doc.add_paragraph(
    "This test compares the mean mathematics scores of two independent groups "
    "without assuming equal population variances. H0: the two population "
    "means are equal. H1: the population means differ. The 95% confidence "
    "interval estimates the mean difference (completed minus none). Cohen's "
    "d summarizes the standardized difference."
)
doc.add_heading("4.2 One-way ANOVA", level=2)
doc.add_paragraph(
    "One-way ANOVA tests H0: all parental education groups have equal mean "
    "mathematics scores. H1: at least one group mean differs. Eta squared "
    "estimates the proportion of observed score variation associated with "
    "between-group differences. Tukey HSD post-hoc comparisons are included "
    "to explore which pairs differ while controlling family-wise error."
)
doc.add_heading("4.3 Pearson Correlation", level=2)
doc.add_paragraph(
    "Pearson's correlation coefficient measures the direction and strength "
    "of a linear relationship. H0: the population correlation is zero. "
    "H1: the population correlation is non-zero. A Fisher-transformation "
    "95% confidence interval is reported. Correlation does not prove causation."
)

doc.add_heading("5. Results", level=1)
table = doc.add_table(rows=1, cols=5)
table.style = "Light Shading Accent 1"
headers = ["Test", "Statistic", "P-value", "Effect size", "Conclusion"]
for cell, text in zip(table.rows[0].cells, headers):
    cell.text = text

for _, row in results.iterrows():
    cells = table.add_row().cells
    cells[0].text = str(row["Test"])
    cells[1].text = f"{row['Statistic']:.4f}"
    cells[2].text = f"{row['P-value']:.4g}"
    cells[3].text = (
        f"{row['Effect size']:.4f}" if pd.notna(row["Effect size"]) else "N/A"
    )
    cells[4].text = str(row["Conclusion"])

doc.add_heading("5.1 Welch t-test: Detailed Findings", level=2)
doc.add_paragraph(
    f"The completed preparation group had a mean mathematics score of "
    f"{mean_completed:.2f} (n = {n1}), compared with {mean_none:.2f} "
    f"(n = {n2}) for the group with no preparation. The mean difference was "
    f"{mean_diff:.2f} points, with a 95% confidence interval from "
    f"{t_ci[0]:.2f} to {t_ci[1]:.2f}. The test statistic was "
    f"t = {t_stat:.4f}, p = {t_p:.4g}, and Cohen's d = {cohens_d:.3f}. "
    + (
        "The difference was statistically significant at the 5% level."
        if t_p < 0.05 else
        "The difference was not statistically significant at the 5% level."
    )
)
doc.add_picture(str(OUT / "1_test_prep_math_scores.png"), width=Inches(6))
doc.add_paragraph(
    "Figure 1. Mathematics score means by test-preparation status. Error bars "
    "represent 95% confidence intervals around the group means."
)

doc.add_heading("5.2 ANOVA: Detailed Findings", level=2)
doc.add_paragraph(
    f"The one-way ANOVA produced F = {f_stat:.4f} and p = {f_p:.4g}. "
    f"Eta squared was {eta_squared:.4f}. "
    + (
        "The null hypothesis of equal group means was rejected; at least "
        "one parental education group differs."
        if f_p < 0.05 else
        "There was insufficient evidence to reject equal group means."
    )
)
doc.add_picture(str(OUT / "2_education_math_boxplot.png"), width=Inches(6))
doc.add_paragraph(
    "Figure 2. Distribution of mathematics scores across parental education groups."
)
doc.add_heading("Tukey HSD Post-hoc Comparisons", level=3)
doc.add_paragraph(
    "The table below reports pairwise comparisons after ANOVA. A significant "
    "pairwise result indicates evidence of a difference between that pair "
    "of groups; it does not imply that every group differs from every other."
)
tukey_table = doc.add_table(rows=1, cols=len(tukey_df.columns))
tukey_table.style = "Light Shading Accent 1"
for cell, name in zip(tukey_table.rows[0].cells, tukey_df.columns):
    cell.text = str(name)
for _, row in tukey_df.iterrows():
    cells = tukey_table.add_row().cells
    for cell, value in zip(cells, row):
        cell.text = str(value)

doc.add_heading("5.3 Pearson Correlation: Detailed Findings", level=2)
doc.add_paragraph(
    f"The correlation between reading and writing scores was r = {r:.4f}, "
    f"p = {corr_p:.4g}. Its 95% confidence interval was "
    f"({corr_ci[0]:.4f}, {corr_ci[1]:.4f}). "
    + (
        "The result indicates a statistically significant linear association."
        if corr_p < 0.05 else
        "There was insufficient evidence of a linear association."
    )
)
doc.add_picture(str(OUT / "3_reading_writing_correlation.png"), width=Inches(5.8))
doc.add_paragraph(
    "Figure 3. Reading and writing scores with a fitted linear regression line."
)

doc.add_heading("6. Overall Discussion", level=1)
doc.add_paragraph(
    "The analysis found evidence of a mathematics-score difference between "
    "students who completed test preparation and those who did not. ANOVA "
    "also found evidence that mathematics means are not all equal across "
    "parental education categories. Reading and writing scores showed a "
    "strong positive linear relationship. These results are descriptive of "
    "this dataset and do not demonstrate that test preparation or parental "
    "education caused the observed scores."
)

doc.add_heading("7. Limitations", level=1)
for item in [
    "The dataset is observational, so causal conclusions are not justified.",
    "Statistical tests depend on assumptions about observations and distributions.",
    "ANOVA identifies an overall difference but needs post-hoc comparisons to locate it.",
    "The dataset may not represent all student populations.",
    "Effect sizes and confidence intervals should be considered alongside p-values."
]:
    doc.add_paragraph(item, style="List Bullet")

doc.add_heading("8. Conclusion", level=1)
doc.add_paragraph(
    "This project demonstrates how inferential statistics can test group "
    "differences and relationships in educational data. Welch's t-test, "
    "one-way ANOVA, Tukey HSD and Pearson correlation provide complementary "
    "evidence. The results, confidence intervals, effect sizes, tables and "
    "figures make the analysis more transparent and reproducible."
)

doc.add_heading("9. Tools and References", level=1)
doc.add_paragraph(
    "Python; Pandas; SciPy; Statsmodels; Matplotlib; Seaborn; python-docx."
)
doc.add_paragraph(
    "Documentation: SciPy statistical functions (scipy.org), Statsmodels "
    "documentation (www.statsmodels.org), and Pandas documentation (pandas.pydata.org)."
)

doc.save(REPORT)
print("Detailed report created:", REPORT)
print("Charts and Tukey results saved in:", OUT)
print("\nMain statistical results:")
print(results.to_string(index=False))

