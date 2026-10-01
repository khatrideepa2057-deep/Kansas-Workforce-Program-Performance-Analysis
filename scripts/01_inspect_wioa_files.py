import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"

files = [
    "2025-06-30_WIOA_Adult_Local_Area_Performance_Results.xlsx",
    "2025-06-30_WIOA_DW_Local_Board_Performance_Results.xlsx",
    "2025-06-30_WIOA_Youth_Local_Board_Performance_Results.xlsx",
]

for filename in files:
    file_path = RAW_DIR / filename

    print("\n" + "=" * 80)
    print(f"FILE: {filename}")
    print("=" * 80)

    excel_file = pd.ExcelFile(file_path)

    print("Sheet names:")
    print(excel_file.sheet_names)

    for sheet_name in excel_file.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet_name)

        print(f"\nSheet: {sheet_name}")
        print(f"Rows: {df.shape[0]}")
        print(f"Columns: {df.shape[1]}")

        print("\nColumn names:")
        print(df.columns.tolist())

        print("\nFirst 5 rows:")
        print(df.head())

        