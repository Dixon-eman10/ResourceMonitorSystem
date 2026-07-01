import sqlite3

DATABASE_NAME = "database/monitoring.db"


def connect_database():
    return sqlite3.connect(DATABASE_NAME)


def create_tables():

    connection = connect_database()
    cursor = connection.cursor()

    # Resource Metrics
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

    # Alerts
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Alerts (
            AlertID INTEGER PRIMARY KEY AUTOINCREMENT,
            AlertType TEXT NOT NULL,
            Severity TEXT NOT NULL,
            Description TEXT NOT NULL,
            Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Incident Logs
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


def insert_resource_metric(cpu, memory, request_rate, response_time):

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

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO Alerts
        (AlertType, Severity, Description)
        VALUES (?, ?, ?)
    """, (alert_type, severity, description))

    connection.commit()
    connection.close()

def alert_exists(alert_type, severity, minutes=1):
    """
    Check whether an identical alert has been generated
    within the last 'minutes' minutes.
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
    """, (alert_type, severity, f"-{minutes} minute"))

    alert = cursor.fetchone()

    connection.close()

    return alert is not None


def insert_incident_log(event_description, detection_status):

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO IncidentLogs
        (EventDescription, DetectionStatus)
        VALUES (?, ?)
    """, (event_description, detection_status))

    connection.commit()
    connection.close()


def fetch_recent_metrics(limit=20):

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM ResourceMetrics
        ORDER BY Timestamp DESC
        LIMIT ?
    """, (limit,))

    records = cursor.fetchall()

    connection.close()

    return records

def fetch_latest_metric():
    """
    Fetch the most recent monitoring record.
    """

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            CPUUsage,
            MemoryUsage,
            RequestRate,
            ResponseTime,
            Timestamp
        FROM ResourceMetrics
        ORDER BY MetricID DESC
        LIMIT 1
    """)

    record = cursor.fetchone()

    connection.close()

    return record


if __name__ == "__main__":

    create_tables()

    insert_alert(
        "Test Alert",
        "Low",
        "This is a test alert."
    )

    insert_incident_log(
        "Test incident log.",
        "Detected"
    )

    print(fetch_recent_metrics())

    print("Database helper functions tested successfully.")

def fetch_recent_alerts(limit=10):
    """
    Fetch the most recent alerts.
    """

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM Alerts
        ORDER BY Timestamp DESC
        LIMIT ?
    """, (limit,))

    alerts = cursor.fetchall()

    connection.close()

    return alerts


def get_active_alert_count():
    """
    Return the total number of alerts.
    """

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM Alerts
    """)

    count = cursor.fetchone()[0]

    connection.close()

    return count