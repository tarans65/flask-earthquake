import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("earthquakes.db")
cursor = conn.cursor()

# Create a table for earthquake events
cursor.execute("""
CREATE TABLE IF NOT EXISTS earthquakes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_bs TEXT,
    date_ad TEXT,
    local_time TEXT,
    utc_time TEXT,
    latitude REAL,
    longitude REAL,
    magnitude REAL,
    remarks TEXT,
    epicenter TEXT
)
""")

conn.commit()
conn.close()
print("✅ Database schema set up successfully!")
