from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    search_query = request.args.get('search', '')

    conn = sqlite3.connect('earthquakes.db')
    conn.row_factory = sqlite3.Row  # ✅ Makes each row a dictionary
    cursor = conn.cursor()

    if search_query:
        query = """SELECT * FROM earthquakes 
                   WHERE epicenter LIKE ? 
                   OR date_ad LIKE ? 
                   OR magnitude LIKE ?"""
        params = [f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"]
    else:
        query = "SELECT * FROM earthquakes"
        params = []

    cursor.execute(query, params)
    earthquakes = [dict(row) for row in cursor.fetchall()]  # ✅ Convert rows to dicts
    conn.close()

    return render_template("index.html", earthquakes=earthquakes, search_query=search_query)
