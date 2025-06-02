import sqlite3

conn = sqlite3.connect("expenses.db")
c = conn.cursor()

# Create users table
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# Add user_id column to expenses table if it doesn't exist
# SQLite doesn't support DROP COLUMN, so we check and add if needed.
c.execute("PRAGMA table_info(expenses)")
columns = [col[1] for col in c.fetchall()]

if 'user_id' not in columns:
    c.execute("ALTER TABLE expenses ADD COLUMN user_id INTEGER")
    print("Added 'user_id' column to 'expenses' table.")
else:
    print("'user_id' column already exists in 'expenses' table.")

conn.commit()
conn.close()
