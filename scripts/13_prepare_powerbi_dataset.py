import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DASHBOARD_DIR = PROJECT_ROOT / "dashboard"

input_file = PROCESSED_DIR / "kansas_wioa_benchmark_final_2025.csv"
output_file = DASHBOARD_DIR / "kansas_wioa_powerbi_2025.csv"

df = pd.read_csv(input_file)

columns = [
    "Program Group",
    "Local Board Code",
    "Local Board Name",
    "Participants",
    "Trained Participants",
    "Trained Participants Rate",
    "Work Experience Rate",
    "Registered Apprenticeship Rate",
    "ERQ2",
    "ERQ4",
    "MEQ2",
    "CRED",
    "MSG",
    "KS Benchmark ERQ2",
    "KS Benchmark ERQ4",
    "KS Benchmark MEQ2",
    "KS Benchmark CRED",
    "KS Benchmark MSG",
    "ERQ2 Final Gap",
    "ERQ4 Final Gap",
    "MEQ2 Final Gap",
    "CRED Final Gap",
    "MSG Final Gap",
    "ERQ2 Final Status",
    "ERQ4 Final Status",
    "MEQ2 Final Status",
    "CRED Final Status",
    "MSG Final Status",
    "Final KPIs Above Benchmark",
    "Final KPIs Below Benchmark",
    "Final KPIs Unavailable",
]

powerbi = df[columns].copy()

powerbi.to_csv(output_file, index=False)

print("\nPower BI dataset created")
print("=" * 70)
print(f"Rows: {powerbi.shape[0]}")
print(f"Columns: {powerbi.shape[1]}")
print(f"\nSaved to: {output_file}")

