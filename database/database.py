"""
Database Module

Handles all SQLite operations for the Resource Monitoring
and Low-Rate DDoS Detection System.
"""

import sqlite3

DATABASE_NAME = "database/monitoring.db"


# ==========================================================
# Database Connection
# ==========================================================

def connect_database():
    """Create and return a SQLite connection."""
    return sqlite3.connect(DATABASE_NAME)


# ==========================================================
# Database Initialization
# ==========================================================

def create_tables():
    """Create all required database tables."""

    connection = connect_database()
    cursor = connection.cursor()

    # ------------------------------------------------------
    # Resource Metrics
    # ------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ResourceMetrics (
            MetricID INTEGER PRIMARY KEY AUTOINCREMENT,
            CPUUsage REAL NOT NULL,
            MemoryUsage REAL NOT NULL,
            RequestRate INTEGER NOT NULL,
            ResponseTime REAL NOT NULL,
            Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ------------------------------------------------------
    # Alerts
    # ------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Alerts (
            AlertID INTEGER PRIMARY KEY AUTOINCREMENT,
            AlertType TEXT NOT NULL,
            Severity TEXT NOT NULL,
            Description TEXT NOT NULL,
            Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ------------------------------------------------------
    # Incident Logs
    # ------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS IncidentLogs (
            LogID INTEGER PRIMARY KEY AUTOINCREMENT,
            EventDescription TEXT NOT NULL,
            DetectionStatus TEXT NOT NULL,
            Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


# ==========================================================
# Insert Functions
# ==========================================================

def insert_resource_metric(cpu, memory, request_rate, response_time):
    """Insert one monitoring record."""

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO ResourceMetrics
        (CPUUsage, MemoryUsage, RequestRate, ResponseTime)
        VALUES (?, ?, ?, ?)
    """, (cpu, memory, request_rate, response_time))

    connection.commit()
    connection.close()


def insert_alert(alert_type, severity, description):
    """Insert an alert."""

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO Alerts
        (AlertType, Severity, Description)
        VALUES (?, ?, ?)
    """, (alert_type, severity, description))

    connection.commit()
    connection.close()


def insert_incident_log(event_description, detection_status):
    """Insert an incident log."""

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO IncidentLogs
        (EventDescription, DetectionStatus)
        VALUES (?, ?)
    """, (event_description, detection_status))

    connection.commit()
    connection.close()


# ==========================================================
# Alert Helpers
# ==========================================================

def alert_exists(alert_type, severity, minutes=5):
    """
    Check whether an identical alert has already been generated
    within the last 'minutes' minutes.

    This prevents the dashboard from filling with duplicate alerts
    during the same attack.
    """

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT AlertID
        FROM Alerts
        WHERE AlertType = ?
        AND Severity = ?
        AND Timestamp >= datetime('now', ?)
        LIMIT 1
    """, (alert_type, severity, f"-{minutes} minutes"))

    alert = cursor.fetchone()

    connection.close()

    return alert is not None


def get_active_alert_count():
    """Return the total number of alerts."""

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM Alerts
    """)

    count = cursor.fetchone()[0]

    connection.close()

    return count


# ==========================================================
# Fetch Functions
# ==========================================================

def fetch_latest_metric():
    """Return the latest monitoring record as a dictionary."""

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM ResourceMetrics
        ORDER BY MetricID DESC
        LIMIT 1
    """)

    metric = cursor.fetchone()

    connection.close()

    if metric is None:
        return None

    return {
        "metric_id": metric[0],
        "cpu": metric[1],
        "memory": metric[2],
        "request_rate": metric[3],
        "response_time": metric[4],
        "timestamp": metric[5]
    }


def fetch_recent_metrics(limit=20):
    """Return recent monitoring records as dictionaries."""

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM ResourceMetrics
        ORDER BY MetricID DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    connection.close()

    rows.reverse()

    metrics = []

    for row in rows:

        metrics.append({
            "metric_id": row[0],
            "cpu": row[1],
            "memory": row[2],
            "request_rate": row[3],
            "response_time": row[4],
            "timestamp": row[5]
        })

    return metrics


def fetch_recent_alerts(limit=10):
    """Return the most recent alerts."""

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM Alerts
        ORDER BY AlertID DESC
        LIMIT ?
    """, (limit,))

    alerts = cursor.fetchall()

    connection.close()

    return alerts


def fetch_recent_incident_logs(limit=10):
    """Return the most recent incident logs."""

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM IncidentLogs
        ORDER BY LogID DESC
        LIMIT ?
    """, (limit,))

    logs = cursor.fetchall()

    connection.close()

    return logs


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    create_tables()

    print("Database initialized successfully.")

    print("\nLatest Metric")
    print(fetch_latest_metric())

    print("\nRecent Metrics")
    print(fetch_recent_metrics())

    print("\nRecent Alerts")
    print(fetch_recent_alerts())

    print("\nRecent Incident Logs")
    print(fetch_recent_incident_logs())


def cleanup_old_metrics(minutes=30):
    """
    Delete resource metrics older than the specified number of minutes.
    """

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM ResourceMetrics
        WHERE Timestamp < datetime('now', ?)
    """, (f"-{minutes} minutes",))

    connection.commit()
    connection.close()