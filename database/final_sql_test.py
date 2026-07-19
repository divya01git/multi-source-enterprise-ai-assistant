"""
Final SQL Database Verification
"""

from __future__ import annotations

import sqlite3

from utils.config import DATABASE_PATH


TEST_QUERIES = {
    "Employee Count": """
        SELECT COUNT(*) AS total_employees
        FROM employees
    """,

    "Total Revenue": """
        SELECT SUM(revenue) AS total_revenue
        FROM sales
    """,

    "Department Employee Count": """
        SELECT
            department,
            COUNT(*) AS employee_count
        FROM employees
        GROUP BY department
    """,

    "Top Selling Product": """
        SELECT
            p.product_name,
            SUM(o.quantity * p.price) AS total_sales
        FROM orders o
        JOIN products p
            ON o.product_id = p.product_id
        GROUP BY p.product_name
        ORDER BY total_sales DESC
        LIMIT 1
    """,

    "Customers and Orders": """
        SELECT
            c.customer_name,
            o.order_id,
            o.quantity,
            o.order_date
        FROM customers c
        JOIN orders o
            ON c.customer_id = o.customer_id
        LIMIT 10
    """,

    "Total Revenue and Expenses": """
        SELECT
            SUM(revenue) AS total_revenue,
            SUM(expenses) AS total_expenses
        FROM sales
    """,
}


def run_tests() -> None:

    print("=" * 80)
    print("FINAL DATABASE VERIFICATION")
    print("=" * 80)

    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    passed = 0
    failed = 0

    try:

        for name, query in TEST_QUERIES.items():

            print("\n" + "-" * 80)
            print(name)
            print("-" * 80)

            try:

                cursor.execute(query)

                rows = [
                    dict(row)
                    for row in cursor.fetchall()
                ]

                print("PASS")
                print("Rows:", rows[:5])

                passed += 1

            except Exception as exc:

                print("FAIL")
                print("Error:", exc)

                failed += 1

    finally:

        conn.close()

    print("\n" + "=" * 80)
    print("FINAL DATABASE TEST SUMMARY")
    print("=" * 80)

    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    if failed == 0:
        print("\nDATABASE VERIFICATION COMPLETE")
    else:
        print("\nDATABASE VERIFICATION REQUIRES ATTENTION")


if __name__ == "__main__":
    run_tests()