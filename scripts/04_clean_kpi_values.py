import pandas as pd
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

input_file = PROCESSED_DIR / "kansas_wioa_kpi_comparison_2025.csv"
output_file = PROCESSED_DIR / "kansas_wioa_kpi_clean_2025.csv"

df = pd.read_csv(input_file)

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

# A rate is unavailable when:
# numerator is negative, denominator is zero/negative,
# or the reported rate itself is negative.
for rate, (numerator, denominator) in rate_specs.items():
    invalid = (
        (df[numerator] < 0)
        | (df[denominator] <= 0)
        | (df[rate] < 0)
    )

    df.loc[invalid, rate] = np.nan

# Clean other rate fields
for column in [
    "Trained Participants Rate",
    "Work Experience Rate",
]:
    df.loc[df[column] < 0, column] = np.nan

# Clean median earnings
df.loc[df["MEQ2"] < 0, "MEQ2"] = np.nan

df.to_csv(output_file, index=False)

print("\nCleaned KPI values")
print("=" * 100)

print(
    df[
        [
            "Program Group",
            "Local Board Name",
            "ERQ2",
            "ERQ4",
            "MEQ2",
            "CRED",
            "MSG",
        ]
    ].to_string(index=False)
)

print(f"\nRows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")
print(f"\nSaved to: {output_file}")

