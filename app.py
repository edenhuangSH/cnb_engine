"""
Takeda Compensation Analytics Dashboard
Streamlit app for gender pay gap analysis and correction planning.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data.generate_dummy_data import generate_employees
from models.pay_gap_analyzer import PayGapAnalyzer

st.set_page_config(
    page_title="Takeda Compensation Analytics",
    page_icon="💊",
    layout="wide",
)

# --- Takeda Branding ---
st.markdown("""
<style>
    .takeda-header {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 8px;
    }
    .takeda-logo {
        width: 48px;
        height: 48px;
    }
    .takeda-title {
        font-size: 2rem;
        font-weight: 700;
        color: #E60012;
        margin: 0;
    }
    .ibm-badge {
        display: inline-block;
        background: #0F62FE;
        color: white;
        padding: 2px 10px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-left: 4px;
    }
    div[data-testid="stMetric"] {
        border: 1px solid #E8E8E8;
        border-radius: 8px;
        padding: 12px;
        background: #FAFAFA;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
    }
</style>
<div class="takeda-header">
    <svg class="takeda-logo" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <circle cx="50" cy="50" r="48" fill="#E60012"/>
        <text x="50" y="58" text-anchor="middle" fill="white" font-size="24" font-weight="bold" font-family="Arial">T</text>
    </svg>
    <div>
        <p class="takeda-title">Compensation & Benefits Analytics</p>
    </div>
