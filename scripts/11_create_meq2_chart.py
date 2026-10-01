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

    subset = subset.dropna(subset=["MEQ2"])

    if subset.empty:
        continue

    benchmark = subset["KS Benchmark MEQ2"].iloc[0]

    plt.figure(figsize=(10, 6))

    plt.barh(
        subset["Local Board Name"],
        subset["MEQ2"]
    )

    plt.axvline(
        benchmark,
        linestyle="--",
        label=f"Kansas Benchmark: ${benchmark:,.0f}"
    )

    plt.xlabel("Median Earnings, 2nd Quarter After Exit ($)")
    plt.ylabel("Local Workforce Board")
    plt.title(f"{program} Program - Median Earnings")

    plt.legend()
    plt.tight_layout()

    safe_program = program.lower().replace(" ", "_")

    chart_file = (
        OUTPUT_DIR
        / f"meq2_{safe_program}_comparison.png"
    )

    plt.savefig(chart_file, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Saved: {chart_file}")

print("\nMEQ2 charts created successfully.")

