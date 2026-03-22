# Takeda Compensation & Benefits Analytics Engine

> **Client**: Takeda Pharmaceuticals — Global Benefits Team
> **Delivered by**: IBM Consulting
> **Purpose**: Identify and remediate gender pay gaps across the global workforce

---

## Overview

This engine provides end-to-end compensation analytics: synthetic data generation, regression-based pay gap decomposition, and an interactive Streamlit dashboard with correction simulation.

### Key Capabilities

- **Pay Gap Detection** — Separates raw pay gaps into explained (job level, experience, education) and unexplained (potential bias) components
- **Multi-Dimensional Analysis** — Drill down by country, department, and job level
- **Correction Simulator** — Budget-adjustable correction recommendations with per-employee raise calculations
- **Export** — Downloadable correction reports (CSV)

---

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Generate synthetic data
python -m data.generate_dummy_data

# Launch dashboard
streamlit run app.py
```

The dashboard opens at `http://localhost:8501`.

---

## Architecture

```
takeda_cmb_engine/
├── app.py                          # Streamlit dashboard (4 tabs)
├── data/
│   └── generate_dummy_data.py      # Synthetic employee DB (5,000 records)
├── models/
│   └── pay_gap_analyzer.py         # Regression model + correction engine
├── docs/
│   └── methodology.md              # Full modeling methodology with formulas
├── .streamlit/
│   └── config.toml                 # Takeda-themed UI config
└── requirements.txt
```

---

## Dashboard Tabs

| Tab | Description |
|-----|-------------|
| **📊 Overview** | KPIs (raw gap, unexplained gap, R²), compensation distributions, gender representation by level |
| **🌍 Country Deep-Dive** | Per-country pay gap bars, department × gender breakdown, employee demographics |
| **🔧 Correction Simulator** | Budget slider (0–100%), total cost, employees affected, priority corrections table, CSV export |
| **📋 Data Explorer** | Full dataset view with filtering and download |

---

## Modeling Methodology

For the complete statistical methodology including formulas, regression specification, and correction algorithm, see:

**📄 [Methodology Document](docs/methodology.md)**

### Summary

1. **Data Generation** — 5,000 synthetic employees across 10 countries with embedded gender pay bias (5–14% by country)
2. **Gap Decomposition** — Log-linear regression controlling for job level, experience, education, country, and department. The gender coefficient isolates the unexplained gap (~8.9%)
3. **Correction Engine** — Predicts fair salary for each underpaid female employee and generates budget-adjustable raise recommendations

---

## Key Results (Synthetic Data)

| Metric | Value |
|--------|-------|
| Raw Pay Gap | 21.1% |
| Unexplained Gap (after controls) | 8.9% |
| Model R² | 0.987 |
| Full Correction Cost | ~$22.9M |
| Employees Needing Adjustment | ~2,069 |

---

## Tech Stack

- **Python 3.10+**
- **pandas / NumPy** — Data manipulation
- **scikit-learn** — Linear regression
- **Streamlit** — Interactive dashboard
- **Plotly** — Visualizations

---

## License

Internal use only — Takeda Pharmaceuticals × IBM Consulting
