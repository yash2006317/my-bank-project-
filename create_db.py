import sqlite3

conn = sqlite3.connect("database.db")

conn.execute("""
CREATE TABLE users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
password TEXT
)
""")

conn.execute("""
CREATE TABLE accounts(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
account_number TEXT,
balance INTEGER
)
""")

conn.execute("""
CREATE TABLE transactions(
id INTEGER PRIMARY KEY AUTOINCREMENT,
account_id INTEGER,
type TEXT,
amount INTEGER
)
""")

# default login
conn.execute(
"INSERT INTO users (username,password) VALUES (?,?)",
("admin","1234")
)

conn.commit()
conn.close()

print("Database Created")