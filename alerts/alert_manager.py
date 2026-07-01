"""
Alert Manager

Responsible for:

- Creating alerts
- Formatting alert descriptions
- Saving alerts to the database
"""

from datetime import datetime

from database.database import (
    insert_alert,
    alert_exists,
    fetch_recent_alerts,
    get_active_alert_count
)
from alerts.notifier import notify


def build_alert_description(attack_type, severity, metrics):
    """
    Build a professional alert description.
    """

    return f"""
===================================================
LOW-RATE APPLICATION-LAYER DDoS ALERT
===================================================

Attack Type:
{attack_type}

Severity:
{severity}

Description:
Abnormal server resource consumption detected.

Current Resource Metrics:
- CPU Usage      : {metrics['cpu']}%
- Memory Usage   : {metrics['memory']}%
- Request Rate   : {metrics['request_rate']} req/sec
- Response Time  : {metrics['response_time']} sec

Recommendation:
Investigate current client sessions and
monitor resource utilization closely.

Status:
Attack Detected

Generated:
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

===================================================
""".strip()


def create_alert(attack_type, severity, metrics):
    """
    Create an alert object.
    """

    return {
        "alert_type": attack_type,
        "severity": severity,
        "description": build_alert_description(
            attack_type,
            severity,
            metrics
        ),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def save_alert(alert):
    """
    Save the alert unless a similar one
    already exists recently.
    """

    if alert_exists(
        alert["alert_type"],
        alert["severity"]
    ):
        print("Duplicate alert suppressed.")
        return False

    insert_alert(
        alert["alert_type"],
        alert["severity"],
        alert["description"]
    )

    print("New alert saved.")

    return True

def generate_alert(attack_type, severity, metrics):
    """
    Generate, save and notify.
    """

    alert = create_alert(
        attack_type,
        severity,
        metrics
    )

    saved = save_alert(alert)

    alert["saved"] = saved

    if saved:
        notify(alert)

    return alert

def get_recent_alerts(limit=10):
    """
    Return recent alerts for the dashboard.
    """
    return fetch_recent_alerts(limit)


def get_alert_summary():
    """
    Return summary information for the dashboard.
    """
    return {
        "active_alerts": get_active_alert_count(),
        "recent_alerts": get_recent_alerts()
    }