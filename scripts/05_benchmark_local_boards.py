import pandas as pd
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

input_file = PROCESSED_DIR / "kansas_wioa_program_performance_2025.csv"
output_file = PROCESSED_DIR / "kansas_wioa_benchmark_analysis_2025.csv"

df = pd.read_csv(input_file)

# Performance KPIs
kpis = [
    "Trained Participants Rate",
    "Work Experience Rate",
    "Registered Apprenticeship Rate",
    "ERQ2",
    "ERQ4",
    "MEQ2",
    "CRED",
    "MSG",
]

# Replace unavailable negative values with missing values
for column in kpis:
    df.loc[df[column] < 0, column] = np.nan

# Separate local boards and Kansas statewide averages
local_boards = df[df["Local Board Code"] != 20000].copy()
state_average = df[df["Local Board Code"] == 20000].copy()

# Keep statewide benchmark values
state_benchmark = state_average[
    ["Program Group"] + kpis
].copy()

state_benchmark = state_benchmark.rename(
    columns={kpi: f"KS Benchmark {kpi}" for kpi in kpis}
)

# Attach benchmark to each local board
comparison = local_boards.merge(
    state_benchmark,
    on="Program Group",
    how="left"
)

# Calculate gaps and above/below benchmark status
for kpi in kpis:
    benchmark_col = f"KS Benchmark {kpi}"
    gap_col = f"{kpi} Gap"
    status_col = f"{kpi} Status"

    comparison[gap_col] = comparison[kpi] - comparison[benchmark_col]

    comparison[status_col] = np.where(
        comparison[kpi].isna() | comparison[benchmark_col].isna(),
        "Unavailable",
        np.where(
            comparison[gap_col] > 0,
            "Above Benchmark",
            np.where(
                comparison[gap_col] < 0,
                "Below Benchmark",
                "At Benchmark"
            )
        )
    )

# Count how many KPIs each board is above or below benchmark
status_columns = [f"{kpi} Status" for kpi in kpis]

comparison["KPIs Above Benchmark"] = (
    comparison[status_columns] == "Above Benchmark"
).sum(axis=1)

comparison["KPIs Below Benchmark"] = (
    comparison[status_columns] == "Below Benchmark"
).sum(axis=1)

comparison["KPIs Unavailable"] = (
    comparison[status_columns] == "Unavailable"
).sum(axis=1)

comparison.to_csv(output_file, index=False)

print("\nKansas WIOA Local Board Benchmark Analysis")
print("=" * 90)

summary_columns = [
    "Program Group",
    "Local Board Name",
    "KPIs Above Benchmark",
    "KPIs Below Benchmark",
    "KPIs Unavailable",
]

print(
    comparison[summary_columns]
    .sort_values(
        ["Program Group", "KPIs Above Benchmark"],
        ascending=[True, False]
    )
    .to_string(index=False)
)

print("\nEmployment Rate Q2 comparison:")
print(
    comparison[
        [
            "Program Group",
            "Local Board Name",
            "ERQ2",
            "KS Benchmark ERQ2",
            "ERQ2 Gap",
            "ERQ2 Status",
        ]
    ].to_string(index=False)
)

print(f"\nSaved to: {output_file}")

