"""
Enterprise AI Assistant
Seed Enterprise Database
"""

import sqlite3
import random
from pathlib import Path
from datetime import date, timedelta


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

DB_PATH = Path("database/company.db")

random.seed(42)


# ---------------------------------------------------------
# Sample Data
# ---------------------------------------------------------

FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Arjun", "Kabir",
    "Rohan", "Rahul", "Karan", "Ananya", "Aanya",
    "Diya", "Isha", "Meera", "Priya", "Riya",
    "Neha", "Simran", "Kavya", "Nisha", "Tanya"
]

LAST_NAMES = [
    "Sharma", "Gupta", "Verma", "Singh", "Kumar",
    "Mehta", "Kapoor", "Malhotra", "Bansal", "Agarwal"
]

DEPARTMENTS = [
    "Engineering",
    "Human Resources",
    "Finance",
    "Marketing",
    "Sales",
    "Operations",
    "IT",
    "Customer Support"
]

DESIGNATIONS = [
    "Software Engineer",
    "Senior Software Engineer",
    "Data Analyst",
    "HR Executive",
    "Financial Analyst",
    "Marketing Manager",
    "Sales Executive",
    "Operations Manager",
    "IT Specialist",
    "Support Executive"
]

INDUSTRIES = [
    "Technology",
    "Healthcare",
    "Finance",
    "Retail",
    "Education",
    "Manufacturing",
    "Telecommunications",
    "Logistics"
]

COUNTRIES = [
    "India",
    "United States",
    "United Kingdom",
    "Canada",
    "Australia",
    "Germany",
    "Singapore",
    "UAE"
]

CITIES = [
    "Chandigarh",
    "Delhi",
    "Mumbai",
    "Bengaluru",
    "Pune",
    "Hyderabad",
    "Chennai",
    "Gurugram"
]

PRODUCTS = [
    ("Cloud Pro", "Cloud Services", 499.99),
    ("AI Analytics Suite", "AI Software", 1299.99),
    ("Enterprise CRM", "Business Software", 899.99),
    ("Data Security Pro", "Cybersecurity", 749.99),
    ("Smart Dashboard", "Analytics", 599.99),
    ("Workflow Automation", "Automation", 699.99),
    ("Cloud Storage Plus", "Cloud Services", 299.99),
    ("AI Assistant Enterprise", "AI Software", 1499.99),
    ("Business Intelligence Pro", "Analytics", 1099.99),
    ("Network Security Suite", "Cybersecurity", 999.99),
    ("Project Manager Pro", "Business Software", 399.99),
    ("Data Warehouse Cloud", "Cloud Services", 1599.99),
    ("Customer Insights", "Analytics", 799.99),
    ("Marketing Automation", "Automation", 549.99),
    ("HR Management Suite", "Business Software", 649.99),
    ("Finance Intelligence", "Finance Software", 899.99),
    ("Predictive Analytics", "AI Software", 1799.99),
    ("API Gateway Enterprise", "Cloud Services", 1199.99),
    ("Secure Access Pro", "Cybersecurity", 449.99),
    ("Sales Intelligence", "Analytics", 999.99),
    ("Document AI", "AI Software", 1299.99),
    ("Inventory Manager", "Business Software", 499.99),
    ("DevOps Cloud", "Cloud Services", 899.99),
    ("Fraud Detection AI", "AI Software", 1899.99),
    ("Customer Support Hub", "Business Software", 599.99),
    ("Data Backup Enterprise", "Cybersecurity", 699.99),
    ("Supply Chain Analytics", "Analytics", 1399.99),
    ("Digital Workspace", "Business Software", 349.99),
    ("AI Forecasting", "AI Software", 1599.99),
    ("Enterprise Integration", "Automation", 1099.99),
]


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def random_date(start_date: date, end_date: date) -> str:

    days_between = (end_date - start_date).days

    random_days = random.randint(
        0,
        days_between
    )

    return (
        start_date
        + timedelta(days=random_days)
    ).isoformat()


# ---------------------------------------------------------
# Connect
# ---------------------------------------------------------

DB_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

conn = sqlite3.connect(
    DB_PATH
)

cursor = conn.cursor()

cursor.execute(
    "PRAGMA foreign_keys = ON"
)


# ---------------------------------------------------------
# Clear Existing Data
# ---------------------------------------------------------

cursor.execute(
    "DELETE FROM attendance"
)

cursor.execute(
    "DELETE FROM leave_requests"
)

cursor.execute(
    "DELETE FROM leave_balance"
)

cursor.execute(
    "DELETE FROM orders"
)

cursor.execute(
    "DELETE FROM sales"
)

cursor.execute(
    "DELETE FROM employees"
)

cursor.execute(
    "DELETE FROM customers"
)

cursor.execute(
    "DELETE FROM products"
)


# ---------------------------------------------------------
# Employees
# ---------------------------------------------------------

employee_ids = []

