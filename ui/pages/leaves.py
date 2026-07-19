"""
Enterprise AI Assistant
Employee Leave Management
"""

from __future__ import annotations

import sqlite3
from datetime import date

import pandas as pd
import streamlit as st

from utils.config import DATABASE_PATH


# ============================================================
# SELECTED EMPLOYEE
# ============================================================

employee_id = st.session_state.get(
    "selected_employee_id"
)


if employee_id is None:

    st.error(
        "No employee selected."
    )

    st.stop()


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    conn = sqlite3.connect(
        DATABASE_PATH
    )

    conn.row_factory = sqlite3.Row

    return conn


# ============================================================
# EMPLOYEE DETAILS
# ============================================================

conn = get_connection()

cursor = conn.cursor()

cursor.execute(
    """
    SELECT
        employee_name,
        department
    FROM employees
    WHERE employee_id = ?
    """,
    (
        employee_id,
    ),
)

employee = cursor.fetchone()

conn.close()


if employee is None:

    st.error(
        "Employee not found."
    )

    st.stop()


# ============================================================
# HEADER
# ============================================================

st.title(
    "🌴 Leave Management"
)

st.write(
    f"Manage your leave balance and submit leave requests, "
    f"{employee['employee_name']}."
)


# ============================================================
# LEAVE BALANCE
# ============================================================

conn = get_connection()

cursor = conn.cursor()

cursor.execute(
    """
    SELECT
        casual_leave,
        sick_leave,
        earned_leave
    FROM leave_balance
    WHERE employee_id = ?
    """,
    (
        employee_id,
    ),
)

leave_balance = cursor.fetchone()

conn.close()


if leave_balance:

    casual_leave = (
        leave_balance["casual_leave"]
        or 0
    )

    sick_leave = (
        leave_balance["sick_leave"]
        or 0
    )

    earned_leave = (
        leave_balance["earned_leave"]
        or 0
    )

else:

    casual_leave = 0

    sick_leave = 0

    earned_leave = 0


total_leave = (

    casual_leave
    + sick_leave
    + earned_leave

)


# ============================================================
# LEAVE BALANCE DISPLAY
# ============================================================

st.subheader(
    "📊 Leave Balance"
)


c1, c2, c3, c4 = st.columns(
    4,
    gap="medium",
)


with c1:

    st.metric(
        "🌴 Total Remaining",
        total_leave,
    )


with c2:

    st.metric(
        "🏖️ Casual Leave",
        casual_leave,
    )


with c3:

    st.metric(
        "🤒 Sick Leave",
        sick_leave,
    )


with c4:

    st.metric(
        "🌿 Earned Leave",
        earned_leave,
    )


st.divider()


# ============================================================
# APPLY FOR LEAVE
# ============================================================

st.subheader(
    "📝 Apply for Leave"
)


with st.form(
    "leave_application_form"
):

    leave_type = st.selectbox(
        "Leave Type",
        [
            "Casual",
            "Sick",
            "Earned",
        ],
    )


    col1, col2 = st.columns(
        2
    )


    with col1:

        start_date = st.date_input(
            "Start Date",
            value=date.today(),
        )


    with col2:

        end_date = st.date_input(
            "End Date",
            value=date.today(),
        )


    reason = st.text_area(
        "Reason",
        placeholder="Enter the reason for your leave...",
        height=120,
    )


    submit = st.form_submit_button(
        "📤 Submit Leave Request",
        width="stretch",
    )


# ============================================================
# SUBMIT LEAVE REQUEST
# ============================================================

if submit:

    if end_date < start_date:

        st.error(
            "End date cannot be before start date."
        )

    elif not reason.strip():

        st.error(
            "Please enter a reason for the leave."
        )

    else:

        requested_days = (
            end_date
            - start_date
        ).days + 1


        available_leave = {

            "Casual": casual_leave,

            "Sick": sick_leave,

            "Earned": earned_leave,

        }[
            leave_type
        ]


        if requested_days > available_leave:

            st.error(
                f"You have only "
                f"{available_leave} "
                f"{leave_type.lower()} leave(s) available."
            )

        else:

            conn = get_connection()

            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO leave_requests (
                    employee_id,
                    leave_type,
                    start_date,
                    end_date,
                    reason,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    employee_id,
                    leave_type,
                    start_date.isoformat(),
                    end_date.isoformat(),
                    reason.strip(),
                    "Pending",
                ),
            )

            conn.commit()

            conn.close()


            st.success(
                "✅ Leave request submitted successfully!"
            )


            st.rerun()


# ============================================================
# MY LEAVE REQUESTS
# ============================================================

st.divider()


st.subheader(
    "📋 My Leave Requests"
)


conn = get_connection()

requests_df = pd.read_sql_query(
    """
    SELECT
        leave_type AS "Leave Type",
        start_date AS "Start Date",
        end_date AS "End Date",
        reason AS "Reason",
        status AS "Status"
    FROM leave_requests
    WHERE employee_id = ?
    ORDER BY request_id DESC
    """,
    conn,
    params=(
        employee_id,
    ),
)

conn.close()


if requests_df.empty:

    st.info(
        "You have not submitted any leave requests yet."
    )

else:

    st.dataframe(
        requests_df,
        width="stretch",
        hide_index=True,
    )