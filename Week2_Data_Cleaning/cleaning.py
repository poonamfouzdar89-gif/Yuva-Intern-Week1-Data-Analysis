
import pandas as pd
import numpy as np

# Load the Week 1 dataset
df = pd.read_csv("StudentsPerformance.csv")

print("Original Dataset Shape:")
print(df.shape)

print("\nFirst 5 Rows:")
print(df.head())

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nStatistical Summary:")
print(df.describe())


# Check unique values in categorical columns
categorical_columns = [
    "gender",
    "race/ethnicity",
    "parental level of education",
    "lunch",
    "test preparation course"
]

print("\n--- UNIQUE CATEGORICAL VALUES ---")

for column in categorical_columns:
    print(f"\n{column}:")
    print(df[column].unique())

# Check numerical score ranges
score_columns = ["math score", "reading score", "writing score"]

print("\n--- SCORE RANGE CHECK ---")

for column in score_columns:
    print(f"\n{column}")
    print("Minimum:", df[column].min())
    print("Maximum:", df[column].max())
    print("Values below 0:", (df[column] < 0).sum())
    print("Values above 100:", (df[column] > 100).sum())

# Check extra spaces in text columns
print("\n--- EXTRA SPACE CHECK ---")

for column in categorical_columns:
    extra_spaces = df[column].astype(str).ne(
        df[column].astype(str).str.strip()
    ).sum()
    print(f"{column}: {extra_spaces}")



# ==============================
# STEP 4: DATA TRANSFORMATION
# ==============================

# Create a copy to preserve the original dataset
cleaned_df = df.copy()

# Remove extra spaces from categorical text
for column in categorical_columns:
    cleaned_df[column] = (
        cleaned_df[column]
        .str.strip()
    )

# Standardize text casing
for column in categorical_columns:
    cleaned_df[column] = cleaned_df[column].str.lower()

print("\n--- DATA TRANSFORMATION ---")
print(cleaned_df[categorical_columns].head())

# ==============================
# FEATURE ENGINEERING
# ==============================

# Calculate average score across three subjects
cleaned_df["average_score"] = cleaned_df[
    score_columns
].mean(axis=1).round(2)

# Calculate total score across three subjects
cleaned_df["total_score"] = cleaned_df[
    score_columns
].sum(axis=1)

print("\n--- NEW FEATURES ---")
print(
    cleaned_df[
        score_columns + ["total_score", "average_score"]
    ].head()
)

print("\nOriginal Dataset Shape:", df.shape)
print("Processed Dataset Shape:", cleaned_df.shape)



# ==============================
# STEP 5: ENCODING
# ==============================

encoded_df = cleaned_df.copy()

# Binary encoding for gender
encoded_df["gender_encoded"] = encoded_df["gender"].map({
    "female": 0,
    "male": 1
})

# Binary encoding for test preparation
encoded_df["test_prep_encoded"] = encoded_df[
    "test preparation course"
].map({
    "none": 0,
    "completed": 1
})

print("\n--- ENCODING RESULTS ---")
print(encoded_df[
    ["gender", "gender_encoded",
     "test preparation course", "test_prep_encoded"]
].head())

# ==============================
# STEP 5B: MIN-MAX SCALING
# ==============================

scaled_df = encoded_df.copy()

for column in score_columns:
    scaled_df[column + "_scaled"] = (
        (scaled_df[column] - scaled_df[column].min())
        / (scaled_df[column].max() - scaled_df[column].min())
    ).round(3)

print("\n--- SCALING RESULTS ---")
print(scaled_df[
    score_columns +
    [column + "_scaled" for column in score_columns]
].head())



# ==============================
# STEP 6: SAVE PROCESSED DATA
# ==============================

output_file = "StudentsPerformance_Cleaned.csv"

scaled_df.to_csv(output_file, index=False)

print("\n--- FINAL DATASET ---")
print("Original shape:", df.shape)
print("Processed shape:", scaled_df.shape)
print("Missing values after processing:", scaled_df.isnull().sum().sum())
print("Duplicate rows after processing:", scaled_df.duplicated().sum())
print(f"Processed dataset saved as: {output_file}")


# STEP 7: VALIDATION CHECKS

print("\n--- VALIDATION CHECKS ---")

print("\nNew columns:")
print([
    "average_score",
    "total_score",
    "gender_encoded",
    "test_prep_encoded",
    "math score_scaled",
    "reading score_scaled",
    "writing score_scaled"
])

print("\nEncoded values check:")
print("Gender:", sorted(scaled_df["gender_encoded"].dropna().unique()))
print("Test preparation:", sorted(scaled_df["test_prep_encoded"].dropna().unique()))

print("\nScaled scores range (should be 0 to 1):")
for column in score_columns:
    scaled_column = column + "_scaled"
    print(
        scaled_column,
        round(scaled_df[scaled_column].min(), 3),
        "to",
        round(scaled_df[scaled_column].max(), 3)
    )

print("\nValidation completed successfully!")


# STEP 8: RELOAD AND VERIFY SAVED FILE

verified_df = pd.read_csv("StudentsPerformance_Cleaned.csv")

print("\n--- SAVED FILE VERIFICATION ---")
print("Shape:", verified_df.shape)
print("Columns:", verified_df.columns.tolist())
print("Missing values:", verified_df.isnull().sum().sum())
print("Duplicate rows:", verified_df.duplicated().sum())

print("\nFirst 5 rows of saved file:")
print(verified_df.head())

print("\nSaved file verification complete!")


# STEP 9: BEFORE AND AFTER COMPARISON

print("\n--- BEFORE VS AFTER COMPARISON ---")

print("Original rows:", len(df))
print("Processed rows:", len(verified_df))

print("\nOriginal column count:", len(df.columns))
print("Processed column count:", len(verified_df.columns))

print("\nNew columns added:")
new_columns = [col for col in verified_df.columns if col not in df.columns]
for col in new_columns:
    print("-", col)

print("\nOriginal score averages:")
print(df[score_columns].mean().round(2))

print("\nNew score summary features:")
print(verified_df[["total_score", "average_score"]].describe().round(2))

print("\nOriginal and processed data comparison completed!")


# STEP 10: SAVE PREPROCESSING SUMMARY

summary = {
    "Metric": [
        "Original rows",
        "Processed rows",
        "Original columns",
        "Processed columns",
        "Missing values after processing",
        "Duplicate rows after processing",
        "New columns added"
    ],
    "Result": [
        len(df),
        len(verified_df),
        len(df.columns),
        len(verified_df.columns),
        int(verified_df.isnull().sum().sum()),
        int(verified_df.duplicated().sum()),
        len(new_columns)
    ]
}

summary_df = pd.DataFrame(summary)
summary_df.to_csv("Week2_Preprocessing_Summary.csv", index=False)

print("\nPreprocessing summary saved successfully!")
print(summary_df)
