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


# ==========================================================
# Alert Description
# ==========================================================

def build_alert_description(attack_type, severity, metrics):
    """
    Build a concise professional alert description.
    """

    return (
        f"{attack_type}\n"
        f"Severity: {severity}\n"
        f"CPU: {metrics['cpu']:.1f}% | "
        f"Memory: {metrics['memory']:.1f}% | "
        f"Request Rate: {metrics['request_rate']} req/sec | "
        f"Response Time: {metrics['response_time']:.3f} sec\n"
        f"Recommendation: Investigate server activity immediately."
    )


# ==========================================================
# Alert Creation
# ==========================================================

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


# ==========================================================
# Save Alert
# ==========================================================

def save_alert(alert):
    """
    Save the alert unless a similar alert already exists
    within the cooldown period.
    """

    if alert_exists(
        alert["alert_type"],
        alert["severity"]
    ):
        print("Alert suppressed (cooldown active).")
        return False

    insert_alert(
        alert["alert_type"],
        alert["severity"],
        alert["description"]
    )

    print("New alert saved.")
    return True


# ==========================================================
# Generate Alert
# ==========================================================

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


# ==========================================================
# Dashboard Helpers
# ==========================================================

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