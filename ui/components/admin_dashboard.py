"""
Enterprise Admin Dashboard
"""

from __future__ import annotations

import sqlite3

import pandas as pd
import streamlit as st

from utils.config import DATABASE_PATH

from ui.components.cards import (
    revenue_card,
    profit_card,
    expense_card,
    employee_card,
    customer_card,
    order_card,
)

from ui.components.charts import (
    revenue_chart,
    expense_chart,
    department_chart,
    profit_chart,
)


# =====================================================
# DATABASE HELPERS
# =====================================================

def fetch(query: str) -> pd.DataFrame:

    conn = sqlite3.connect(
        DATABASE_PATH
    )

    try:

        return pd.read_sql_query(
            query,
            conn,
        )

    finally:

        conn.close()


def scalar(
    query: str,
    default=0,
):

    try:

        conn = sqlite3.connect(
            DATABASE_PATH
        )

        cursor = conn.cursor()

        cursor.execute(
            query
        )

        result = cursor.fetchone()

        conn.close()

        if not result:

            return default

        if result[0] is None:

            return default

        return result[0]

    except Exception:

        return default


# =====================================================
# ADMIN DASHBOARD
# =====================================================

def render_admin_dashboard():

    # -------------------------------------------------
    # HEADER
    # -------------------------------------------------

    st.html(
    """
    <div class="hero">

        <h1>
            🏢 ABC Technologies Pvt. Ltd.
        </h1>

        <p>
            Enterprise Business Intelligence Dashboard
        </p>

    </div>
    """
        )

    # =================================================
    # KPI VALUES
    # =================================================

    revenue = scalar(
        """
        SELECT
            SUM(revenue)
        FROM sales
        """
    )


    expenses = scalar(
        """
        SELECT
            SUM(expenses)
        FROM sales
        """
    )


    profit = scalar(
        """
        SELECT
            SUM(profit)
        FROM sales
        """
    )


    customers = scalar(
        """
        SELECT
            COUNT(*)
        FROM customers
        """
    )


    employees = scalar(
        """
        SELECT
            COUNT(*)
        FROM employees
        """
    )


    orders = scalar(
        """
        SELECT
            COUNT(*)
        FROM orders
        """
    )


    # =================================================
    # BUSINESS OVERVIEW
    # =================================================

    st.markdown(
        "### 📊 Business Overview"
    )


    c1, c2, c3 = st.columns(
        3,
        gap="medium",
    )


    with c1:

        revenue_card(
            revenue
        )


    with c2:

        profit_card(
            profit
        )


    with c3:

        expense_card(
            expenses
        )


    c4, c5, c6 = st.columns(
        3,
        gap="medium",
    )


    with c4:

        employee_card(
            employees
        )


    with c5:

        customer_card(
            customers
        )


    with c6:

        order_card(
            orders
        )


    # =================================================
    # BUSINESS ANALYTICS
    # =================================================

    st.markdown(
        "### 📈 Business Analytics"
    )


    # -------------------------------------------------
    # REVENUE DATA
    # -------------------------------------------------

    revenue_df = fetch(
        """
        SELECT

            month,

            revenue

        FROM sales

        ORDER BY sale_id
        """
    )


    # -------------------------------------------------
    # EXPENSE DATA
    # -------------------------------------------------

    expense_df = fetch(
        """
        SELECT

            month AS category,

            expenses AS amount

        FROM sales

        ORDER BY sale_id
        """
    )


    # -------------------------------------------------
    # EMPLOYEE DATA
    # -------------------------------------------------

    employee_df = fetch(
        """
        SELECT

            department

        FROM employees

        WHERE department IS NOT NULL
        """
    )


    # =================================================
    # CHART ROW 1
    # =================================================

    left, right = st.columns(
        2,
        gap="large",
    )


    with left:

        revenue_chart(
            revenue_df
        )


    with right:

        expense_chart(
            expense_df
        )


    # =================================================
    # CHART ROW 2
    # =================================================

    left, right = st.columns(
        2,
        gap="large",
    )


    with left:

        department_chart(
            employee_df
        )


    with right:

        profit_chart(
            revenue_df,
            expense_df,
        )


    # =================================================
    # RECENT ORDERS
    # =================================================

    st.markdown(
        "### 🛒 Recent Orders"
    )


    orders_df = fetch(
        """
        SELECT

            o.order_id,

            c.customer_name,

            p.product_name,

            o.quantity,

            o.order_date

        FROM orders o

        LEFT JOIN customers c

            ON o.customer_id = c.customer_id

        LEFT JOIN products p

            ON o.product_id = p.product_id

        ORDER BY

            o.order_date DESC

        LIMIT 10
        """
    )


    if orders_df.empty:

        st.info(
            "No recent orders found."
        )

    else:

        st.dataframe(
            orders_df,
            width="stretch",
            hide_index=True,
        )


    # =================================================
    # AI INSIGHTS
    # =================================================

    st.markdown(
        "### 🤖 AI Business Insights"
    )


    st.info(
        """
        **Enterprise Intelligence Available**

        Ask the AI Assistant about:

        • Business revenue and expenses

        • Employees and departments

        • Customers and orders

        • Company documents

        • Latest web information

        The AI system automatically routes each question
        to the appropriate data source.
        """
    )