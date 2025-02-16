@app.route('/')
def index():
    conn = sqlite3.connect("earthquakes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM earthquakes")
    earthquakes = cursor.fetchall()
    conn.close()

    print("Fetched Data:", earthquakes)  # Debugging step

    return render_template("index.html", earthquakes=earthquakes)
