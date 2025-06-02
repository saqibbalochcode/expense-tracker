import sqlite3

# Connect to SQLite (it will create the file if it doesn't exist)
conn = sqlite3.connect('expenses.db')

# Create a cursor
c = conn.cursor()

# Create the expenses table
c.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        date TEXT NOT NULL
    )
''')

# Commit and close
conn.commit()
conn.close()

print("✅ Database and table created!")
