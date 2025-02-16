from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_earthquake_data():
    conn = sqlite3.connect("earthquakes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM earthquakes ORDER BY date_ad DESC")
    data = cursor.fetchall()
    conn.close()
    return data

@app.route("/")
def index():
    earthquakes = get_earthquake_data()
    return render_template("index.html", earthquakes=earthquakes)

if __name__ == "__main__":
    app.run(debug=True)
