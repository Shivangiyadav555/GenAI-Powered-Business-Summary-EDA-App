import pandas as pd
from ydata_profiling import ProfileReport

# Load your dataset
df = pd.read_csv(r"C:/Users/yadav/Downloads/Train.csv")  # Adjust path if needed

# Generate the profiling report
profile = ProfileReport(df, title="Training Data EDA Summary", explorative=True)

# Export the report to HTML
profile.to_file("eda_report.html")

print("✅ EDA report generated: eda_report.html")


