"""
Enterprise Dashboard Charts
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st


# =====================================================
# REVENUE CHART
# =====================================================

def revenue_chart(df: pd.DataFrame) -> None:

    if df.empty:
        st.info("No revenue data available.")
        return

    fig = px.line(
        df,
        x="month",
        y="revenue",
        markers=True,
        title="Monthly Revenue Trend",
    )

    fig.update_layout(
        height=420,
        margin=dict(
            l=10,
            r=10,
            t=50,
            b=10,
        ),
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )


# =====================================================
# EXPENSE CHART
# =====================================================

def expense_chart(df: pd.DataFrame) -> None:

    if df.empty:
        st.info("No expense data available.")
        return

    fig = px.pie(
        df,
        values="amount",
        names="category",
        hole=0.45,
        title="Expense Breakdown",
    )

    fig.update_layout(
        height=420,
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )


# =====================================================
# DEPARTMENT CHART
# =====================================================

def department_chart(df: pd.DataFrame) -> None:

    if df.empty:
        st.info("No employee data available.")
        return

    chart = (
        df
        .groupby("department")
        .size()
        .reset_index(
            name="employees"
        )
    )

    fig = px.bar(
        chart,
        x="department",
        y="employees",
        text="employees",
        title="Employees by Department",
    )

    fig.update_layout(
        height=420,
        xaxis_title="Department",
        yaxis_title="Employees",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )


# =====================================================
# PROFIT CHART
# =====================================================

def profit_chart(
    revenue_df: pd.DataFrame,
    expense_df: pd.DataFrame,
) -> None:

    if (
        revenue_df.empty
        or expense_df.empty
    ):

        st.info(
            "Profit data unavailable."
        )

        return

    total_revenue = (
        revenue_df["revenue"]
        .sum()
    )

    total_expenses = (
        expense_df["amount"]
        .sum()
    )

    total_profit = (
        total_revenue
        - total_expenses
    )

    chart_df = pd.DataFrame(
        {
            "Metric": [
                "Revenue",
                "Expenses",
                "Profit",
            ],
            "Amount": [
                total_revenue,
                total_expenses,
                total_profit,
            ],
        }
    )

    fig = px.bar(
        chart_df,
        x="Metric",
        y="Amount",
        text="Amount",
        title="Revenue, Expenses & Profit",
    )

    fig.update_layout(
        height=420,
        xaxis_title="",
        yaxis_title="Amount (₹)",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )


# =====================================================
# ATTENDANCE CHART
# =====================================================

def attendance_chart(df: pd.DataFrame) -> None:

    if df.empty:
        st.info(
            "Attendance data unavailable."
        )

        return

    fig = px.line(
        df,
        x="month",
        y="attendance",
        markers=True,
        title="Attendance Trend",
    )

    fig.update_layout(
        height=420,
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )