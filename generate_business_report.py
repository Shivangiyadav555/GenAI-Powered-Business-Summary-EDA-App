import pandas as pd
from gpt_summary import generate_summary

# Load your cleaned dataset
file_path = r"C:/Users/yadav/Downloads/Train.csv"
df = pd.read_csv(file_path)

# Build insights (just like extract_eda_insights.py)
insights = []

# Basic shape
insights.append(f"Dataset has {df.shape[0]} rows and {df.shape[1]} columns.")

# Missing values
missing = df.isnull().sum()
missing_percent = (missing / len(df)) * 100
missing_info = missing[missing > 0]
if not missing_info.empty:
    insights.append(f"Missing data found in:\n{missing_info.to_string()}")

# Summary stats
summary_stats = df.describe().T
insights.append(f"Summary Statistics:\n{summary_stats[['mean', 'std', 'min', 'max']].to_string()}")

# Target column (if exists)
if 'Reached.on.Time_Y.N' in df.columns:
    insights.append("Target column distribution (Reached.on.Time_Y.N):\n" + str(df['Reached.on.Time_Y.N'].value_counts()))

# Correlation (top 5 pairs)
corr = df.corr(numeric_only=True).unstack().sort_values(ascending=False)
corr = corr[corr != 1].drop_duplicates()
insights.append("Top 5 correlations:\n" + str(corr.head(5)))

# Combine all insights into one prompt
final_prompt = "\n\n".join(insights)

# Generate business summary from insights
summary = generate_summary(final_prompt)

# Output result
print("\n📊 Final Business Summary:\n")
print(summary)
