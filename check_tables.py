import sqlite3

from utils.config import DATABASE_PATH


conn = sqlite3.connect(
    DATABASE_PATH
)

cursor = conn.cursor()

cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
)

tables = cursor.fetchall()

print("\nDATABASE TABLES:\n")

for table in tables:
    print(table[0])

print("\nTABLE COLUMNS:\n")

for table in tables:

    table_name = table[0]

    print(f"\n{table_name}:")

    cursor.execute(
        f"PRAGMA table_info({table_name})"
    )

    columns = cursor.fetchall()

    for column in columns:

        print(
            f"  - {column[1]} ({column[2]})"
        )

conn.close()