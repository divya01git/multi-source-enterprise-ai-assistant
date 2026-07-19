"""
Enterprise Employee Dashboard
"""

from __future__ import annotations

import sqlite3

import streamlit as st

from utils.config import DATABASE_PATH

from ui.components.cards import (
    attendance_card,
    leave_card,
    salary_card,
    department_card,
)


# -----------------------------------------------------
# Database Helpers
# -----------------------------------------------------

def get_employee_data(employee_id: int):

    conn = sqlite3.connect(
        DATABASE_PATH
    )

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()


    # -------------------------------------------------
    # Employee Details
    # -------------------------------------------------

    cursor.execute(
        """
        SELECT
            employee_id,
            employee_name,
            department,
            designation,
            salary,
            joining_date
        FROM employees
        WHERE employee_id = ?
        """,
        (employee_id,)
    )

    employee = cursor.fetchone()


    # -------------------------------------------------
    # Leave Balance
    # -------------------------------------------------

    cursor.execute(
        """
        SELECT
            casual_leave,
            sick_leave,
            earned_leave
        FROM leave_balance
        WHERE employee_id = ?
        """,
        (employee_id,)
    )

    leave_balance = cursor.fetchone()


    # -------------------------------------------------
    # Attendance Summary
    # -------------------------------------------------

    cursor.execute(
        """
        SELECT
            COUNT(*) AS total_days,
            SUM(
                CASE
                    WHEN status = 'Present'
                    THEN 1
                    ELSE 0
                END
            ) AS present_days
        FROM attendance
        WHERE employee_id = ?
        """,
        (employee_id,)
    )

    attendance = cursor.fetchone()


    # -------------------------------------------------
    # Monthly Attendance
    # -------------------------------------------------

    cursor.execute(
        """
        SELECT
            substr(attendance_date, 1, 7) AS month,
            ROUND(
                100.0 *
                SUM(
                    CASE
                        WHEN status = 'Present'
                        THEN 1
                        ELSE 0
                    END
                )
                / COUNT(*),
                1
            ) AS attendance_percentage
        FROM attendance
        WHERE employee_id = ?
        GROUP BY substr(attendance_date, 1, 7)
        ORDER BY month
        """,
        (employee_id,)
    )

    monthly_attendance = [
        dict(row)
        for row in cursor.fetchall()
    ]


    conn.close()


    return (
        employee,
        leave_balance,
        attendance,
        monthly_attendance
    )


# -----------------------------------------------------
# Dashboard
# -----------------------------------------------------

def render_employee_dashboard(
    employee_id: int
):

    (
        employee,
        leave_balance,
        attendance,
        monthly_attendance
    ) = get_employee_data(
        employee_id
    )


    if employee is None:

        st.error(
            "Employee not found."
        )

        return


    employee_name = employee[
        "employee_name"
    ]


    department = employee[
        "department"
    ]


    # -------------------------------------------------
    # Attendance Percentage
    # -------------------------------------------------

    total_days = (
        attendance["total_days"]
        or 0
    )


    present_days = (
        attendance["present_days"]
        or 0
    )


    if total_days > 0:

        attendance_percentage = round(
            (
                present_days
                / total_days
            )
            * 100,
            1
        )

    else:

        attendance_percentage = 0


    # -------------------------------------------------
    # Total Leaves
    # -------------------------------------------------

    if leave_balance:

        total_leaves = (

            leave_balance[
                "casual_leave"
            ]

            +

            leave_balance[
                "sick_leave"
            ]

            +

            leave_balance[
                "earned_leave"
            ]

        )

    else:

        total_leaves = 0


    # -------------------------------------------------
    # Header
    # -------------------------------------------------

    st.markdown(
        f"""
<div class="hero">

<h1>👋 Welcome, {employee_name}</h1>

<p>
Your Personal Enterprise Workspace
</p>

</div>
""",
        unsafe_allow_html=True,
    )


    # -------------------------------------------------
    # Summary Cards
    # -------------------------------------------------

    c1, c2 = st.columns(2)


    with c1:

        attendance_card(
            attendance_percentage
        )


    with c2:

        leave_card(
            total_leaves
        )


    c3, c4 = st.columns(2)


    with c3:

        salary_card(
            "Credited"
        )


    with c4:

        department_card(
            department
        )


    # -------------------------------------------------
    # Attendance
    # -------------------------------------------------

    st.markdown(
        "## 📅 Attendance"
    )


    if monthly_attendance:

        st.line_chart(
            monthly_attendance,
            x="month",
            y="attendance_percentage",
            width="stretch",
        )

    else:

        st.info(
            "No attendance data available."
        )


    # -------------------------------------------------
    # Leave Summary
    # -------------------------------------------------

    st.markdown(
        "## 🌴 Leave Summary"
    )


    if leave_balance:

        leave_data = {

            "Leave Type": [

                "Casual",

                "Sick",

                "Earned",

            ],

            "Available": [

                leave_balance[
                    "casual_leave"
                ],

                leave_balance[
                    "sick_leave"
                ],

                leave_balance[
                    "earned_leave"
                ],

            ]

        }


        st.dataframe(
            leave_data,
            width="stretch",
            hide_index=True,
        )

    else:

        st.info(
            "No leave balance found."
        )


    # -------------------------------------------------
    # Upcoming Holidays
    # -------------------------------------------------

    st.markdown(
        "## 🎉 Upcoming Holidays"
    )


    holiday_data = {

        "Date": [

            "15 Aug",

            "02 Oct",

            "25 Dec",

        ],

        "Holiday": [

            "Independence Day",

            "Gandhi Jayanti",

            "Christmas",

        ]

    }


    st.dataframe(
        holiday_data,
        width="stretch",
        hide_index=True,
    )


    # -------------------------------------------------
    # AI Assistant
    # -------------------------------------------------

    st.markdown(
        "## 🤖 Enterprise AI"
    )


    st.info(
        """
Try asking:

• How many leaves do I have left?

• Show my attendance.

• What is my department?

• What is my designation?

Use the AI Assistant page to ask these questions.
"""
    )