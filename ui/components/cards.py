"""
Enterprise AI Assistant
Reusable Dashboard Cards
"""

from __future__ import annotations

import html

import streamlit as st


# =====================================================
# BASE METRIC CARD
# =====================================================

def metric_card(
    title: str,
    value,
    icon: str = "📊",
    delta: str | None = None,
) -> None:

    safe_title = html.escape(
        str(title)
    )

    safe_value = html.escape(
        str(value)
    )

    delta_html = ""

    if delta:

        safe_delta = html.escape(
            str(delta)
        )

        delta_html = f"""
        <div class="metric-delta">
            {safe_delta}
        </div>
        """


    card_html = f"""
    <div class="metric-card">

        <div class="metric-icon">
            {icon}
        </div>

        <div class="metric-title">
            {safe_title}
        </div>

        <div class="metric-value">
            {safe_value}
        </div>

        {delta_html}

    </div>
    """


    st.html(
        card_html
    )


# =====================================================
# BUSINESS CARDS
# =====================================================

def revenue_card(
    value,
) -> None:

    metric_card(
        title="Revenue",
        value=f"₹{value:,.0f}",
        icon="💰",
    )


def profit_card(
    value,
) -> None:

    metric_card(
        title="Profit",
        value=f"₹{value:,.0f}",
        icon="📈",
    )


def expense_card(
    value,
) -> None:

    metric_card(
        title="Expenses",
        value=f"₹{value:,.0f}",
        icon="💸",
    )


def employee_card(
    value,
) -> None:

    metric_card(
        title="Employees",
        value=value,
        icon="👨‍💼",
    )


def customer_card(
    value,
) -> None:

    metric_card(
        title="Customers",
        value=value,
        icon="👥",
    )


def order_card(
    value,
) -> None:

    metric_card(
        title="Orders",
        value=value,
        icon="🛒",
    )


# =====================================================
# EMPLOYEE CARDS
# =====================================================

def attendance_card(
    value,
) -> None:

    metric_card(
        title="Attendance",
        value=f"{value}%",
        icon="🗓️",
    )


def leave_card(
    value,
) -> None:

    metric_card(
        title="Leaves Remaining",
        value=value,
        icon="🌴",
    )


def salary_card(
    status,
) -> None:

    metric_card(
        title="Salary Status",
        value=status,
        icon="💵",
    )


def department_card(
    name,
) -> None:

    metric_card(
        title="Department",
        value=name,
        icon="🏢",
    )