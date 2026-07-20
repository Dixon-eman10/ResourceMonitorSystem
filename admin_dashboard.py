"""
Administrator Dashboard

Runs the administrator dashboard and provides
live dashboard data through a REST API.
"""

from flask import Flask, render_template, jsonify

from dashboard.dashboard import get_dashboard_data
from detection.detection_engine import detect_attack

app = Flask(__name__)


# ==========================================================
# Dashboard Page
# ==========================================================

@app.route("/")
def dashboard():

    return render_template(
        "dashboard.html",
        dashboard_data=get_dashboard_data()
    )


# ==========================================================
# Live Dashboard API
# ==========================================================

@app.route("/api/dashboard-data")
def dashboard_api():

    # Run detection FIRST so any new alerts/incidents
    # are written into the database.
    detection = detect_attack()

    # Then fetch the latest dashboard data.
    data = get_dashboard_data()

    if detection:

        data["system_status"] = detection["dashboard"]["system_status"]
        data["decision"] = detection["decision"]
        data["severity"] = detection["severity"]
        data["attack_type"] = detection["attack_type"]
        data["matched_rules"] = detection["matched_rules"]

    else:

        data["system_status"] = "🟢 Normal"
        data["decision"] = "No Attack"
        data["severity"] = "None"
        data["attack_type"] = "None"
        data["matched_rules"] = []

    return jsonify(data)


# ==========================================================
# Run Dashboard
# ==========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )