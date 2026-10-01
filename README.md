# Kansas Workforce Program Performance Analysis

## Project Overview

This project analyzes Kansas Workforce Innovation and Opportunity Act (WIOA) program performance across local workforce boards.

The analysis focuses on three major WIOA programs:

- Adult
- Dislocated Worker
- Youth

The goal is to compare local workforce board performance with Kansas statewide benchmarks and identify differences across key workforce outcome measures.

## Data Source

Source: U.S. Department of Labor WIOA Local Area Performance Results

Reporting period: PY2024 / June 30, 2025 performance files.

The project uses separate performance files for:

- Adult
- Dislocated Worker
- Youth

## Key Performance Indicators

The analysis includes:

- Participants
- Trained Participants Rate
- Work Experience Rate
- Registered Apprenticeship Rate
- ERQ2 — Employment Rate, 2nd Quarter After Exit
- ERQ4 — Employment Rate, 4th Quarter After Exit
- MEQ2 — Median Earnings, 2nd Quarter After Exit
- CRED — Credential Attainment Rate
- MSG — Measurable Skill Gains

## Analysis Process

The project workflow included:

1. Inspecting the original WIOA Excel files
2. Filtering records for Kansas
3. Combining Adult, Dislocated Worker, and Youth programs
4. Separating local workforce boards from statewide benchmark records
5. Validating KPI numerator and denominator values
6. Treating invalid or suppressed values as unavailable rather than zero
7. Calculating gaps between local board results and Kansas statewide benchmarks
8. Classifying available KPI results as:
   - Above Benchmark
   - Below Benchmark
   - At Benchmark
   - Unavailable
9. Creating static charts with Matplotlib
10. Creating an interactive dashboard with Plotly

## Kansas Workforce Boards Analyzed

- Kansas WorkforceONE
- Heartland Works, Inc.
- Workforce Partnership
- Workforce Alliance of South Central Kansas
- Southeast KANSASWORKS

## Live Interactive Dashboard

View the live dashboard here:

[Open Kansas Workforce Program Performance Dashboard](https://khatrideepa2057-deep.github.io/Kansas-Workforce-Program-Performance-Analysis/)

The dashboard includes:

- KPI summary cards
- ERQ2 employment-rate comparisons
- ERQ4 employment-rate comparisons
- Median earnings comparisons
- KPI benchmark-status summaries
- Interactive hover details

## Important Data Quality Considerations

Suppressed or invalid KPI values were not treated as zero.

For rate-based measures, numerator and denominator values were checked before performance comparisons were calculated.

Results based on small denominators should be interpreted carefully because small cohorts can cause large changes in percentage-based performance measures.

## Project Structure

```text
Kansas Workforce Program Performance Analysis/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── scripts/
│
├── outputs/
│
├── dashboard/
│
├── reports/
│
├── index.html
│
├── requirements.txt
│
└── README.md

