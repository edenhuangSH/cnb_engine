# Compensation & Benefits Analytics Engine

A comprehensive compensation analytics platform featuring gender pay gap analysis, interactive data journalism, and PhD-level data science challenges.

## Current Analysis: Amazon × Mercer

**Company**: Amazon (~1,500,000 employees globally)
**Consulting Partner**: Mercer

### Components

| Component | Path | Description |
|-----------|------|-------------|
| **Pay Equity Dashboard** | `app.py` | Streamlit dashboard with Blinder-Oaxaca decomposition, correction simulator |
| **Digital Magazine** | `case/index.html` | NYT-style interactive story on the motherhood penalty |
| **PDF Report** | `case/report.pdf` | Professional report with charts and LaTeX formulas |
| **Take-Home Challenge** | `take_home_challenge/` | PhD-level data science screening exam |

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py

# Generate PDF report
python3 case/generate_report.py

# View the magazine
open case/index.html
```

### Methodology

The analysis uses **Blinder-Oaxaca regression decomposition** to separate the gender pay gap into:
- **Explained** factors (job level, experience, education, department)
- **Unexplained** gap (potential systemic bias, including motherhood penalty)

Key formula:
```
ln(TC_i) = β₀ + β₁·Level + β₂·Experience + Σγ·Country + Σδ·Dept + Σφ·Education + α·IsFemale + ε
```

The coefficient α represents the unexplained gender pay gap.

### Deployment

The interactive magazine deploys to Vercel as a static site (`public/index.html`).

---

## Archive: Takeda × IBM Consulting

The original analysis for Takeda Pharmaceuticals (~49,000 employees) is preserved in `archive/takeda/`. See [archive/takeda/README.md](archive/takeda/README.md) for details.

---

*Built with Python, Streamlit, Plotly, Chart.js, Leaflet.js, and KaTeX.*
