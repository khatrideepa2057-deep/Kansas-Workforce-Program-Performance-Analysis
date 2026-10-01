import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

input_file = PROCESSED_DIR / "kansas_wioa_program_performance_2025.csv"

df = pd.read_csv(input_file)

# Separate local boards from statewide averages
local_boards = df[df["Local Board Code"] != 20000].copy()
state_average = df[df["Local Board Code"] == 20000].copy()

# KPIs we will use
kpis = [
    "Participants",
    "Trained Participants Rate",
    "Work Experience Rate",
    "Registered Apprenticeship Rate",
    "ERQ2",
    "ERQ4",
    "MEQ2",
    "CRED",
    "MSG",
]

# Rename statewide benchmark columns
state_benchmark = state_average[
    ["Program Group"] + kpis
].copy()

state_benchmark = state_benchmark.rename(
    columns={kpi: f"State Average {kpi}" for kpi in kpis}
)

# Merge statewide benchmark onto each local board
comparison = local_boards.merge(
    state_benchmark,
    on="Program Group",
    how="left",
)

# Calculate board performance gaps from Kansas statewide averages
for kpi in kpis:
    comparison[f"{kpi} Gap"] = (
        comparison[kpi] - comparison[f"State Average {kpi}"]
    )

# Save analysis-ready comparison file
output_file = PROCESSED_DIR / "kansas_wioa_kpi_comparison_2025.csv"

comparison.to_csv(output_file, index=False)

print("\nKansas WIOA KPI Comparison")
print("=" * 80)

print(f"Rows: {comparison.shape[0]}")
print(f"Columns: {comparison.shape[1]}")

print("\nPrograms:")
print(comparison["Program Group"].value_counts())

print("\nLocal Boards:")
print(comparison["Local Board Name"].unique())

print("\nSample KPI results:")
print(
    comparison[
        [
            "Program Group",
            "Local Board Name",
            "Participants",
            "ERQ2",
            "ERQ4",
            "MEQ2",
            "CRED",
            "MSG",
        ]
    ].to_string(index=False)
)

print(f"\nSaved to: {output_file}")

