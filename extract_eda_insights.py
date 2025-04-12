
import pandas as pd
from ydata_profiling import ProfileReport


# Load your dataset (Train.csv)

df = pd.read_csv(r"C:/Users/yadav/Downloads/Train.csv")






# ---------- BASIC METRICS ----------
print("\n🔹 Dataset Shape:", df.shape)
print("🔹 Column Names:", df.columns.tolist())
print("🔹 Data Types:\n", df.dtypes)

# ---------- MISSING VALUES ----------
missing = df.isnull().sum()
missing_percent = (missing / len(df)) * 100
missing_df = pd.DataFrame({'MissingValues': missing, 'MissingPercent': missing_percent})
missing_df = missing_df[missing_df.MissingValues > 0]
print("\n❗ Missing Value Summary:\n", missing_df)

# ---------- SUMMARY STATS ----------
print("\n📊 Numerical Summary:\n", df.describe())

# ---------- TARGET COLUMN CHECK ----------
if 'Reached.on.Time_Y.N' in df.columns:
    print("\n🎯 Target Column Distribution (Reached.on.Time_Y.N):\n", df['Reached.on.Time_Y.N'].value_counts())

# ---------- CORRELATION ----------
correlation_matrix = df.corr(numeric_only=True)
print("\n🔗 Correlation Matrix (top correlations):")
print(correlation_matrix.unstack().sort_values(ascending=False)[1:10])  # Exclude self-correlation

# ---------- UNIQUE VALUES ----------
print("\n🧩 Unique Values per Column:")
for col in df.columns:
    unique_vals = df[col].nunique()
    if unique_vals < 20:
        print(f"{col} ({unique_vals} unique):", df[col].unique())
    else:
        print(f"{col} ({unique_vals} unique)")
