import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

files = {
    "Adult": "2025-06-30_WIOA_Adult_Local_Area_Performance_Results.xlsx",
    "Dislocated Worker": "2025-06-30_WIOA_DW_Local_Board_Performance_Results.xlsx",
    "Youth": "2025-06-30_WIOA_Youth_Local_Board_Performance_Results.xlsx",
}

kansas_frames = []

for program_name, filename in files.items():
    file_path = RAW_DIR / filename

    df = pd.read_excel(file_path)

    kansas_df = df[df["State"] == "KS"].copy()

    kansas_df["Program Group"] = program_name

    kansas_frames.append(kansas_df)

    print(f"\n{program_name}")
    print(f"Kansas rows: {len(kansas_df)}")
    print(kansas_df[["State", "Local Board Code", "Local Board Name"]])

combined = pd.concat(kansas_frames, ignore_index=True)

output_file = PROCESSED_DIR / "kansas_wioa_program_performance_2025.csv"

combined.to_csv(output_file, index=False)

print("\nCombined Kansas dataset")
print(f"Rows: {combined.shape[0]}")
print(f"Columns: {combined.shape[1]}")
print(f"\nSaved to: {output_file}")

