# Takeda Compensation Analytics Engine

## Project Overview
Compensation analytics engine for Takeda Pharmaceuticals (~49,000 employees globally), built by IBM Consulting. Includes gender pay gap analysis using Blinder-Oaxaca decomposition, interactive Streamlit dashboard, and a NYT-style computational journalism piece on the motherhood penalty.

## Key Skills & Patterns
See `skills/` directory for reusable skill files:
- `pay-gap-analytics.md` — Blinder-Oaxaca regression decomposition
- `streamlit-dashboard.md` — Professional Streamlit + Plotly dashboards
- `synthetic-hr-data.md` — Realistic synthetic employee data generation
- `data-science-take-home.md` — PhD-level take-home challenge creation
- `computational-journalism.md` — NYT-style scrollytelling HTML

## Architecture
- `app.py` — Streamlit dashboard (run with `streamlit run app.py`)
- `models/pay_gap_analyzer.py` — Regression model and correction engine
- `data/generate_dummy_data.py` — Synthetic data generator (5000 employees)
- `case/index.html` — Interactive motherhood penalty magazine story
- `case/generate_report.py` — PDF report generator
- `public/index.html` — Vercel deployment copy of the magazine

## Deployment
- Vercel: deploys `public/` as static site (the magazine story)
- Streamlit dashboard: run locally or deploy to Streamlit Community Cloud

## iCloud Note
This project is in an iCloud-synced directory. Files written by tools may get evicted by "Optimize Mac Storage". Use bash `cat >` or `cp` commands to create files that persist locally.
