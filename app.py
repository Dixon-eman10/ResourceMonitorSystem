import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

DATABASE = "database.db"


def create_database():
    """Create the SQLite database and required tables."""

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            fullname TEXT NOT NULL,
            email TEXT,
            department TEXT
        )
    """)

    # Resources table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            author TEXT,
            year INTEGER,
            description TEXT
        )
    """)

    # Search history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            keyword TEXT,
            search_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# ==========================
# Routes
# ==========================

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login")
def login():
    return render_template(
        "login.html",
        error=None,
        success=None
    )


@app.route("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html",
        username="Student"
    )


@app.route("/profile")
def profile():
    return render_template(
        "profile.html",
        fullname="John Doe",
        username="student01",
        email="student@university.edu",
        department="Computer Science"
    )


@app.route("/search", methods=["GET", "POST"])
def search():
    return render_template(
        "search.html",
        results=[]
    )


# ==========================
# Main
# ==========================

if __name__ == "__main__":
    create_database()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )