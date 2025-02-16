import sqlite3
import pdfplumber

# Path to your PDF file
PDF_PATH = "databasedata.pdf"
DB_PATH = "earthquake.db"

# Function to extract data from PDF
def extract_data():
    data = []
    with pdfplumber.open(PDF_PATH) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = text.split("\n")[1:]  # Skip header row if present
                for line in lines:
                    parts = line.split()
                    if len(parts) >= 9:  # Ensure we have enough columns
                        data.append((
                            parts[0],  # Date BS
                            parts[1],  # Date AD
                            parts[2],  # Local Time
                            parts[3],  # UTC Time
                            float(parts[4]),  # Latitude
                            float(parts[5]),  # Longitude
                            float(parts[6]),  # Magnitude
                            parts[7],  # Remarks
                            " ".join(parts[8:])  # Epicenter (handles spaces)
                        ))
    return data

# Function to insert data into SQLite
def insert_data(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute('''
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
    ''')

    # Insert data
    cursor.executemany('''
        INSERT INTO earthquakes (date_bs, date_ad, local_time, utc_time, latitude, longitude, magnitude, remarks, epicenter)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)

    conn.commit()
    conn.close()

# Main execution
data = extract_data()
if data:
    insert_data(data)
    print(f"✅ Successfully inserted {len(data)} records into the database.")
else:
    print("❌ No data extracted from the PDF.")
