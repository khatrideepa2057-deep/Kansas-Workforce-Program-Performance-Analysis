import pandas as pd
import plotly.express as px
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = (
    PROJECT_ROOT
    / "dashboard"
    / "kansas_wioa_powerbi_2025.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "dashboard"
    / "kansas_wioa_interactive_dashboard.html"
)

df = pd.read_csv(DATA_FILE)

fig = px.bar(
    df,
    x="Local Board Name",
    y="ERQ2",
    color="Program Group",
    barmode="group",
    title="Kansas WIOA Employment Rate - 2nd Quarter After Exit",
    labels={
        "Local Board Name": "Local Workforce Board",
        "ERQ2": "Employment Rate",
        "Program Group": "Program"
    }
)

fig.update_layout(
    xaxis_tickangle=-30,
    yaxis_tickformat=".0%",
    template="plotly_white"
)

fig.write_html(OUTPUT_FILE)

print("\nInteractive dashboard created successfully.")
print(f"Saved to: {OUTPUT_FILE}")

