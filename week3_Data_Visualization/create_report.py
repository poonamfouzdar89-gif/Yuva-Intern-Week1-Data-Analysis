
import os
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "StudentsPerformance.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
REPORT_PATH = os.path.join(BASE_DIR, "Week3_Data_Visualization_Report.docx")

# Load dataset
df = pd.read_csv(DATA_PATH)
subjects = ["math score", "reading score", "writing score"]
averages = df[subjects].mean()
correlation = df[subjects].corr()

# Create document
doc = Document()

# Default font
style = doc.styles["Normal"]
style.font.name = "Arial"
style.font.size = Pt(10)

# Cover page
title = doc.add_heading("Week 3: Data Visualization and Reporting", 0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph("Yuva Internship – Virtual Data Analysis Apprentice")
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph("Project: Students' Academic Performance Analysis")
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_page_break()

# 1. Introduction
doc.add_heading("1. Introduction", level=1)
doc.add_paragraph(
    "This project explores students' academic performance using data "
    "visualization techniques in Python. The objective is to present "
    "important patterns, compare average subject scores, examine score "
    "distributions, and study relationships between subjects."
)

# 2. Objectives
doc.add_heading("2. Objectives", level=1)
for item in [
    "Compare average scores in mathematics, reading, and writing.",
    "Visualize the distribution of students' scores.",
    "Examine the relationship between mathematics and reading scores.",
    "Measure correlations between the three subject scores.",
    "Communicate findings using charts and descriptive statistics."
]:
    doc.add_paragraph(item, style="List Bullet")

# 3. Dataset
doc.add_heading("3. Dataset Description", level=1)
doc.add_paragraph(
    f"The StudentsPerformance.csv dataset contains {df.shape[0]} records "
    f"and {df.shape[1]} columns. It includes demographic and educational "
    "information, along with mathematics, reading, and writing scores."
)

table = doc.add_table(rows=1, cols=2)
table.style = "Light Shading Accent 1"
table.rows[0].cells[0].text = "Measure"
table.rows[0].cells[1].text = "Value"

for label, value in [
    ("Number of records", str(df.shape[0])),
    ("Number of columns", str(df.shape[1])),
    ("Average mathematics score", f"{averages['math score']:.2f}"),
    ("Average reading score", f"{averages['reading score']:.2f}"),
    ("Average writing score", f"{averages['writing score']:.2f}")
]:
    cells = table.add_row().cells
    cells[0].text = label
    cells[1].text = value

# 4. Tools and methodology
doc.add_heading("4. Tools and Methodology", level=1)
doc.add_paragraph(
    "Python was used with Pandas for data handling, Matplotlib for chart "
    "creation, and Seaborn for statistical visualizations. The dataset "
    "was loaded into a DataFrame, the subject score columns were selected, "
    "and averages and Pearson correlation coefficients were calculated."
)

# 5. Visualizations and interpretation
doc.add_heading("5. Visualizations and Findings", level=1)

charts = [
    (
        "1_average_scores.png",
        "Figure 1: Average Scores by Subject",
        f"Reading has the highest average score ({averages['reading score']:.2f}), "
        f"followed by writing ({averages['writing score']:.2f}). "
        f"Mathematics has the lowest average ({averages['math score']:.2f}). "
        "These averages describe the dataset overall and do not explain the "
        "reasons behind the differences."
    ),
    (
        "2_score_distribution.png",
        "Figure 2: Distribution of Student Scores",
        "This density plot compares the distributions of mathematics, reading, "
        "and writing scores. It helps show where scores are concentrated and "
        "how their spreads differ."
    ),
    (
        "3_math_vs_reading.png",
        "Figure 3: Mathematics vs Reading Scores",
        f"The Pearson correlation between mathematics and reading scores is "
        f"{correlation.loc['math score', 'reading score']:.2f}. The scatter "
        "plot helps visualize their positive association and the variation "
        "between individual student records."
    ),
    (
        "4_score_correlation.png",
        "Figure 4: Correlation Between Subject Scores",
        f"Reading and writing have the strongest positive correlation "
        f"({correlation.loc['reading score', 'writing score']:.2f}). "
        f"Mathematics and writing have a correlation of "
        f"{correlation.loc['math score', 'writing score']:.2f}. "
        "Correlation indicates association, not causation."
    ),
    (
        "5_student_score_trends.png",
        "Figure 5: Subject Scores Across Dataset Records",
        "The line chart displays the three subject scores across dataset "
        "record numbers. Since the records are not time-series observations, "
        "the lines should be interpreted as record-wise patterns rather "
        "than changes over time."
    )
]

for filename, heading, explanation in charts:
    doc.add_heading(heading, level=2)
    chart_path = os.path.join(OUTPUT_DIR, filename)

    if os.path.isfile(chart_path):
        doc.add_picture(chart_path, width=Inches(5.8))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    else:
        doc.add_paragraph(f"Chart file not found: {filename}")

    doc.add_paragraph(explanation)

# 6. Correlation table
doc.add_heading("6. Correlation Results", level=1)
corr_table = doc.add_table(rows=1, cols=4)
corr_table.style = "Light Shading Accent 1"

headers = ["Subject", "Math", "Reading", "Writing"]
for i, header in enumerate(headers):
    corr_table.rows[0].cells[i].text = header

for subject, label in [
    ("math score", "Math"),
    ("reading score", "Reading"),
    ("writing score", "Writing")
]:
    cells = corr_table.add_row().cells
    cells[0].text = label
    for i, other in enumerate(subjects, start=1):
        cells[i].text = f"{correlation.loc[subject, other]:.2f}"

# 7. Conclusion
doc.add_heading("7. Conclusion", level=1)
doc.add_paragraph(
    "The visual analysis shows that reading has the highest average score "
    "among the three subjects, while mathematics has the lowest. Reading "
    "and writing scores show a strong positive relationship in this dataset. "
    "The visualizations demonstrate how charts and correlation analysis can "
    "summarize academic data and support clearer interpretation. These "
    "results describe associations in the dataset and should not be treated "
    "as proof of cause-and-effect relationships."
)

# 8. Limitations
doc.add_heading("8. Limitations", level=1)
doc.add_paragraph(
    "This analysis focuses on descriptive statistics and visual patterns. "
    "It does not establish why score differences occur, and the dataset's "
    "record order does not represent time. Further analysis would be needed "
    "to investigate the effects of demographic and educational factors."
)

# Save report
doc.save(REPORT_PATH)

print("Report created successfully!")
print("Location:", REPORT_PATH)
