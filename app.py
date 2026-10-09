"""
Retail Sales Analysis — Single-file Streamlit App
Backend analysis functions + all four dashboard sections combined.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

# ═══════════════════════════════════════════════════════════════════════════════
# BACKEND — Data loading & analysis functions
# ═══════════════════════════════════════════════════════════════════════════════

DATA_PATH = Path(__file__).parent / "data" / "retail_sales_dataset.csv"


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    df["Month"]     = df["Date"].dt.to_period("M").astype(str)
    df["MonthDate"] = df["Date"].dt.to_period("M").dt.to_timestamp()
    df["Year"]      = df["Date"].dt.year
    df["Quarter"]   = "Q" + df["Date"].dt.quarter.astype(str)
    df["Age Group"] = pd.cut(
        df["Age"],
        bins=[0, 25, 35, 45, 60, 100],
        labels=["18-25", "26-35", "36-45", "46-60", "60+"],
    )
    return df


# ── KPI ───────────────────────────────────────────────────────────────────────

def kpi_summary(df):
    return {
        "total_revenue":      df["Total Amount"].sum(),
        "total_transactions": len(df),
        "unique_customers":   df["Customer ID"].nunique(),
        "avg_order_value":    df["Total Amount"].mean(),
        "avg_quantity":       df["Quantity"].mean(),
    }


# ── Time-series ───────────────────────────────────────────────────────────────

def monthly_revenue(df):
    return (
        df.groupby("MonthDate")["Total Amount"].sum().reset_index()
        .rename(columns={"MonthDate": "Month", "Total Amount": "Revenue"})
        .sort_values("Month")
    )


def monthly_transactions(df):
    return (
        df.groupby("MonthDate")["Transaction ID"].count().reset_index()
        .rename(columns={"MonthDate": "Month", "Transaction ID": "Transactions"})
        .sort_values("Month")
    )


def quarterly_revenue(df):
    return (
        df.groupby(["Year", "Quarter"])["Total Amount"].sum().reset_index()
        .rename(columns={"Total Amount": "Revenue"})
    )


# ── Product ───────────────────────────────────────────────────────────────────

def revenue_by_category(df):
    return (
        df.groupby("Product Category")["Total Amount"].sum().reset_index()
        .rename(columns={"Total Amount": "Revenue"})
        .sort_values("Revenue", ascending=False)
    )


def quantity_by_category(df):
    return (
        df.groupby("Product Category")["Quantity"].sum().reset_index()
        .sort_values("Quantity", ascending=False)
    )


def avg_price_by_category(df):
    return (
        df.groupby("Product Category")["Price per Unit"].mean().reset_index()
        .rename(columns={"Price per Unit": "Avg Price"})
    )


def category_monthly_trend(df):
    return (
        df.groupby(["MonthDate", "Product Category"])["Total Amount"].sum().reset_index()
        .rename(columns={"MonthDate": "Month", "Total Amount": "Revenue"})
        .sort_values("Month")
    )


# ── Customer ──────────────────────────────────────────────────────────────────

def revenue_by_gender(df):
    return (
        df.groupby("Gender")["Total Amount"].sum().reset_index()
        .rename(columns={"Total Amount": "Revenue"})
    )


def transactions_by_gender(df):
    return (
        df.groupby("Gender")["Transaction ID"].count().reset_index()
        .rename(columns={"Transaction ID": "Transactions"})
    )


def revenue_by_age_group(df):
    return (
        df.groupby("Age Group", observed=True)["Total Amount"].sum().reset_index()
        .rename(columns={"Total Amount": "Revenue"})
    )


def gender_category_heatmap(df):
    return (
        df.groupby(["Gender", "Product Category"])["Total Amount"]
        .sum().unstack(fill_value=0)
    )


def age_group_category(df):
    return (
        df.groupby(["Age Group", "Product Category"], observed=True)["Total Amount"]
        .sum().reset_index()
        .rename(columns={"Total Amount": "Revenue"})
    )


def top_customers(df, n=10):
    return (
        df.groupby("Customer ID")
        .agg(
            Total_Spent=("Total Amount", "sum"),
            Transactions=("Transaction ID", "count"),
            Avg_Order=("Total Amount", "mean"),
        )
        .reset_index()
        .sort_values("Total_Spent", ascending=False)
        .head(n)
    )


# ── Distribution ──────────────────────────────────────────────────────────────

def price_distribution(df):
    return df["Price per Unit"].value_counts().sort_index()


def quantity_distribution(df):
    return df["Quantity"].value_counts().sort_index()


def total_amount_stats(df):
    s = df["Total Amount"]
    return {
        "min":    s.min(),
        "max":    s.max(),
        "mean":   s.mean(),
        "median": s.median(),
        "std":    s.std(),
        "p25":    s.quantile(0.25),
        "p75":    s.quantile(0.75),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# FRONTEND — Streamlit Dashboard
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Retail Sales Analysis",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

df = load_data()

st.title("🛍️ Retail Sales Analysis Dashboard")
st.caption(
    f"Dataset: `retail_sales_dataset.csv` — "
    f"**{len(df):,}** transactions · **{df['Customer ID'].nunique():,}** unique customers"
)

tab_home, tab_overview, tab_product, tab_customer, tab_deep = st.tabs([
    "🏠 Home",
    "📊 Overview",
    "🏷️ Product Analysis",
    "👥 Customer Insights",
    "🔍 Transaction Deep-Dive",
])


# ─────────────────────────────────────────────────────────────────────────────
# TAB 0 — Home
# ─────────────────────────────────────────────────────────────────────────────
with tab_home:
    st.subheader("Welcome")
    st.markdown("""
    Use the **tabs above** to navigate between sections:

    | Tab | What you'll find |
    |---|---|
    | 📊 Overview | KPI cards, monthly revenue & transaction trends |
    | 🏷️ Product Analysis | Revenue, quantity & pricing by category |
    | 👥 Customer Insights | Gender & age demographics, top customers |
    | 🔍 Transaction Deep-Dive | Filter & explore individual transactions |
    """)
    st.divider()
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Dataset Preview")
        st.dataframe(df.head(10), use_container_width=True)
    with col2:
        st.subheader("Column Info")
        info_df = df.dtypes.reset_index()
        info_df.columns = ["Column", "Type"]
        info_df["Non-Null"] = df.notnull().sum().values
        st.dataframe(info_df, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — Overview
# ─────────────────────────────────────────────────────────────────────────────
with tab_overview:
    st.subheader("Filters")
    ov_c1, ov_c2, ov_c3 = st.columns(3)
    with ov_c1:
        ov_cat = st.selectbox(
            "Product Category",
            ["All"] + sorted(df["Product Category"].unique().tolist()),
            key="ov_cat",
        )
    with ov_c2:
        ov_gender = st.selectbox(
            "Gender",
            ["All"] + sorted(df["Gender"].unique().tolist()),
            key="ov_gender",
        )
    with ov_c3:
        ov_year = st.multiselect(
            "Year",
            sorted(df["Year"].unique().tolist()),
            default=sorted(df["Year"].unique().tolist()),
            key="ov_year",
        )

    ov = df.copy()
    if ov_cat != "All":
        ov = ov[ov["Product Category"] == ov_cat]
    if ov_gender != "All":
        ov = ov[ov["Gender"] == ov_gender]
    if ov_year:
        ov = ov[ov["Year"].isin(ov_year)]

    st.divider()

    # KPI cards
    kpis = kpi_summary(ov)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("💰 Total Revenue",    f"${kpis['total_revenue']:,.0f}")
    c2.metric("🧾 Transactions",     f"{kpis['total_transactions']:,}")
    c3.metric("👤 Unique Customers", f"{kpis['unique_customers']:,}")
    c4.metric("🛒 Avg Order Value",  f"${kpis['avg_order_value']:,.2f}")
    c5.metric("📦 Avg Quantity",     f"{kpis['avg_quantity']:.2f}")

    st.divider()

    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("Monthly Revenue Trend")
        fig = px.area(
            monthly_revenue(ov), x="Month", y="Revenue",
            color_discrete_sequence=["#3b82d4"],
            labels={"Revenue": "Revenue ($)", "Month": ""},
        )
        fig.update_layout(margin=dict(t=20, b=20), hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.subheader("Monthly Transaction Count")
        fig2 = px.bar(
            monthly_transactions(ov), x="Month", y="Transactions",
            color_discrete_sequence=["#7c5cd8"],
            labels={"Transactions": "# Transactions", "Month": ""},
        )
        fig2.update_layout(margin=dict(t=20, b=20))
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Quarterly Revenue")
    qrev = quarterly_revenue(ov)
    qrev["Period"] = qrev["Year"].astype(str) + " " + qrev["Quarter"]
    fig3 = px.bar(
        qrev, x="Period", y="Revenue", color="Quarter",
        color_discrete_sequence=px.colors.qualitative.Set2,
        labels={"Revenue": "Revenue ($)", "Period": ""},
        text_auto=".2s",
    )
    fig3.update_layout(margin=dict(t=20, b=20))
    st.plotly_chart(fig3, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — Product Analysis
# ─────────────────────────────────────────────────────────────────────────────
with tab_product:
    st.subheader("Filters")
    pr_c1, pr_c2 = st.columns(2)
    with pr_c1:
        pr_gender = st.selectbox(
            "Gender",
            ["All"] + sorted(df["Gender"].unique().tolist()),
            key="pr_gender",
        )
    with pr_c2:
        pr_year = st.multiselect(
            "Year",
            sorted(df["Year"].unique().tolist()),
            default=sorted(df["Year"].unique().tolist()),
            key="pr_year",
        )

    pr = df.copy()
    if pr_gender != "All":
        pr = pr[pr["Gender"] == pr_gender]
    if pr_year:
        pr = pr[pr["Year"].isin(pr_year)]

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Revenue by Category")
        fig = px.bar(
            revenue_by_category(pr), x="Product Category", y="Revenue",
            color="Product Category",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            text_auto=".2s", labels={"Revenue": "Revenue ($)"},
        )
        fig.update_layout(showlegend=False, margin=dict(t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Units Sold by Category")
        fig2 = px.pie(
            quantity_by_category(pr), values="Quantity", names="Product Category",
            color_discrete_sequence=px.colors.qualitative.Set2, hole=0.4,
        )
        fig2.update_traces(textposition="inside", textinfo="percent+label")
        fig2.update_layout(margin=dict(t=20, b=20))
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Average Price per Unit by Category")
        fig3 = px.bar(
            avg_price_by_category(pr), x="Product Category", y="Avg Price",
            color="Product Category",
            color_discrete_sequence=px.colors.qualitative.Bold,
            text_auto=".2f", labels={"Avg Price": "Avg Price ($)"},
        )
        fig3.update_layout(showlegend=False, margin=dict(t=20, b=20))
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.subheader("Monthly Revenue Trend by Category")
        fig4 = px.line(
            category_monthly_trend(pr), x="Month", y="Revenue",
            color="Product Category",
            color_discrete_sequence=px.colors.qualitative.Set1,
            markers=True, labels={"Revenue": "Revenue ($)", "Month": ""},
        )
        fig4.update_layout(margin=dict(t=20, b=20), hovermode="x unified")
        st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Category Summary Table")
    summary = (
        pr.groupby("Product Category")
        .agg(
            Revenue=("Total Amount", "sum"),
            Transactions=("Transaction ID", "count"),
            Units_Sold=("Quantity", "sum"),
            Avg_Order=("Total Amount", "mean"),
            Avg_Price=("Price per Unit", "mean"),
        )
        .reset_index()
        .sort_values("Revenue", ascending=False)
    )
    summary["Revenue"]   = summary["Revenue"].map("${:,.0f}".format)
    summary["Avg_Order"] = summary["Avg_Order"].map("${:,.2f}".format)
    summary["Avg_Price"] = summary["Avg_Price"].map("${:,.2f}".format)
    st.dataframe(summary, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — Customer Insights
# ─────────────────────────────────────────────────────────────────────────────
with tab_customer:
    st.subheader("Filters")
    cu_c1, cu_c2, cu_c3 = st.columns(3)
    with cu_c1:
        cu_cat = st.selectbox(
            "Product Category",
            ["All"] + sorted(df["Product Category"].unique().tolist()),
            key="cu_cat",
        )
    with cu_c2:
        cu_year = st.multiselect(
            "Year",
            sorted(df["Year"].unique().tolist()),
            default=sorted(df["Year"].unique().tolist()),
            key="cu_year",
        )
    with cu_c3:
        top_n = st.slider("Top N Customers", min_value=5, max_value=20, value=10)

    cu = df.copy()
    if cu_cat != "All":
        cu = cu[cu["Product Category"] == cu_cat]
    if cu_year:
        cu = cu[cu["Year"].isin(cu_year)]

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Revenue by Gender")
        fig = px.pie(
            revenue_by_gender(cu), values="Revenue", names="Gender",
            color_discrete_sequence=["#3b82d4", "#f472b6"], hole=0.45,
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig.update_layout(margin=dict(t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Transactions by Gender")
        fig2 = px.bar(
            transactions_by_gender(cu), x="Gender", y="Transactions",
            color="Gender",
            color_discrete_sequence=["#3b82d4", "#f472b6"],
            text_auto=True,
        )
        fig2.update_layout(showlegend=False, margin=dict(t=20, b=20))
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Revenue by Age Group")
        fig3 = px.bar(
            revenue_by_age_group(cu), x="Age Group", y="Revenue",
            color="Age Group",
            color_discrete_sequence=px.colors.qualitative.Safe,
            text_auto=".2s", labels={"Revenue": "Revenue ($)"},
        )
        fig3.update_layout(showlegend=False, margin=dict(t=20, b=20))
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.subheader("Age Distribution")
        fig4 = px.histogram(
            cu, x="Age", nbins=20,
            color_discrete_sequence=["#7c5cd8"],
            labels={"Age": "Customer Age"},
        )
        fig4.update_layout(margin=dict(t=20, b=20))
        st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Revenue Heatmap: Gender × Product Category")
    fig5 = px.imshow(
        gender_category_heatmap(cu),
        text_auto=".2s", color_continuous_scale="Blues",
        labels={"color": "Revenue ($)"}, aspect="auto",
    )
    fig5.update_layout(margin=dict(t=20, b=20))
    st.plotly_chart(fig5, use_container_width=True)

    st.subheader("Revenue by Age Group & Category")
    fig6 = px.bar(
        age_group_category(cu), x="Age Group", y="Revenue",
        color="Product Category", barmode="group",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        labels={"Revenue": "Revenue ($)"},
    )
    fig6.update_layout(margin=dict(t=20, b=20))
    st.plotly_chart(fig6, use_container_width=True)

    st.subheader(f"Top {top_n} Customers by Total Spend")
    top = top_customers(cu, n=top_n)
    fig7 = px.bar(
        top, x="Customer ID", y="Total_Spent",
        color="Total_Spent", color_continuous_scale="Teal",
        text_auto=".2s",
        labels={"Total_Spent": "Total Spend ($)", "Customer ID": "Customer"},
    )
    fig7.update_layout(margin=dict(t=20, b=20), coloraxis_showscale=False)
    st.plotly_chart(fig7, use_container_width=True)
    st.dataframe(
        top.rename(columns={"Total_Spent": "Total Spend ($)", "Avg_Order": "Avg Order ($)"}),
        use_container_width=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — Transaction Deep-Dive
# ─────────────────────────────────────────────────────────────────────────────
with tab_deep:
    st.subheader("Filters")
    d_c1, d_c2 = st.columns(2)
    with d_c1:
        d_cat = st.selectbox(
            "Product Category",
            ["All"] + sorted(df["Product Category"].unique().tolist()),
            key="d_cat",
        )
        d_gender = st.selectbox(
            "Gender",
            ["All"] + sorted(df["Gender"].unique().tolist()),
            key="d_gender",
        )
    with d_c2:
        d_age = st.slider(
            "Age Range",
            int(df["Age"].min()), int(df["Age"].max()),
            (int(df["Age"].min()), int(df["Age"].max())),
        )
        d_amount = st.slider(
            "Total Amount ($)",
            float(df["Total Amount"].min()), float(df["Total Amount"].max()),
            (float(df["Total Amount"].min()), float(df["Total Amount"].max())),
        )

    date_min = df["Date"].min().date()
    date_max = df["Date"].max().date()
    d_dates = st.date_input(
        "Date Range", value=(date_min, date_max),
        min_value=date_min, max_value=date_max,
    )

    dv = df.copy()
    if d_cat != "All":
        dv = dv[dv["Product Category"] == d_cat]
    if d_gender != "All":
        dv = dv[dv["Gender"] == d_gender]
    dv = dv[(dv["Age"] >= d_age[0]) & (dv["Age"] <= d_age[1])]
    dv = dv[(dv["Total Amount"] >= d_amount[0]) & (dv["Total Amount"] <= d_amount[1])]
    if len(d_dates) == 2:
        dv = dv[
            (dv["Date"].dt.date >= d_dates[0]) &
            (dv["Date"].dt.date <= d_dates[1])
        ]

    st.markdown(f"**{len(dv):,}** transactions match the current filters.")
    st.divider()

    # Stats row
    st.subheader("Total Amount Statistics")
    stats = total_amount_stats(dv)
    sc1, sc2, sc3, sc4, sc5, sc6, sc7 = st.columns(7)
    sc1.metric("Min",       f"${stats['min']:,.0f}")
    sc2.metric("Max",       f"${stats['max']:,.0f}")
    sc3.metric("Mean",      f"${stats['mean']:,.2f}")
    sc4.metric("Median",    f"${stats['median']:,.2f}")
    sc5.metric("Std Dev",   f"${stats['std']:,.2f}")
    sc6.metric("25th %ile", f"${stats['p25']:,.2f}")
    sc7.metric("75th %ile", f"${stats['p75']:,.2f}")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Total Amount Distribution")
        fig = px.histogram(
            dv, x="Total Amount", nbins=30,
            color_discrete_sequence=["#3b82d4"],
            labels={"Total Amount": "Total Amount ($)"},
        )
        fig.update_layout(margin=dict(t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Price per Unit Distribution")
        price_d = price_distribution(dv).reset_index()
        price_d.columns = ["Price per Unit", "Count"]
        fig2 = px.bar(
            price_d, x="Price per Unit", y="Count",
            color_discrete_sequence=["#7c5cd8"],
            labels={"Price per Unit": "Price ($)", "Count": "# Transactions"},
        )
        fig2.update_layout(margin=dict(t=20, b=20))
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Quantity Distribution")
        qty_d = quantity_distribution(dv).reset_index()
        qty_d.columns = ["Quantity", "Count"]
        fig3 = px.bar(
            qty_d, x="Quantity", y="Count",
            color_discrete_sequence=["#22c55e"],
            labels={"Quantity": "Units Ordered", "Count": "# Transactions"},
            text_auto=True,
        )
        fig3.update_layout(margin=dict(t=20, b=20))
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.subheader("Total Amount Box Plot by Category")
        fig4 = px.box(
            dv, x="Product Category", y="Total Amount",
            color="Product Category",
            color_discrete_sequence=px.colors.qualitative.Set2,
            labels={"Total Amount": "Total Amount ($)"},
        )
        fig4.update_layout(showlegend=False, margin=dict(t=20, b=20))
        st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Transaction Table")
    display_df = dv[[
        "Transaction ID", "Date", "Customer ID", "Gender", "Age",
        "Product Category", "Quantity", "Price per Unit", "Total Amount",
    ]].copy()
    display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")
    st.dataframe(
        display_df.sort_values("Date", ascending=False).reset_index(drop=True),
        use_container_width=True,
        height=400,
    )
    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=display_df.to_csv(index=False).encode("utf-8"),
        file_name="filtered_transactions.csv",
        mime="text/csv",
    )
