"""
Enterprise AI Assistant
Database Explorer
"""

from __future__ import annotations

import sqlite3

import pandas as pd
import streamlit as st

from utils.config import DATABASE_PATH


# ---------------------------------------
# Database Functions
# ---------------------------------------

def get_connection():

    conn = sqlite3.connect(
        DATABASE_PATH
    )

    conn.row_factory = sqlite3.Row

    return conn


def get_tables():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name
        """
    )

    tables = [
        row["name"]
        for row in cursor.fetchall()
    ]

    conn.close()

    return tables


def get_table_row_count(
    table_name: str
) -> int:

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        f"""
        SELECT COUNT(*)
        FROM "{table_name}"
        """
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


def execute_query(
    query: str
) -> pd.DataFrame:

    conn = get_connection()

    try:

        dataframe = pd.read_sql_query(
            query,
            conn
        )

        return dataframe

    finally:

        conn.close()


# ---------------------------------------
# CSS
# ---------------------------------------

st.markdown(
    """
    <style>

    .header{
        padding:20px;
        border-radius:18px;
        background:linear-gradient(90deg,#0F172A,#1E3A8A);
        color:white;
        margin-bottom:25px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------
# Header
# ---------------------------------------

st.markdown(
    """
    <div class="header">

    <h2>🗄 Database Explorer</h2>

    <p>
    Browse your enterprise database, execute SQL queries and inspect tables.
    </p>

    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------
# Database Overview
# ---------------------------------------

tables = get_tables()

total_rows = sum(
    get_table_row_count(table)
    for table in tables
)


c1, c2, c3 = st.columns(3)


with c1:

    st.metric(
        "Database",
        "SQLite",
        "Connected"
    )


with c2:

    st.metric(
        "Tables",
        len(tables)
    )


with c3:

    st.metric(
        "Total Records",
        total_rows
    )


st.divider()


# ---------------------------------------
# SQL Workspace
# ---------------------------------------

st.subheader(
    "🧑‍💻 SQL Workspace"
)


query = st.text_area(
    "Write SQL Query",
    value="SELECT * FROM customers LIMIT 10;",
    height=140
)


execute = st.button(
    "▶ Execute Query",
    width="stretch"
)


if execute:

    if not query.strip():

        st.warning(
            "Please enter a SQL query."
        )

    else:

        try:

            result = execute_query(
                query
            )

            st.success(
                f"Query executed successfully. "
                f"{len(result)} rows returned."
            )

            st.subheader(
                "📊 Query Results"
            )

            st.dataframe(
                result,
                width="stretch",
                hide_index=True
            )

        except Exception as error:

            st.error(
                f"Query failed: {error}"
            )


st.divider()


# ---------------------------------------
# Available Tables
# ---------------------------------------

st.subheader(
    "📚 Available Tables"
)


table_data = []


for table in tables:

    table_data.append(
        {
            "Table": table,
            "Rows": get_table_row_count(
                table
            )
        }
    )


tables_dataframe = pd.DataFrame(
    table_data
)


st.dataframe(
    tables_dataframe,
    width="stretch",
    hide_index=True
)


st.success(
    "✅ Database connection is active."
)