import sqlite3
import pdfplumber

pdf_path = "databasedata.pdf"  # Ensure this file is in the project folder

# Connect to the SQLite database
conn = sqlite3.connect("earthquakes.db")
cursor = conn.cursor()

# Extract earthquake event data from the PDF
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            lines = text.split("\n")
            for line in lines:
                parts = line.split()
                
                # Ensure it has enough columns (Modify index positions based on actual structure)
                if len(parts) >= 9:
                    try:
                        date_bs = parts[0]  # First column: Date in BS
                        date_ad = parts[1]  # Second column: Date in AD
                        local_time = parts[2]  # Third column: Local Time
                        utc_time = parts[3]  # Fourth column: UTC Time
                        latitude = float(parts[4])  # Fifth column: Latitude
                        longitude = float(parts[5])  # Sixth column: Longitude
                        magnitude = float(parts[6])  # Seventh column: Magnitude
                        remarks = parts[7]  # Eighth column: Remarks (e.g., "NSC", "RSC/NSC")
                        epicenter = " ".join(parts[8:])  # Remaining columns: Epicenter Name

                        # Insert into SQLite database
                        print("Extracted Row:", date_bs, date_ad, local_time, utc_time, latitude, longitude, magnitude, remarks, epicenter)
                        cursor.execute("""
                        INSERT INTO earthquakes (date_bs, date_ad, local_time, utc_time, latitude, longitude, magnitude, remarks, epicenter)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (date_bs, date_ad, local_time, utc_time, latitude, longitude, magnitude, remarks, epicenter))

                    except ValueError:
                        continue  # Skip lines with invalid numerical values

conn.commit()
conn.close()
print("✅ Earthquake data imported successfully!")
