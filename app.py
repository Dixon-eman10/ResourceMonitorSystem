import sqlite3
import hashlib
import math
import time

from flask import Flask, render_template

from monitoring.resource_monitor import start_resource_monitor
from monitoring.request_tracker import (
    register_request_tracker,
    start_request_tracker
)

from database.database import create_tables


app = Flask(__name__)

DATABASE = "database.db"


# ==================================================
# Database Initialization
# ==================================================

def create_database():
    """
    Create the application database and required tables.
    """

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


# Register Flask request monitoring
register_request_tracker(app)


# ==================================================
# Routes
# ==================================================

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


@app.route("/stress")
def stress():
    """
    Simulates a computationally expensive
    application-layer request.

    Used ONLY for demonstrating
    low-rate application-layer DDoS detection.
    """

    start = time.perf_counter()

    data = b"LowRateApplicationLayerAttack"

    # CPU-intensive hashing
    for _ in range(250000):
        data = hashlib.sha256(data).digest()

    # Additional floating-point computation
    value = 0.0

    for i in range(120000):
        value += math.sqrt(i)

    elapsed = time.perf_counter() - start

    return {
        "status": "completed",
        "processing_time": round(elapsed, 3),
        "result": round(value, 2),
        "message": "Resource intensive operation finished."
    }


# ==================================================
# Main
# ==================================================

if __name__ == "__main__":

    # Create application database
    create_database()

    # Create monitoring database
    create_tables()

    # Start monitoring components
    start_request_tracker()
    start_resource_monitor()

    # Start Flask server
    app.run(
        host="0.0.0.0",
        port=5000,
        threaded=True,
        debug=False
    )