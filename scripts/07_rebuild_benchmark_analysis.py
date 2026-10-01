import pandas as pd
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

clean_file = PROCESSED_DIR / "kansas_wioa_kpi_clean_2025.csv"
raw_file = PROCESSED_DIR / "kansas_wioa_program_performance_2025.csv"

output_file = PROCESSED_DIR / "kansas_wioa_benchmark_final_2025.csv"

clean_df = pd.read_csv(clean_file)
raw_df = pd.read_csv(raw_file)

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

state_average = raw_df[raw_df["Local Board Code"] == 20000].copy()

rate_specs = {
    "ERQ2": ("ERQ2 Numerator", "ERQ2 Denominator"),
    "ERQ4": ("ERQ4 Numerator", "ERQ4 Denominator"),
    "CRED": ("CRED Numerator", "CRED Denominator"),
    "MSG": ("MSG Numerator", "MSG Denominator"),
    "Registered Apprenticeship Rate": (
        "Registered Apprenticeship Numerator",
        "Registered Apprenticeship Denominator",
    ),
}

for rate, (num, den) in rate_specs.items():
    invalid = (
        (state_average[num] < 0)
        | (state_average[den] <= 0)
        | (state_average[rate] < 0)
    )
    state_average.loc[invalid, rate] = np.nan

for column in [
    "Trained Participants Rate",
    "Work Experience Rate",
]:
    state_average.loc[state_average[column] < 0, column] = np.nan

state_average.loc[state_average["MEQ2"] < 0, "MEQ2"] = np.nan

state_benchmark = state_average[
    ["Program Group"] + kpis
].copy()

state_benchmark = state_benchmark.rename(
    columns={kpi: f"KS Benchmark {kpi}" for kpi in kpis}
)

comparison = clean_df.merge(
    state_benchmark,
    on="Program Group",
    how="left"
)

for kpi in kpis:
    benchmark_col = f"KS Benchmark {kpi}"
    gap_col = f"{kpi} Final Gap"
    status_col = f"{kpi} Final Status"

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

status_columns = [f"{kpi} Final Status" for kpi in kpis]

comparison["Final KPIs Above Benchmark"] = (
    comparison[status_columns] == "Above Benchmark"
).sum(axis=1)

comparison["Final KPIs Below Benchmark"] = (
    comparison[status_columns] == "Below Benchmark"
).sum(axis=1)

comparison["Final KPIs Unavailable"] = (
    comparison[status_columns] == "Unavailable"
).sum(axis=1)

comparison.to_csv(output_file, index=False)

print("\nFINAL Kansas WIOA Benchmark Analysis")
print("=" * 100)

print(
    comparison[
        [
            "Program Group",
            "Local Board Name",
            "Final KPIs Above Benchmark",
            "Final KPIs Below Benchmark",
            "Final KPIs Unavailable",
        ]
    ]
    .sort_values(
        ["Program Group", "Final KPIs Above Benchmark"],
        ascending=[True, False]
    )
    .to_string(index=False)
)

print("\nSoutheast KANSASWORKS - Dislocated Worker check:")
print(
    comparison[
        (comparison["Program Group"] == "Dislocated Worker")
        & (comparison["Local Board Name"] == "Southeast KANSASWORKS")
    ][
        [
            "ERQ2",
            "ERQ2 Final Status",
            "ERQ4",
            "ERQ4 Final Status",
            "CRED",
            "CRED Final Status",
        ]
    ].to_string(index=False)
)

print(f"\nSaved to: {output_file}")

