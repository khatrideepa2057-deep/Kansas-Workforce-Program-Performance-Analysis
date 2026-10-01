import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

input_file = PROCESSED_DIR / "kansas_wioa_benchmark_final_2025.csv"

df = pd.read_csv(input_file)

programs = ["Adult", "Dislocated Worker", "Youth"]

for program in programs:
    subset = df[df["Program Group"] == program].copy()

    subset = subset[
        [
            "Local Board Name",
            "Final KPIs Above Benchmark",
            "Final KPIs Below Benchmark",
            "Final KPIs Unavailable",
        ]
    ]

    subset = subset.set_index("Local Board Name")

    plt.figure(figsize=(11, 6))

    subset.plot(
        kind="bar",
        figsize=(11, 6)
    )

    plt.xlabel("Local Workforce Board")
    plt.ylabel("Number of KPIs")
    plt.title(f"{program} Program - KPI Benchmark Summary")

    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    safe_program = program.lower().replace(" ", "_")

    chart_file = (
        OUTPUT_DIR
        / f"kpi_status_{safe_program}.png"
    )

    plt.savefig(chart_file, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Saved: {chart_file}")

print("\nKPI status charts created successfully.")