</div>
""", unsafe_allow_html=True)
st.caption("Gender Pay Gap Analysis | Delivered by <span class='ibm-badge'>IBM Consulting</span>",
           unsafe_allow_html=True)


@st.cache_data
def load_data():
    return generate_employees()


@st.cache_data
def run_analysis(df_json):
    df = pd.read_json(df_json)
    analyzer = PayGapAnalyzer(df)
    result = analyzer.fit_regression()
    return analyzer, result


df = load_data()
analyzer = PayGapAnalyzer(df)
result = analyzer.fit_regression()

# --- Sidebar ---
st.sidebar.header("Filters")
selected_countries = st.sidebar.multiselect(
    "Countries", df["country"].unique().tolist(), default=df["country"].unique().tolist()
)
selected_departments = st.sidebar.multiselect(
    "Departments", df["department"].unique().tolist(), default=df["department"].unique().tolist()
)

filtered_df = df[
    (df["country"].isin(selected_countries)) & (df["department"].isin(selected_departments))
]

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview", "🌍 Country Deep-Dive", "🔧 Correction Simulator", "📋 Data Explorer"
])

# ===================== TAB 1: OVERVIEW =====================
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Employees", f"{len(filtered_df):,}")
    with col2:
        st.metric("Raw Pay Gap", f"{result.overall_gap_pct:.1f}%",
                   help="Unadjusted difference in average pay between men and women")
    with col3:
        st.metric("Unexplained Gap", f"{result.unexplained_gap_pct:.1f}%",
                   delta=f"-{result.unexplained_gap_pct:.1f}%", delta_color="inverse",
                   help="Gap remaining after controlling for job level, experience, education, etc.")
    with col4:
        st.metric("Model R²", f"{result.regression_r2:.3f}",
                   help="How well legitimate factors explain pay variation")

    st.divider()

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Compensation Distribution by Gender")
        fig = px.histogram(
            filtered_df, x="total_compensation", color="gender",
            barmode="overlay", opacity=0.7, nbins=50,
            color_discrete_map={"M": "#4A90D9", "F": "#E85D75"},
            labels={"total_compensation": "Total Compensation (USD eq.)", "gender": "Gender"},
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("Average Compensation by Job Level & Gender")
        level_gender = filtered_df.groupby(["job_level", "gender"])["total_compensation"].mean().reset_index()
        fig = px.bar(
            level_gender, x="job_level", y="total_compensation", color="gender",
            barmode="group",
            color_discrete_map={"M": "#4A90D9", "F": "#E85D75"},
            labels={"job_level": "Job Level", "total_compensation": "Avg Total Comp", "gender": "Gender"},
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Gender representation by level
    st.subheader("Gender Representation by Job Level")
    level_counts = filtered_df.groupby(["job_level", "gender"]).size().reset_index(name="count")
    level_totals = level_counts.groupby("job_level")["count"].transform("sum")
    level_counts["pct"] = level_counts["count"] / level_totals * 100
    fig = px.bar(
        level_counts, x="job_level", y="pct", color="gender",
        color_discrete_map={"M": "#4A90D9", "F": "#E85D75"},
        labels={"job_level": "Job Level", "pct": "% of Employees", "gender": "Gender"},
    )
    fig.update_layout(height=350, yaxis_range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)

# ===================== TAB 2: COUNTRY DEEP-DIVE =====================
with tab2:
    st.subheader("Pay Gap by Country")

    gap_by_country = result.gap_by_country.copy()
    gap_by_country = gap_by_country[gap_by_country["category"].isin(selected_countries)]

    fig = px.bar(
        gap_by_country.sort_values("gap_pct", ascending=True),
        x="gap_pct", y="category", orientation="h",
        color="gap_pct",
        color_continuous_scale=["#2ECC71", "#F39C12", "#E74C3C"],
        labels={"gap_pct": "Raw Pay Gap (%)", "category": "Country"},
    )
    fig.update_layout(height=400, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

    # Country detail
    selected_country = st.selectbox("Select country for detail", selected_countries)
    country_df = filtered_df[filtered_df["country"] == selected_country]

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**{selected_country} — Compensation by Department & Gender**")
        dept_gender = country_df.groupby(["department", "gender"])["total_compensation"].mean().reset_index()
        fig = px.bar(
            dept_gender, x="department", y="total_compensation", color="gender",
            barmode="group",
            color_discrete_map={"M": "#4A90D9", "F": "#E85D75"},
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.write(f"**{selected_country} — Employee Count**")
        gender_counts = country_df["gender"].value_counts().reset_index()
        gender_counts.columns = ["gender", "count"]
        fig = px.pie(gender_counts, values="count", names="gender",
                     color="gender", color_discrete_map={"M": "#4A90D9", "F": "#E85D75"})
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

# ===================== TAB 3: CORRECTION SIMULATOR =====================
with tab3:
    st.subheader("Pay Gap Correction Simulator")
    st.write("Adjust the budget slider to see how much of the pay gap can be closed.")

    budget_pct = st.slider(
        "Correction Budget (% of full correction)",
        min_value=0, max_value=100, value=100, step=5,
    )

    plan = analyzer.generate_corrections(budget_pct=budget_pct)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Cost", f"${plan.total_cost:,.0f}")
    with col2:
        st.metric("Employees Affected", f"{plan.employees_affected:,}")
    with col3:
        st.metric("Avg Raise", f"{plan.avg_raise_pct:.1f}%")

    if len(plan.corrections) > 0:
        st.divider()

        col_left, col_right = st.columns(2)
        with col_left:
            st.write("**Cost by Country**")
            cost_by_country = plan.corrections.groupby("country")["recommended_raise"].sum().reset_index()
            cost_by_country.columns = ["country", "total_cost"]
            fig = px.bar(cost_by_country.sort_values("total_cost", ascending=True),
                         x="total_cost", y="country", orientation="h",
                         labels={"total_cost": "Correction Cost (USD)", "country": "Country"})
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)

        with col_right:
            st.write("**Raise Distribution**")
            fig = px.histogram(plan.corrections, x="raise_pct", nbins=30,
                               labels={"raise_pct": "Raise %"})
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)

        st.write("**Top 20 Priority Corrections**")
        display_cols = ["employee_id", "country", "department", "job_level",
                        "current_compensation", "fair_compensation", "recommended_raise", "raise_pct"]
        st.dataframe(plan.corrections[display_cols].head(20), use_container_width=True)

        # Export
        csv = plan.corrections.to_csv(index=False)
        st.download_button(
            label="📥 Download Full Correction Report (CSV)",
            data=csv,
            file_name="takeda_pay_gap_corrections.csv",
            mime="text/csv",
        )

# ===================== TAB 4: DATA EXPLORER =====================
with tab4:
    st.subheader("Raw Data Explorer")
    st.dataframe(filtered_df, use_container_width=True, height=500)

    st.download_button(
        label="📥 Download Employee Data (CSV)",
        data=filtered_df.to_csv(index=False),
        file_name="takeda_employee_data.csv",
        mime="text/csv",
    )
