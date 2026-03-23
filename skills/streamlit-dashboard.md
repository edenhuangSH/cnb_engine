---
name: streamlit-dashboard
description: Build professional Streamlit dashboards with Plotly, branding, and interactive filters
type: skill
---

## When to Use
When building interactive data dashboards with Streamlit and Plotly Express.

## Key Patterns
- `st.set_page_config(layout="wide")` for full-width layout
- Custom CSS via `st.markdown(unsafe_allow_html=True)` for corporate branding
- `st.tabs()` for multi-section layout
- `@st.cache_data` for expensive data loading
- `st.sidebar.multiselect()` for filters
- `st.metric()` for KPI cards
- `px.histogram/bar/pie` with `color_discrete_map` for consistent colors
- `st.download_button()` for CSV export

## Checklist
- [ ] Set page config first (before any other st calls)
- [ ] Cache data loading functions
- [ ] Use consistent color maps across all charts
- [ ] Add help text to metrics
- [ ] Include download buttons for data export
