import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

file_path = PROCESSED_DIR / "kansas_wioa_program_performance_2025.csv"

df = pd.read_csv(file_path)

local_boards = df[df["Local Board Code"] != 20000].copy()

columns = [
    "Program Group",
    "Local Board Name",
    "ERQ2 Numerator",
    "ERQ2 Denominator",
    "ERQ2",
    "ERQ4 Numerator",
    "ERQ4 Denominator",
    "ERQ4",
    "CRED Numerator",
    "CRED Denominator",
    "CRED",
    "MSG Numerator",
    "MSG Denominator",
    "MSG",
]

print("\nKPI Numerator and Denominator Check")
print("=" * 100)

print(
    local_boards[columns]
    .sort_values(["Program Group", "Local Board Name"])
    .to_string(index=False)
)

