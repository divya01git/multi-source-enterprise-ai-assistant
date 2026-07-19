"""
Enterprise Dashboard
"""

from __future__ import annotations

import sqlite3

import streamlit as st

from utils.config import DATABASE_PATH
from ui.components.styles import load_styles
from ui.components.admin_dashboard import render_admin_dashboard
from ui.components.employee_dashboard import render_employee_dashboard


# -----------------------------------------------------
# Page Configuration
# -----------------------------------------------------

st.set_page_config(
    page_title="Enterprise Dashboard",
    page_icon="🏢",
    layout="wide",
)


load_styles()


# -----------------------------------------------------
# Load Employees
# -----------------------------------------------------

def get_employees():

    conn = sqlite3.connect(
        DATABASE_PATH
    )

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            employee_id,
            employee_name,
            department,
            designation
        FROM employees
        ORDER BY employee_name
        """
    )

    employees = [
        dict(row)
        for row in cursor.fetchall()
    ]

    conn.close()

    return employees


# -----------------------------------------------------
# Sidebar
# -----------------------------------------------------

st.sidebar.title(
    "Enterprise Portal"
)


role = st.sidebar.selectbox(
    "Login As",
    [
        "Admin",
        "Employee",
    ],
)


# -----------------------------------------------------
# Admin Dashboard
# -----------------------------------------------------

if role == "Admin":

    render_admin_dashboard()


# -----------------------------------------------------
# Employee Dashboard
# -----------------------------------------------------

else:

    employees = get_employees()


    if not employees:

        st.error(
            "No employees found in the database."
        )

        st.stop()


    employee_options = {

        f"{employee['employee_name']} "
        f"— {employee['department']} "
        f"({employee['designation']})":

        employee["employee_id"]

        for employee in employees

    }


    selected_employee = st.sidebar.selectbox(
        "Select Employee",
        list(
            employee_options.keys()
        ),
    )


    employee_id = employee_options[
        selected_employee
    ]


    # Store selected employee globally
    # for this Streamlit session

    st.session_state[
        "current_employee_id"
    ] = employee_id


    st.session_state[
        "current_employee_name"
    ] = selected_employee.split(
        " — "
    )[0]


    render_employee_dashboard(
        employee_id
    )