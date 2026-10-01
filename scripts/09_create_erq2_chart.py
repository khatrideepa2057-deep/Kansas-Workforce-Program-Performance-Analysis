import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

input_file = PROCESSED_DIR / "kansas_wioa_benchmark_final_2025.csv"
output_file = OUTPUT_DIR / "erq2_employment_rate_comparison.png"

df = pd.read_csv(input_file)

programs = ["Adult", "Dislocated Worker", "Youth"]

for program in programs:
    subset = df[df["Program Group"] == program].copy()

    subset = subset.dropna(subset=["ERQ2"])

    if subset.empty:
        continue

    benchmark = subset["KS Benchmark ERQ2"].iloc[0]

    plt.figure(figsize=(10, 6))

    plt.barh(
        subset["Local Board Name"],
        subset["ERQ2"]
    )

    plt.axvline(
        benchmark,
        linestyle="--",
        label=f"Kansas Benchmark: {benchmark:.1%}"
    )

    plt.xlabel("Employment Rate, 2nd Quarter After Exit")
    plt.ylabel("Local Workforce Board")
    plt.title(f"{program} Program - ERQ2 Performance")

    plt.xlim(0, 1)

    plt.legend()
    plt.tight_layout()

    safe_program = program.lower().replace(" ", "_")

    chart_file = (
        OUTPUT_DIR
        / f"erq2_{safe_program}_comparison.png"
    )

    plt.savefig(chart_file, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Saved: {chart_file}")

print("\nERQ2 charts created successfully.")

