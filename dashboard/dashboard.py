"""
Dashboard Module
"""

from database.database import (
    fetch_latest_metric,
    fetch_recent_metrics,
    fetch_recent_alerts,
    fetch_recent_incident_logs
)


def get_dashboard_data():

    return {

        "latest_metric": fetch_latest_metric(),

        "recent_metrics": fetch_recent_metrics(20),

        "alerts": fetch_recent_alerts(10),

        "incident_logs": fetch_recent_incident_logs(10)

    }