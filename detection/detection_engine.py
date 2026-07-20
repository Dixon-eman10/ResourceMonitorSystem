"""
Detection Engine

Receives the results produced by the Pattern Analysis Module,
applies detection rules,
assigns a severity level,
makes the final detection decision,
and generates alerts.
"""

from analysis.pattern_analyzer import analyze_pattern

from detection.detection_rules import (
    rule_cpu_high_normal_request,
    rule_slow_http_attack,
    rule_resource_exhaustion,
    rule_high_confidence_attack,
)

from alerts.alert_manager import generate_alert
from database.database import insert_incident_log

import time


# ==========================================================
# Incident Cooldown
# ==========================================================

INCIDENT_COOLDOWN = 60  # seconds

_last_incident_time = {}
_last_alert_time = {}


# ==========================================================
# Apply Detection Rules
# ==========================================================

def apply_detection_rules(analysis):
    """
    Evaluate all detection rules.
    """

    matched_rules = []

    if rule_cpu_high_normal_request(analysis):
        matched_rules.append("Possible Low-Rate DDoS")

    if rule_slow_http_attack(analysis):
        matched_rules.append("Possible Slow HTTP Attack")

    if rule_resource_exhaustion(analysis):
        matched_rules.append("Possible Resource Exhaustion")

    if rule_high_confidence_attack(analysis):
        matched_rules.append("High Confidence Attack")

    return matched_rules


# ==========================================================
# Assign Severity
# ==========================================================

def assign_severity(matched_rules):
    """
    Assign severity based on the number of matched rules.
    """

    count = len(matched_rules)

    if count == 0:
        return "None"

    elif count == 1:
        return "Low"

    elif count == 2:
        return "Medium"

    return "High"


# ==========================================================
# Detection Decision
# ==========================================================

def make_detection_decision(severity):
    """
    Decide whether an attack is occurring.
    """

    if severity in ["Medium", "High"]:
        return "Attack Detected"

    return "No Attack"


# ==========================================================
# Attack Type
# ==========================================================

def get_attack_type(matched_rules):
    """
    Return the primary attack type.
    """

    if not matched_rules:
        return "None"

    if "High Confidence Attack" in matched_rules:
        return "High Confidence Low-Rate DDoS"

    return matched_rules[0]


# ==========================================================
# Main Detection Function
# ==========================================================

def detect_attack():

    result = analyze_pattern()

    if result is None:
        return None

    matched_rules = apply_detection_rules(result["analysis"])

    severity = assign_severity(matched_rules)

    decision = make_detection_decision(severity)

    attack_type = get_attack_type(matched_rules)

    result["matched_rules"] = matched_rules
    result["severity"] = severity
    result["decision"] = decision
    result["attack_type"] = attack_type

    # ------------------------------------------------------

    if decision == "Attack Detected":

        current_time = time.time()

        # ---------------------------------------------
        # Alert Cooldown
        # ---------------------------------------------

        if (
            attack_type not in _last_alert_time
            or current_time - _last_alert_time[attack_type] >= INCIDENT_COOLDOWN
        ):

            generate_alert(
                attack_type,
                severity,
                result["metrics"]
            )

            _last_alert_time[attack_type] = current_time

        # ---------------------------------------------
        # Incident Log Cooldown
        # ---------------------------------------------

        if (
            attack_type not in _last_incident_time
            or current_time - _last_incident_time[attack_type] >= INCIDENT_COOLDOWN
        ):

            description = (
                f"{attack_type} | "
                f"Severity: {severity} | "
                f"CPU: {result['metrics']['cpu']:.1f}% | "
                f"Memory: {result['metrics']['memory']:.1f}% | "
                f"Request Rate: {result['metrics']['request_rate']} req/sec | "
                f"Response Time: {result['metrics']['response_time']:.3f} sec"
            )

            insert_incident_log(
                event_description=description,
                detection_status=decision
            )

            _last_incident_time[attack_type] = current_time

    # ------------------------------------------------------

    dashboard_data = {

        "system_status":
            "🔴 Attack Detected"
            if decision == "Attack Detected"
            else "🟢 Normal",

        "decision": decision,

        "severity": severity,

        "attack_type": attack_type,

        "matched_rules": matched_rules,

        "latest_metrics": result["metrics"]
    }

    result["dashboard"] = dashboard_data

    return result


# ==========================================================
# Standalone Testing
# ==========================================================

if __name__ == "__main__":

    result = detect_attack()

    if result is None:
        print("No monitoring data available.")
        exit()

    print("\n========== DETECTION ENGINE ==========\n")

    print(f"Decision      : {result['decision']}")
    print(f"Severity      : {result['severity']}")
    print(f"Attack Type   : {result['attack_type']}")

    print("\nDetection Rules Triggered:")

    if result["matched_rules"]:
        for rule in result["matched_rules"]:
            print(f"• {rule}")
    else:
        print("No detection rules matched.")

    print("\n========== DASHBOARD ==========\n")

    print(f"System Status : {result['dashboard']['system_status']}")
    print(f"Decision      : {result['dashboard']['decision']}")
    print(f"Severity      : {result['dashboard']['severity']}")
    print(f"Attack Type   : {result['dashboard']['attack_type']}")

    print("\nLatest Metrics")

    metrics = result["dashboard"]["latest_metrics"]

    print(f"CPU Usage      : {metrics['cpu']:.1f}%")
    print(f"Memory Usage   : {metrics['memory']:.1f}%")
    print(f"Request Rate   : {metrics['request_rate']} req/sec")
    print(f"Response Time  : {metrics['response_time']:.3f} sec")