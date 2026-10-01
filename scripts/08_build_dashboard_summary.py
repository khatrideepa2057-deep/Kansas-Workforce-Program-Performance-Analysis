import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

input_file = PROCESSED_DIR / "kansas_wioa_benchmark_final_2025.csv"
output_file = PROCESSED_DIR / "kansas_wioa_dashboard_summary_2025.csv"

df = pd.read_csv(input_file)

dashboard_columns = [
    "Program Group",
    "Local Board Name",
    "Participants",
    "Trained Participants",
    "Trained Participants Rate",
    "Work Experience Rate",
    "ERQ2",
    "ERQ4",
    "MEQ2",
    "CRED",
    "MSG",
    "Final KPIs Above Benchmark",
    "Final KPIs Below Benchmark",
    "Final KPIs Unavailable",
]

dashboard = df[dashboard_columns].copy()

dashboard.to_csv(output_file, index=False)

print("\nDashboard-ready Kansas WIOA dataset")
print("=" * 80)

print(f"Rows: {dashboard.shape[0]}")
print(f"Columns: {dashboard.shape[1]}")

print("\nPreview:")
print(dashboard.head(15).to_string(index=False))

print(f"\nSaved to: {output_file}")

