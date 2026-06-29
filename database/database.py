import sqlite3

DATABASE_NAME = "database.db"


def connect_db():
    """
    Connect to the SQLite database.
    """
    return sqlite3.connect(DATABASE_NAME)


def create_tables():
    """
    Create the ResourceMetrics table.
    """

    connection = connect_db()
    cursor = connection.cursor()

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

    connection.commit()
    connection.close()


def insert_resource_metric(cpu, memory, request_rate, response_time):
    """
    Insert one monitoring record.
    """

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO ResourceMetrics
        (
            CPUUsage,
            MemoryUsage,
            RequestRate,
            ResponseTime
        )
        VALUES (?, ?, ?, ?)
    """, (
        cpu,
        memory,
        request_rate,
        response_time
    ))

    connection.commit()
    connection.close()


if __name__ == "__main__":

    create_tables()

    print("ResourceMetrics table created successfully.")