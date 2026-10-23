# Student Performance Data Analysis

## About the Project

This project was developed as part of **Week 1 of the Virtual Data Analysis Apprentice Internship at Yuva Intern**.

The project focuses on exploring student performance data to identify patterns and differences in Mathematics, Reading, and Writing scores.

The analysis examines factors such as:

- Gender
- Race/Ethnicity
- Parental Level of Education
- Lunch Type
- Test Preparation Course

Python-based data analysis and visualization techniques were used to explore the dataset and generate meaningful insights.

---

## Problem Statement

This analysis aims to explore the factors associated with students' academic performance in Mathematics, Reading, and Writing.

The study examines variables such as test preparation course, parental education level, lunch type, and gender to identify patterns and differences in students' scores.

---

## Dataset

**Dataset:** Students Performance in Exams

**Source:** Kaggle

**Records:** 1,000 students

**Variables:** 8

The dataset contains:

- Gender
- Race/Ethnicity
- Parental Level of Education
- Lunch
- Test Preparation Course
- Math Score
- Reading Score
- Writing Score

> The dataset file is not included in this repository.

---

## Objectives

- Understand the structure of the dataset
- Explore categorical and numerical variables
- Compare average student scores
- Identify patterns in academic performance
- Create meaningful visualizations
- Generate insights from the data

---

## Tools & Technologies

- Python 3.13
- Pandas
- NumPy
- Matplotlib
- VS Code

---

## Analysis Performed

The following analysis was performed:

1. Dataset loading and exploration
2. Dataset shape and column analysis
3. Data type and statistical summary
4. Missing value checking
5. Duplicate record checking
6. Categorical variable exploration
7. Average score comparison by:
   - Test Preparation Course
   - Parental Education
   - Lunch Type
   - Gender
8. Data visualization using Matplotlib
9. Creation of a Student Performance EDA Dashboard

---

## Key Findings

### Test Preparation Course

Students who completed the test preparation course had higher average scores in Mathematics, Reading, and Writing compared with students who did not complete the course.

### Parental Education

Students with higher parental education levels generally showed higher average academic scores.

### Lunch Type

Students receiving standard lunch had higher average scores across all three subjects compared with students receiving free/reduced lunch.

### Gender

Male students had a higher average Mathematics score, while female students had higher average Reading and Writing scores.

### Overall Performance

Reading had the highest overall average score among the three subjects.

---

## Visualizations

The project includes a dashboard containing four comparative visualizations:

- Average Scores by Test Preparation Course
- Average Scores by Gender
- Average Scores by Parental Education
- Average Scores by Lunch Type

---

## Project Structure

```text
Yuva-Intern-Week1-Data-Analysis/
│
├── data_analysis.py
├── .gitignore
└── README.md

How to Run
1. Clone the repository
git clone https://github.com/poonamfouzdar89-gif/Yuva-Intern-Week1-Data-Analysis.git

2. Open the project folder
cd Yuva-Intern-Week1-Data-Analysis

3. Install required libraries
pip install pandas numpy matplotlib

4. Add the dataset
Place StudentsPerformance.csv in the project folder.
5. Run the Python file
python data_analysis.py

Internship
Organization: Yuva Intern
Internship: Virtual Data Analysis Apprentice Internship
Week: 1
Task: Data Exploration and Problem Definition
