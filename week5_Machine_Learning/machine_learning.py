
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# --------------------------------
# 1. Folder Setup
# --------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# --------------------------------
# 2. Load Dataset
# --------------------------------

dataset_path = os.path.join(BASE_DIR, "StudentsPerformance.csv")
df = pd.read_csv(dataset_path)

print("\nFirst 5 Rows:")
print(df.head())

print("\nDataset Information:")
print(df.info())

print("\nDataset Shape:")
print(df.shape)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nColumn Names:")
print(df.columns.tolist())

# --------------------------------
# 3. Features and Target
# --------------------------------

X = df.drop("math score", axis=1)
y = df["math score"]

print("\nFeatures:")
print(X.head())

print("\nTarget:")
print(y.head())

print("\nFeatures Shape:", X.shape)
print("Target Shape:", y.shape)

# --------------------------------
# 4. Train-Test Split
# --------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# --------------------------------
# 5. Encode Categorical Columns
# --------------------------------

categorical_columns = X.select_dtypes(
    include=["object", "str", "category"]
).columns

preprocessor = ColumnTransformer(
    transformers=[
        ("encoder",
         OneHotEncoder(handle_unknown="ignore"),
         categorical_columns)
    ],
    remainder="passthrough"
)

X_train_encoded = preprocessor.fit_transform(X_train)
X_test_encoded = preprocessor.transform(X_test)

print("\nEncoded Training Shape:", X_train_encoded.shape)
print("Encoded Testing Shape:", X_test_encoded.shape)

# --------------------------------
# 6. Linear Regression
# --------------------------------

lr_model = LinearRegression()

lr_model.fit(X_train_encoded, y_train)

y_pred_lr = lr_model.predict(X_test_encoded)

print("\nLinear Regression Model")
print("First 10 Actual Scores:")
print(y_test.iloc[:10].values)

print("\nFirst 10 Predicted Scores:")
print(y_pred_lr[:10])

mae = mean_absolute_error(y_test, y_pred_lr)
mse = mean_squared_error(y_test, y_pred_lr)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred_lr)

print("\nLinear Regression Evaluation")
print("MAE:", mae)
print("MSE:", mse)
print("RMSE:", rmse)
print("R2 Score:", r2)

# --------------------------------
# 7. Random Forest
# --------------------------------

rf_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

rf_model.fit(X_train_encoded, y_train)

y_pred_rf = rf_model.predict(X_test_encoded)

print("\nRandom Forest Model")
print("First 10 Actual Scores:")
print(y_test.iloc[:10].values)

print("\nFirst 10 Predicted Scores:")
print(y_pred_rf[:10])

mae_rf = mean_absolute_error(y_test, y_pred_rf)
mse_rf = mean_squared_error(y_test, y_pred_rf)
rmse_rf = np.sqrt(mse_rf)
r2_rf = r2_score(y_test, y_pred_rf)

print("\nRandom Forest Evaluation")
print("MAE:", mae_rf)
print("MSE:", mse_rf)
print("RMSE:", rmse_rf)
print("R2 Score:", r2_rf)

# --------------------------------
# 8. Model Comparison
# --------------------------------

comparison = pd.DataFrame({
    "Model": ["Linear Regression", "Random Forest"],
    "MAE": [mae, mae_rf],
    "MSE": [mse, mse_rf],
    "RMSE": [rmse, rmse_rf],
    "R2 Score": [r2, r2_rf]
})

print("\nModel Comparison:")
print(comparison)

comparison.to_csv(
    os.path.join(OUTPUT_DIR, "model_comparison.csv"),
    index=False
)

# --------------------------------
# 9. Save Predictions
# --------------------------------

predictions = pd.DataFrame({
    "Actual": y_test.values,
    "Linear Regression": y_pred_lr,
    "Random Forest": y_pred_rf
})

predictions.to_csv(
    os.path.join(OUTPUT_DIR, "model_predictions.csv"),
    index=False
)

# --------------------------------
# 10. Linear Regression Graph
# --------------------------------

plt.figure(figsize=(8, 5))

plt.scatter(y_test, y_pred_lr, alpha=0.7)
plt.plot([0, 100], [0, 100], linestyle="--")

plt.xlabel("Actual Math Scores")
plt.ylabel("Predicted Math Scores")
plt.title("Linear Regression: Actual vs Predicted")

plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "linear_regression_plot.png")
)

plt.close()

# --------------------------------
# 11. Random Forest Graph
# --------------------------------

plt.figure(figsize=(8, 5))

plt.scatter(y_test, y_pred_rf, alpha=0.7)
plt.plot([0, 100], [0, 100], linestyle="--")

plt.xlabel("Actual Math Scores")
plt.ylabel("Predicted Math Scores")
plt.title("Random Forest: Actual vs Predicted")

plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "random_forest_plot.png")
)

plt.close()

# --------------------------------
# 12. Final Result
# --------------------------------

print("\nBest Model:")

if r2 >= r2_rf:
    print("Linear Regression")
else:
    print("Random Forest")

print("\nAll files saved successfully!")
print("Output Folder:", OUTPUT_DIR)
