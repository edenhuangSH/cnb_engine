---
name: Streamlit Dashboard
description: Use when building interactive Streamlit dashboards with Plotly charts, sidebar filters, and branded styling
type: skill
---

## When to Use
Use this skill when creating data exploration dashboards in Streamlit, especially those with multiple tabs, interactive Plotly visualizations, KPI cards, and CSV export functionality. Particularly suited for HR analytics and compensation reporting.

## Key Patterns

**Multi-Tab Layout**
```python
tab1, tab2, tab3 = st.tabs(["Overview", "Analysis", "Details"])
with tab1:
    st.header("Overview")
```

**Plotly Express Charts**
- `px.histogram` for distribution comparisons (overlay with `barmode="overlay"`)
- `px.bar` for grouped categorical comparisons
- `px.pie` for composition breakdowns
- `px.scatter` for correlation plots with trendlines
- Always set `color_discrete_map={"M": "#4A90D9", "F": "#E85D75"}` for gender viz

**Custom CSS Branding**
```python
st.markdown("""
<style>
    .stApp { font-family: 'Inter', sans-serif; }
    .metric-card { background: #f8f9fa; border-radius: 8px; padding: 1rem; }
</style>
""", unsafe_allow_html=True)
```

**Performance and Caching**
```python
@st.cache_data
def load_data(path):
    return pd.read_csv(path)
```

**Sidebar Filters**
```python
with st.sidebar:
    selected_countries = st.multiselect("Country", options=df["country"].unique(), default=df["country"].unique())
    filtered_df = df[df["country"].isin(selected_countries)]
```

**KPI Cards and Exports**
```python
col1, col2, col3 = st.columns(3)
col1.metric("Median Gap", f"{gap:.1f}%", delta=f"{delta:.1f}%")

st.download_button("Export CSV", data=df.to_csv(index=False), file_name="report.csv", mime="text/csv")
```

## Checklist
- [ ] Use `st.set_page_config(layout="wide")` at the very top
- [ ] Cache expensive computations with `@st.cache_data`
- [ ] Apply consistent color maps across all gender-based charts
- [ ] Provide CSV download buttons for key tables
- [ ] Use `st.metric` for headline KPIs with delta indicators
- [ ] Add sidebar filters that apply globally across all tabs
- [ ] Test with `streamlit run app.py` locally before deploying