for i in range(40):

    first_name = random.choice(
        FIRST_NAMES
    )

    last_name = random.choice(
        LAST_NAMES
    )

    employee_name = (
        f"{first_name} {last_name}"
    )

    email = (
        f"{first_name.lower()}"
        f".{last_name.lower()}"
        f"{i + 1}@enterprise.com"
    )

    department = random.choice(
        DEPARTMENTS
    )

    designation = random.choice(
        DESIGNATIONS
    )

    salary = random.randint(
        35000,
        180000
    )

    joining_date = random_date(
        date(2018, 1, 1),
        date(2025, 12, 31)
    )

    cursor.execute(
        """
        INSERT INTO employees(
            employee_name,
            email,
            department,
            designation,
            salary,
            joining_date
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            employee_name,
            email,
            department,
            designation,
            salary,
            joining_date
        )
    )

    employee_ids.append(
        cursor.lastrowid
    )


# ---------------------------------------------------------
# Leave Balance
# ---------------------------------------------------------

for employee_id in employee_ids:

    cursor.execute(
        """
        INSERT INTO leave_balance(
            employee_id,
            casual_leave,
            sick_leave,
            earned_leave
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            employee_id,
            random.randint(3, 12),
            random.randint(2, 10),
            random.randint(5, 18)
        )
    )


# ---------------------------------------------------------
# Leave Requests
# ---------------------------------------------------------

leave_types = [
    "Casual",
    "Sick",
    "Earned"
]

leave_statuses = [
    "Pending",
    "Approved",
    "Rejected"
]

for _ in range(80):

    employee_id = random.choice(
        employee_ids
    )

    start_date = random_date(
        date(2025, 1, 1),
        date(2026, 7, 1)
    )

    end_date = start_date

    status = random.choice(
        leave_statuses
    )

    reason = random.choice(
        [
            "Personal work",
            "Medical appointment",
            "Family function",
            "Vacation",
            "Health reasons",
            "Emergency"
        ]
    )

    cursor.execute(
        """
        INSERT INTO leave_requests(
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
            random.choice(leave_types),
            start_date,
            end_date,
            reason,
            status
        )
    )


# ---------------------------------------------------------
# Attendance
# ---------------------------------------------------------

attendance_statuses = [
    "Present",
    "Absent",
    "Work From Home",
    "Half Day"
]

attendance_start = date(
    2026,
    1,
    1
)

for employee_id in employee_ids:

    for day in range(30):

        attendance_date = (
            attendance_start
            + timedelta(days=day)
        ).isoformat()

        status = random.choices(
            attendance_statuses,
            weights=[
                75,
                8,
                12,
                5
            ]
        )[0]

        cursor.execute(
            """
            INSERT INTO attendance(
                employee_id,
                attendance_date,
                status
            )
            VALUES (?, ?, ?)
            """,
            (
                employee_id,
                attendance_date,
                status
            )
        )


# ---------------------------------------------------------
# Customers
# ---------------------------------------------------------

customer_ids = []

for i in range(50):

    customer_name = (
        f"{random.choice(FIRST_NAMES)} "
        f"{random.choice(LAST_NAMES)} Enterprises"
    )

    industry = random.choice(
        INDUSTRIES
    )

    country = random.choice(
        COUNTRIES
    )

    cursor.execute(
        """
        INSERT INTO customers(
            customer_name,
            industry,
            country
        )
        VALUES (?, ?, ?)
        """,
        (
            customer_name,
            industry,
            country
        )
    )

    customer_ids.append(
        cursor.lastrowid
    )


# ---------------------------------------------------------
# Products
# ---------------------------------------------------------

product_ids = []

for product in PRODUCTS:

    cursor.execute(
        """
        INSERT INTO products(
            product_name,
            category,
            price
        )
        VALUES (?, ?, ?)
        """,
        product
    )

    product_ids.append(
        cursor.lastrowid
    )


# ---------------------------------------------------------
# Orders
# ---------------------------------------------------------

for _ in range(300):

    customer_id = random.choice(
        customer_ids
    )

    product_id = random.choice(
        product_ids
    )

    quantity = random.randint(
        1,
        20
    )

    order_date = random_date(
        date(2024, 1, 1),
        date(2026, 7, 1)
    )

    cursor.execute(
        """
        INSERT INTO orders(
            customer_id,
            product_id,
            quantity,
            order_date
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            customer_id,
            product_id,
            quantity,
            order_date
        )
    )


# ---------------------------------------------------------
# Sales
# ---------------------------------------------------------

start_month = date(
    2024,
    7,
    1
)

for month_number in range(24):

    month_date = (
        start_month
        + timedelta(
            days=month_number * 30
        )
    )

    month = month_date.strftime(
        "%Y-%m"
    )

    revenue = random.randint(
        150000,
        900000
    )

    expenses = random.randint(
        50000,
        450000
    )

    profit = revenue - expenses

    cursor.execute(
        """
        INSERT INTO sales(
            month,
            revenue,
            expenses,
            profit
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            month,
            revenue,
            expenses,
            profit
        )
    )


# ---------------------------------------------------------
# Commit
# ---------------------------------------------------------

conn.commit()


# ---------------------------------------------------------
# Verification
# ---------------------------------------------------------

tables = [
    "employees",
    "leave_balance",
    "leave_requests",
    "attendance",
    "customers",
    "products",
    "orders",
    "sales"
]

print("=" * 60)
print("DATABASE SEEDED SUCCESSFULLY")
print("=" * 60)

for table in tables:

    cursor.execute(
        f"SELECT COUNT(*) FROM {table}"
    )

    count = cursor.fetchone()[0]

    print(
        f"{table:<20} {count} rows"
    )

print("=" * 60)


conn.close()