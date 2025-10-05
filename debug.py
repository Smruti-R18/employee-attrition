import pandas as pd
import joblib

# --- Paths (update if needed) ---
preprocessor_path = "C:/Users/smrut/Documents/Projects/Employee Attrition Predictor/artifacts/preprocessor.pkl"
csv_path = "C:/Users/smrut/Documents/Projects/Employee Attrition Predictor/test_input.csv"

# --- Load preprocessor tuple ---
preprocessor_tuple = joblib.load(preprocessor_path)

# Unpack the tuple
column_transformer = preprocessor_tuple[0]  # ColumnTransformer
all_columns = preprocessor_tuple[1]         # All columns
categorical_columns = preprocessor_tuple[2] # Categorical columns

# --- Load CSV ---
df = pd.read_csv(csv_path)

# --- Check missing columns ---
missing_cols = [col for col in all_columns if col not in df.columns]
extra_cols = [col for col in df.columns if col not in all_columns]

print("All expected columns:", all_columns)
print("Missing columns in CSV:", missing_cols)
print("Extra columns in CSV:", extra_cols)

# --- Check column types ---
print("\nColumn types in CSV:")
print(df.dtypes)

# --- Check categorical values ---
print("\nCategorical columns and unique values:")
for col in categorical_columns:
    if col in df.columns:
        print(f"{col}: {df[col].unique()}")

# --- Optional: check for NaNs ---
print("\nMissing values in CSV:")
print(df.isna().sum())
