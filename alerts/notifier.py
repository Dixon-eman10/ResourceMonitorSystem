"""
Notifier Module

Responsible for notifying the administrator
when an alert is generated.
"""


def notify(alert):
    """
    Display a notification for the generated alert.
    Future versions can send emails, SMS, Telegram, etc.
    """

    notification = f"""
===================================================
🚨 SECURITY ALERT 🚨
===================================================

Severity    : {alert['severity']}
Attack Type : {alert['alert_type']}

Description:
{alert['description']}

===================================================
"""

    print(notification)

    return notification