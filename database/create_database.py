"""
Enterprise AI Assistant
Create Enterprise Database
"""

import sqlite3
from pathlib import Path

DB_PATH = Path("database/company.db")

DB_PATH.parent.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

# =====================================================
# EMPLOYEES
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees(
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_name TEXT NOT NULL,
    email TEXT UNIQUE,
    department TEXT,
    designation TEXT,
    salary REAL,
    joining_date TEXT
)
""")

# =====================================================
# LEAVE BALANCE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS leave_balance(
    employee_id INTEGER PRIMARY KEY,
    casual_leave INTEGER DEFAULT 12,
    sick_leave INTEGER DEFAULT 10,
    earned_leave INTEGER DEFAULT 18,
    FOREIGN KEY(employee_id)
    REFERENCES employees(employee_id)
)
""")

# =====================================================
# LEAVE REQUESTS
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS leave_requests(
    request_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    leave_type TEXT,
    start_date TEXT,
    end_date TEXT,
    reason TEXT,
    status TEXT DEFAULT 'Pending',
    FOREIGN KEY(employee_id)
    REFERENCES employees(employee_id)
)
""")

# =====================================================
# ATTENDANCE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance(
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    attendance_date TEXT,
    status TEXT,
    FOREIGN KEY(employee_id)
    REFERENCES employees(employee_id)
)
""")

# =====================================================
# CUSTOMERS
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers(
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    industry TEXT,
    country TEXT
)
""")

# =====================================================
# PRODUCTS
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS products(
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT,
    category TEXT,
    price REAL
)
""")

# =====================================================
# ORDERS
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    order_date TEXT,
    FOREIGN KEY(customer_id)
    REFERENCES customers(customer_id),
    FOREIGN KEY(product_id)
    REFERENCES products(product_id)
)
""")

# =====================================================
# SALES
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales(
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    month TEXT,
    revenue REAL,
    expenses REAL,
    profit REAL
)
""")

conn.commit()
conn.close()

print("=" * 60)
print("Enterprise database created successfully.")
print("=" * 60)