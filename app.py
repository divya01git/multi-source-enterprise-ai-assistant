"""
Enterprise AI Assistant
Main Streamlit Application
"""

from __future__ import annotations

import runpy
import sqlite3

import streamlit as st

from utils.config import DATABASE_PATH
from ui.components.styles import load_styles
from ui.components.admin_dashboard import render_admin_dashboard
from ui.components.employee_dashboard import render_employee_dashboard


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Enterprise AI Assistant",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# LOAD CUSTOM STYLES
# ============================================================

load_styles()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🏢 Enterprise AI Assistant")

st.sidebar.markdown(
    """
    <div style="color: #9ca3af; font-size: 13px; margin-bottom: 20px;">
        Multi-Source Enterprise Intelligence
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# ROLE SELECTION
# ============================================================

role = st.sidebar.selectbox(
    "Login As",
    [
        "Admin",
        "Employee",
    ],
)


# ============================================================
# EMPLOYEE SELECTION
# ============================================================

employee_id = None


if role == "Employee":

    conn = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            employee_id,
            employee_name
        FROM employees
        ORDER BY employee_name
        """
    )

    employees = cursor.fetchall()

    conn.close()


    if employees:

        employee_options = {
            employee_name: employee_id
            for employee_id, employee_name in employees
        }


        selected_employee = st.sidebar.selectbox(
            "Select Employee",
            list(employee_options.keys()),
        )


        employee_id = employee_options[
            selected_employee
        ]

    else:

        st.sidebar.error(
            "No employees found."
        )


# ============================================================
# NAVIGATION
# ============================================================

if role == "Admin":

    page = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "🤖 AI Assistant",
            "🗄️ Database",
            "📄 Documents",
            "🌐 Web Search",
        ],
    )

else:

    page = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "🤖 AI Assistant",
            "🌴 Leaves",
            "📄 Documents",
        ],
    )


# ============================================================
# PAGE ROUTING
# ============================================================

if page == "🏠 Dashboard":

    if role == "Admin":

        render_admin_dashboard()

    else:

        if employee_id is not None:

            render_employee_dashboard(
                employee_id
            )

        else:

            st.warning(
                "Please select an employee."
            )


elif page == "🤖 AI Assistant":

    runpy.run_path(
        "ui/pages/assistant.py"
    )


elif page == "🌴 Leaves":

    if employee_id is not None:

        st.session_state["selected_employee_id"] = employee_id

        runpy.run_path(
            "ui/pages/leaves.py"
        )

    else:

        st.warning(
            "Please select an employee."
        )


elif page == "🗄️ Database":

    runpy.run_path(
        "ui/pages/database.py"
    )


elif page == "📄 Documents":

    runpy.run_path(
        "ui/pages/documents.py"
    )


elif page == "🌐 Web Search":

    runpy.run_path(
        "ui/pages/websearch.py"
    )