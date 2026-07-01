"""
Alert Manager

Creates alerts and stores them in the database.
"""

from database.database import insert_alert


def generate_alert(attack_type, severity):
    """
    Generate and store an alert.
    """

    description = f"{attack_type} detected."

    insert_alert(
        alert_type=attack_type,
        severity=severity,
        description=description
    )

    return {
        "alert_type": attack_type,
        "severity": severity,
        "description": description
    }