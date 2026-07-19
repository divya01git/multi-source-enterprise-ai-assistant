"""
Enterprise AI Assistant
Insert Sample Enterprise Data
"""

import sqlite3
import random
from datetime import date, timedelta

conn = sqlite3.connect("database/company.db")
cursor = conn.cursor()

# =====================================================
# EMPLOYEES
# =====================================================

employees = [
    ("Amit Sharma","amit@company.com","Sales","Sales Executive",60000,"2022-01-10"),
    ("Neha Gupta","neha@company.com","HR","HR Manager",65000,"2021-05-18"),
    ("Rahul Verma","rahul@company.com","Engineering","Software Engineer",90000,"2023-02-11"),
    ("Priya Singh","priya@company.com","Finance","Finance Manager",80000,"2020-07-20"),
    ("Karan Mehta","karan@company.com","Marketing","Marketing Executive",62000,"2022-09-12"),
    ("Riya Kapoor","riya@company.com","HR","HR Executive",52000,"2023-04-18"),
    ("Mohit Jain","mohit@company.com","Engineering","Backend Developer",87000,"2022-11-01"),
    ("Sneha Arora","sneha@company.com","Engineering","Frontend Developer",85000,"2021-08-15"),
    ("Vikas Kumar","vikas@company.com","Sales","Sales Manager",76000,"2020-12-09"),
    ("Anjali Sharma","anjali@company.com","Finance","Accountant",58000,"2023-01-01")
]

cursor.executemany("""
INSERT INTO employees(
employee_name,
email,
department,
designation,
salary,
joining_date
)
VALUES(?,?,?,?,?,?)
""", employees)

# =====================================================
# LEAVE BALANCE
# =====================================================

leave_balance = []

for emp in range(1,11):

    casual = random.randint(4,12)
    sick = random.randint(3,10)
    earned = random.randint(8,18)

    leave_balance.append(
        (
            emp,
            casual,
            sick,
            earned
        )
    )

cursor.executemany("""
INSERT INTO leave_balance
VALUES(?,?,?,?)
""", leave_balance)

# =====================================================
# LEAVE REQUESTS
# =====================================================

requests = [
(1,"Casual","2026-07-20","2026-07-22","Family Function","Approved"),
(2,"Sick","2026-06-12","2026-06-14","Medical","Approved"),
(3,"Earned","2026-08-01","2026-08-05","Vacation","Pending"),
(5,"Casual","2026-07-25","2026-07-25","Personal Work","Pending"),
(7,"Sick","2026-07-02","2026-07-03","Fever","Rejected")
]

cursor.executemany("""
INSERT INTO leave_requests(
employee_id,
leave_type,
start_date,
end_date,
reason,
status
)
VALUES(?,?,?,?,?,?)
""", requests)

# =====================================================
# ATTENDANCE
# =====================================================

attendance = []

today = date.today()

for emp in range(1,11):

    for i in range(15):

        d = today - timedelta(days=i)

        status = random.choice(
            [
                "Present",
                "Present",
                "Present",
                "Present",
                "Absent"
            ]
        )

        attendance.append(
            (
                emp,
                str(d),
                status
            )
        )

cursor.executemany("""
INSERT INTO attendance(
employee_id,
attendance_date,
status
)
VALUES(?,?,?)
""", attendance)

# =====================================================
# CUSTOMERS
# =====================================================

customers = [
("TechNova","Technology","India"),
("GreenLeaf","Agriculture","India"),
("FutureSoft","Software","Canada"),
("Prime Healthcare","Healthcare","India"),
("Sky Retail","Retail","USA")
]

cursor.executemany("""
INSERT INTO customers(
customer_name,
industry,
country
)
VALUES(?,?,?)
""", customers)

# =====================================================
# PRODUCTS
# =====================================================

products = [
("AI Analytics","Software",5500),
("CRM Platform","Software",4200),
("Cloud Storage","Cloud",2500),
("HR Management","HR",4800),
("Finance Dashboard","Finance",6000)
]

cursor.executemany("""
INSERT INTO products(
product_name,
category,
price
)
VALUES(?,?,?)
""", products)

# =====================================================
# ORDERS
# =====================================================

orders = [
(1,1,5,"2026-01-12"),
(2,2,2,"2026-02-11"),
(3,3,3,"2026-03-14"),
(4,4,1,"2026-04-20"),
(5,5,4,"2026-05-18"),
(2,1,2,"2026-06-10"),
(1,3,7,"2026-06-14"),
(4,2,5,"2026-07-02")
]

cursor.executemany("""
INSERT INTO orders(
customer_id,
product_id,
quantity,
order_date
)
VALUES(?,?,?,?)
""", orders)

# =====================================================
# SALES
# =====================================================

sales = [
("January",320000,180000,140000),
("February",350000,190000,160000),
("March",310000,175000,135000),
("April",420000,210000,210000),
("May",465000,235000,230000),
("June",510000,260000,250000),
("July",540000,280000,260000)
]

cursor.executemany("""
INSERT INTO sales(
month,
revenue,
expenses,
profit
)
VALUES(?,?,?,?)
""", sales)

conn.commit()
conn.close()

print("="*60)
print("Enterprise sample data inserted successfully.")
print("="*60)