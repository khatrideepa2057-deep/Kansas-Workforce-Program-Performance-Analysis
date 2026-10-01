import pandas as pd
import plotly.express as px
import plotly.io as pio
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
    / "kansas_wioa_full_dashboard.html"
)

df = pd.read_csv(DATA_FILE)

# ---------------------------------------------------
# DASHBOARD SUMMARY VALUES
# ---------------------------------------------------

number_of_boards = df["Local Board Name"].nunique()
number_of_programs = df["Program Group"].nunique()
number_of_records = len(df)

total_above = int(df["Final KPIs Above Benchmark"].sum())
total_below = int(df["Final KPIs Below Benchmark"].sum())
total_unavailable = int(df["Final KPIs Unavailable"].sum())

# ---------------------------------------------------
# ERQ2 CHART
# ---------------------------------------------------

erq2_fig = px.bar(
    df.dropna(subset=["ERQ2"]),
    x="Local Board Name",
    y="ERQ2",
    color="Program Group",
    barmode="group",
    title="Employment Rate - 2nd Quarter After Exit (ERQ2)",
    labels={
        "Local Board Name": "Local Workforce Board",
        "ERQ2": "Employment Rate",
        "Program Group": "Program"
    }
)

erq2_fig.update_layout(
    template="plotly_white",
    xaxis_tickangle=-30,
    yaxis_tickformat=".0%"
)

# ---------------------------------------------------
# ERQ4 CHART
# ---------------------------------------------------

erq4_fig = px.bar(
    df.dropna(subset=["ERQ4"]),
    x="Local Board Name",
    y="ERQ4",
    color="Program Group",
    barmode="group",
    title="Employment Rate - 4th Quarter After Exit (ERQ4)",
    labels={
        "Local Board Name": "Local Workforce Board",
        "ERQ4": "Employment Rate",
        "Program Group": "Program"
    }
)

erq4_fig.update_layout(
    template="plotly_white",
    xaxis_tickangle=-30,
    yaxis_tickformat=".0%"
)

# ---------------------------------------------------
# MEDIAN EARNINGS CHART
# ---------------------------------------------------

earnings_fig = px.bar(
    df.dropna(subset=["MEQ2"]),
    x="Local Board Name",
    y="MEQ2",
    color="Program Group",
    barmode="group",
    title="Median Earnings - 2nd Quarter After Exit (MEQ2)",
    labels={
        "Local Board Name": "Local Workforce Board",
        "MEQ2": "Median Earnings ($)",
        "Program Group": "Program"
    }
)

earnings_fig.update_layout(
    template="plotly_white",
    xaxis_tickangle=-30,
    yaxis_tickprefix="$",
    yaxis_tickformat=","
)

# ---------------------------------------------------
# KPI BENCHMARK SUMMARY
# ---------------------------------------------------

status_df = df[
    [
        "Local Board Name",
        "Program Group",
        "Final KPIs Above Benchmark",
        "Final KPIs Below Benchmark",
        "Final KPIs Unavailable"
    ]
].copy()

status_long = status_df.melt(
    id_vars=["Local Board Name", "Program Group"],
    value_vars=[
        "Final KPIs Above Benchmark",
        "Final KPIs Below Benchmark",
        "Final KPIs Unavailable"
    ],
    var_name="KPI Status",
    value_name="Number of KPIs"
)

status_long["KPI Status"] = (
    status_long["KPI Status"]
    .str.replace("Final KPIs ", "", regex=False)
)

status_fig = px.bar(
    status_long,
    x="Local Board Name",
    y="Number of KPIs",
    color="KPI Status",
    facet_col="Program Group",
    barmode="stack",
    title="KPI Performance Compared with Kansas Benchmarks",
    labels={
        "Local Board Name": "Local Workforce Board"
    }
)

status_fig.update_layout(
    template="plotly_white",
    xaxis_tickangle=-30
)

# ---------------------------------------------------
# CONVERT PLOTS TO HTML
# ---------------------------------------------------

erq2_html = pio.to_html(
    erq2_fig,
    full_html=False,
    include_plotlyjs="cdn"
)

erq4_html = pio.to_html(
    erq4_fig,
    full_html=False,
    include_plotlyjs=False
)

earnings_html = pio.to_html(
    earnings_fig,
    full_html=False,
    include_plotlyjs=False
)

status_html = pio.to_html(
    status_fig,
    full_html=False,
    include_plotlyjs=False
)

# ---------------------------------------------------
# FULL DASHBOARD HTML
# ---------------------------------------------------

html = f"""
<!DOCTYPE html>

<html>

<head>

<title>Kansas Workforce Program Performance Dashboard</title>

<style>

body {{
    font-family: Arial, sans-serif;
    background-color: #f4f6f8;
    margin: 0;
    padding: 30px;
}}

h1 {{
    text-align: center;
    margin-bottom: 5px;
}}

.subtitle {{
    text-align: center;
    color: #555;
    margin-bottom: 30px;
}}

.cards {{
    display: flex;
    gap: 15px;
    justify-content: center;
    flex-wrap: wrap;
    margin-bottom: 30px;
}}

.card {{
    background: white;
    padding: 20px;
    width: 180px;
    text-align: center;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.10);
}}

.card h2 {{
    margin: 0;
    font-size: 30px;
}}

.card p {{
    margin-top: 8px;
    color: #555;
}}

.chart {{
    background: white;
    margin-bottom: 25px;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}}

.note {{
    background: white;
    padding: 20px;
    border-radius: 10px;
    margin-top: 25px;
}}

</style>

</head>

<body>

<h1>Kansas Workforce Program Performance Analysis</h1>

<div class="subtitle">
WIOA Local Workforce Board Performance | PY2024
</div>

<div class="cards">

<div class="card">
<h2>{number_of_boards}</h2>
<p>Local Workforce Boards</p>
</div>

<div class="card">
<h2>{number_of_programs}</h2>
<p>WIOA Programs</p>
</div>

<div class="card">
<h2>{number_of_records}</h2>
<p>Board-Program Records</p>
</div>

<div class="card">
<h2>{total_above}</h2>
<p>KPIs Above Benchmark</p>
</div>

<div class="card">
<h2>{total_below}</h2>
<p>KPIs Below Benchmark</p>
</div>

<div class="card">
<h2>{total_unavailable}</h2>
<p>Unavailable KPI Results</p>
</div>

</div>

<div class="chart">
{erq2_html}
</div>

<div class="chart">
{erq4_html}
</div>

<div class="chart">
{earnings_html}
</div>

<div class="chart">
{status_html}
</div>

<div class="note">

<h3>Dashboard Notes</h3>

<p>
ERQ2 represents employment in the second quarter after program exit.
ERQ4 represents employment in the fourth quarter after exit.
MEQ2 represents median earnings during the second quarter after exit.
</p>

<p>
Performance results are compared with Kansas statewide program benchmarks.
Suppressed or invalid values are treated as unavailable rather than zero.
Rates with invalid numerator or denominator values were excluded from
benchmark comparisons.
</p>

<p>
Small program cohorts should be interpreted carefully because rates based
on small denominators may vary substantially.
</p>

</div>

</body>

</html>
"""

OUTPUT_FILE.write_text(html, encoding="utf-8")

print("\nFull interactive dashboard created successfully.")
print(f"Saved to: {OUTPUT_FILE}")

