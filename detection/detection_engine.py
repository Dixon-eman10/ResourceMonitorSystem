"""
Detection Engine

Receives the results produced by the Pattern Analysis Module,
applies detection rules, assigns a severity level,
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


def apply_detection_rules(analysis):

    matched_rules = []

    if rule_cpu_high_normal_request(analysis):
        matched_rules.append("Possible Low-Rate DDoS")

    if rule_slow_http_attack(analysis):
        matched_rules.append("Possible Slow HTTP Attack")

    if rule_resource_exhaustion(analysis):
        matched_rules.append("Possible Resource Exhaustion Attack")

    if rule_high_confidence_attack(analysis):
        matched_rules.append("High Confidence Attack")

    return matched_rules


def assign_severity(pattern_status, matched_rules):

    count = len(matched_rules)

    if count == 0:
        return "None"

    if count == 1:
        if pattern_status == "Suspicious":
            return "Medium"
        return "Low"

    return "High"


def make_detection_decision(pattern_status, severity):

    if pattern_status == "Suspicious" and severity in ["Medium", "High"]:
        return "Attack Detected"

    return "No Attack"


def get_attack_type(matched_rules):
    """
    Return the primary detected attack type.
    """

    if matched_rules:
        return matched_rules[0]

    return "None"


def detect_attack():

    result = analyze_pattern()

    if result is None:
        return None

    matched_rules = apply_detection_rules(result["analysis"])

    severity = assign_severity(
        result["pattern"]["overall_status"],
        matched_rules
    )

    decision = make_detection_decision(
        result["pattern"]["overall_status"],
        severity
    )

    attack_type = get_attack_type(matched_rules)

    result["matched_rules"] = matched_rules
    result["severity"] = severity
    result["decision"] = decision
    result["attack_type"] = attack_type

    if decision == "Attack Detected":

        # Generate an alert
        ggenerate_alert(
        attack_type,
        severity,
        result["metrics"]
        )

        # Log the incident
        description = (
            f"{attack_type} | "
            f"Severity: {severity} | "
            f"CPU: {result['metrics']['cpu']}% | "
            f"Memory: {result['metrics']['memory']}% | "
            f"Request Rate: {result['metrics']['request_rate']} req/sec | "
            f"Response Time: {result['metrics']['response_time']} sec"
        )

        insert_incident_log(
            event_description=description,
            detection_status=decision
        )

    dashboard_data = {
        "system_status": (
            "🔴 Attack Detected"
            if decision == "Attack Detected"
            else "🟢 Normal"
        ),
        "decision": decision,
        "severity": severity,
        "attack_type": attack_type,
        "matched_rules": matched_rules,
        "latest_metrics": result["metrics"]
    }

    result["dashboard"] = dashboard_data

    return result


if __name__ == "__main__":

    result = detect_attack()

    if result is None:
        print("No monitoring data available.")
        exit()

    print("\n========== DETECTION ENGINE ==========\n")

    print(f"Pattern Status : {result['pattern']['overall_status']}")
    print(f"Severity       : {result['severity']}")
    print(f"Decision       : {result['decision']}")
    print(f"Attack Type    : {result['attack_type']}")

    print("\nDetection Rules Triggered:")

    if result["matched_rules"]:
        for rule in result["matched_rules"]:
            print(f"• {rule}")
    else:
        print("No detection rules matched.")

    print("\n========== DASHBOARD DATA ==========\n")
    print(f"System Status : {result['dashboard']['system_status']}")
    print(f"Decision      : {result['dashboard']['decision']}")
    print(f"Severity      : {result['dashboard']['severity']}")
    print(f"Attack Type   : {result['dashboard']['attack_type']}")

    print("\nLatest Metrics:")
    print(f"CPU Usage      : {result['dashboard']['latest_metrics']['cpu']}%")
    print(f"Memory Usage   : {result['dashboard']['latest_metrics']['memory']}%")
    print(f"Request Rate   : {result['dashboard']['latest_metrics']['request_rate']} req/sec")
    print(f"Response Time  : {result['dashboard']['latest_metrics']['response_time']} sec")